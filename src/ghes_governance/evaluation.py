"""Minimal governed evaluation for the first governed slices (tickets T1–T2).

Internal engine logic behind the Execution boundary seam: select the single active
authoritative Observe binding for a (policy, repository) pair via three-result scope
resolution, evaluate its composite policy through PredicateEvaluation, and aggregate the
engine-owned Policy Outcome and Coverage State. Deliberately minimal — scope is an
``equals`` leaf or an ``any``/``all``/``not`` combinator under three-valued (Kleene) logic,
predicates are a single ``equals`` (full operators and aggregation precedence are T3), and
authority selection yields a terminal pair-level Unknown for a proven conflict or an A=1/U≥1
undeterminable pair (the A=0/U≥2 case and effective periods are later increments). Broader
inputs fail loud.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .enums import (
    ApplicabilityOutcome,
    CoverageState,
    EnforcementMode,
    EvaluationRole,
    GovernanceInterpretation,
    PolicyOutcome,
    ProviderResult,
    RequirementOutcome,
    TechnicalOutcome,
)
from .errors import BundleError


@dataclass(frozen=True)
class AuthorityConflict:
    """A proven authority conflict: two or more Applicable authoritative bindings for a pair.

    Carries the conflicting bindings so the Execution boundary can record the terminal
    pair-level Unknown outcome and enumerate them in the authority-conflict finding
    (ADR-0005, ADR-0013, ADR-0015).
    """

    conflicting: list[dict[str, Any]]


@dataclass(frozen=True)
class AuthorityUndeterminable:
    """Authority cannot be established (ADR-0015, A=1 & U≥1): one binding definitely applies
    and at least one other's scope applicability is Unknown, so it is neither counted nor
    excluded. Carries the applicable candidates and, per unresolved candidate, the scope
    attributes that could not be determined, for the terminal Unknown and its finding.
    """

    applicable: list[dict[str, Any]]
    undeterminable: list[tuple[dict[str, Any], list[str]]]


def select_authoritative_binding(
    bindings: list[dict[str, Any]],
    policy: dict[str, Any],
    repo: dict[str, Any],
    evaluation_timestamp: str,
) -> tuple[dict[str, Any], ApplicabilityOutcome] | AuthorityConflict | AuthorityUndeterminable | None:
    """Select the authoritative Observe binding for (policy, repo) and its applicability.

    Returns ``(binding, applicability)`` where applicability is Applicable or Unknown;
    ``None`` when no active authoritative binding applies (a normal ungoverned state); an
    ``AuthorityConflict`` when two or more Applicable bindings prove a conflict; or an
    ``AuthorityUndeterminable`` when one binding definitely applies and at least one other's
    applicability is Unknown (A=1, U≥1). NotApplicable bindings are excluded. Two or more
    Unknown candidates with none Applicable (A=0, U≥2) remains undefined and fails loud.
    """
    candidates = [
        (binding, resolve_applicability(binding.get("scope"), repo))
        for binding in bindings
        if binding.get("evaluation_role") == EvaluationRole.AUTHORITATIVE.value
        and binding.get("enforcement_mode") == EnforcementMode.OBSERVE.value
        and binding.get("policy") == policy["id"]
        and _binding_active(binding, evaluation_timestamp)
    ]
    applicable = [b for b, outcome in candidates if outcome is ApplicabilityOutcome.APPLICABLE]
    undeterminable = [b for b, outcome in candidates if outcome is ApplicabilityOutcome.UNKNOWN]

    if len(applicable) > 1:
        # A proven authority conflict: more than one binding whose scope is Applicable
        # (ADR-0005, ADR-0013, ADR-0015). The caller records the terminal pair-level Unknown.
        return AuthorityConflict(conflicting=applicable)
    if applicable and undeterminable:
        # A=1, U≥1: one binding definitely applies and at least one other's applicability is
        # Unknown, so the Unknown candidate is neither counted nor excluded — authority cannot
        # be established (ADR-0015). The caller records the terminal pair-level Unknown.
        return AuthorityUndeterminable(
            applicable=applicable,
            undeterminable=[
                (binding, _undetermined_attributes(binding.get("scope"), repo))
                for binding in undeterminable
            ],
        )
    if len(undeterminable) > 1:
        # A=0, U≥2: two or more undeterminable candidates and none Applicable — still undefined
        # in this slice; fail loud rather than resolve.
        raise NotImplementedError(
            "undetermined authoritative binding selection: two or more authoritative bindings "
            "have Unknown applicability and none is Applicable; resolving it is not defined in "
            "this slice"
        )
    if applicable:
        return applicable[0], ApplicabilityOutcome.APPLICABLE
    if undeterminable:
        return undeterminable[0], ApplicabilityOutcome.UNKNOWN
    return None


def resolve_applicability(scope: Any, repo: dict[str, Any]) -> ApplicabilityOutcome:
    """Resolve a scope expression to Applicable / NotApplicable / Unknown.

    A scope expression is a single-key dict: an ``equals`` leaf, which consults the
    three-result attribute provider, or an ``any`` / ``all`` / ``not`` combinator over
    nested scope expressions combined under three-valued (Kleene) logic. Cannot Determine
    on a decision-relevant operand → Unknown.
    """
    operator = _expression_operator(scope, "scope expression")
    if operator == "equals":
        return _resolve_equals_scope(scope, repo)
    if operator == "any":
        return _resolve_any(scope["any"], repo)
    if operator == "all":
        return _resolve_all(scope["all"], repo)
    if operator == "not":
        return _resolve_not(scope["not"], repo)
    raise NotImplementedError(f"unsupported scope operator {operator!r}")


def _expression_operator(expression: Any, what: str) -> str:
    if not isinstance(expression, dict) or len(expression) != 1:
        raise BundleError(f"malformed {what}: {expression!r}")
    return next(iter(expression))


def _resolve_equals_scope(scope: Any, repo: dict[str, Any]) -> ApplicabilityOutcome:
    """The ``equals`` leaf: Cannot Determine → Unknown; present-and-matching → Applicable;
    present-but-different or absent → NotApplicable."""
    condition = _single_equals(scope, "attribute", "scope expression")
    result, value = _provider_lookup(repo, condition["attribute"])
    if result is ProviderResult.CANNOT_DETERMINE:
        return ApplicabilityOutcome.UNKNOWN
    if result is ProviderResult.VALUE_PRESENT and value == condition["value"]:
        return ApplicabilityOutcome.APPLICABLE
    return ApplicabilityOutcome.NOT_APPLICABLE


def _resolve_any(operands: Any, repo: dict[str, Any]) -> ApplicabilityOutcome:
    """Three-valued OR over nested scope expressions.

    Applicable if any operand is Applicable (a determined-TRUE operand forces the result);
    otherwise Unknown if any operand is Unknown; otherwise NotApplicable.
    """
    if not isinstance(operands, list) or not operands:
        raise BundleError(f"malformed 'any' scope expression: {operands!r}")
    outcomes = [resolve_applicability(operand, repo) for operand in operands]
    if ApplicabilityOutcome.APPLICABLE in outcomes:
        return ApplicabilityOutcome.APPLICABLE
    if ApplicabilityOutcome.UNKNOWN in outcomes:
        return ApplicabilityOutcome.UNKNOWN
    return ApplicabilityOutcome.NOT_APPLICABLE


def _resolve_all(operands: Any, repo: dict[str, Any]) -> ApplicabilityOutcome:
    """Three-valued AND over nested scope expressions.

    NotApplicable if any operand is NotApplicable (a determined-FALSE operand forces the
    result); otherwise Unknown if any operand is Unknown; otherwise Applicable.
    """
    if not isinstance(operands, list) or not operands:
        raise BundleError(f"malformed 'all' scope expression: {operands!r}")
    outcomes = [resolve_applicability(operand, repo) for operand in operands]
    if ApplicabilityOutcome.NOT_APPLICABLE in outcomes:
        return ApplicabilityOutcome.NOT_APPLICABLE
    if ApplicabilityOutcome.UNKNOWN in outcomes:
        return ApplicabilityOutcome.UNKNOWN
    return ApplicabilityOutcome.APPLICABLE


def _resolve_not(operand: Any, repo: dict[str, Any]) -> ApplicabilityOutcome:
    """Three-valued negation of exactly one nested scope expression.

    Applicable ↔ NotApplicable; Unknown negates to Unknown — negation cannot resolve an
    undeterminable operand. ``not`` takes exactly one operand (a single scope expression).
    """
    if not isinstance(operand, dict) or len(operand) != 1:
        raise BundleError(f"malformed 'not' scope expression: {operand!r}")
    outcome = resolve_applicability(operand, repo)
    if outcome is ApplicabilityOutcome.APPLICABLE:
        return ApplicabilityOutcome.NOT_APPLICABLE
    if outcome is ApplicabilityOutcome.NOT_APPLICABLE:
        return ApplicabilityOutcome.APPLICABLE
    return ApplicabilityOutcome.UNKNOWN


def _undetermined_attributes(scope: Any, repo: dict[str, Any]) -> list[str]:
    """Scope attributes that could not be determined *and* were decision-relevant to an
    Unknown applicability — deduplicated, in scope-expression order.

    Respects the combinator short-circuit: a determined operand that forces the result
    (a TRUE in ``any``, a FALSE in ``all``) hides the undetermined operands it overrode, so
    only operands that are themselves Unknown are followed. The reported attributes therefore
    come from the same provider observations that produced the applicability and never
    disagree with it.
    """
    operator = _expression_operator(scope, "scope expression")
    if operator == "equals":
        condition = _single_equals(scope, "attribute", "scope expression")
        result, _value = _provider_lookup(repo, condition["attribute"])
        return [condition["attribute"]] if result is ProviderResult.CANNOT_DETERMINE else []
    if operator == "not":
        return _undetermined_attributes(scope["not"], repo)
    if operator in ("any", "all"):
        attributes: list[str] = []
        for operand in scope[operator]:
            if resolve_applicability(operand, repo) is ApplicabilityOutcome.UNKNOWN:
                attributes.extend(_undetermined_attributes(operand, repo))
        return list(dict.fromkeys(attributes))
    return []


def evaluate_policy(policy: dict[str, Any], repo: dict[str, Any]) -> dict[str, Any]:
    """Evaluate an applicable governed pair: per-requirement findings plus aggregated outcomes."""
    findings = [_evaluate_requirement(policy["id"], repo, req) for req in policy["requirements"]]
    policy_outcome, coverage_state = _aggregate(findings)
    return {
        "findings": findings,
        "policy_outcome": policy_outcome.value,
        "coverage_state": coverage_state.value,
    }


def _provider_lookup(repo: dict[str, Any], attribute: str) -> tuple[ProviderResult, Any]:
    """The GitHub-native attribute provider under the three-result contract.

    Cannot Determine is distinct from Value Absent: an attribute the synthetic estate
    marks undeterminable is Cannot Determine and is never treated as ordinary absence.
    """
    if attribute in repo.get("undeterminable", []):
        return ProviderResult.CANNOT_DETERMINE, None
    if attribute in repo:
        return ProviderResult.VALUE_PRESENT, repo[attribute]
    return ProviderResult.VALUE_ABSENT, None


def _binding_active(binding: dict[str, Any], timestamp: str) -> bool:
    # Half-open [effective_start, effective_end); ISO-8601 UTC strings order chronologically.
    start = binding.get("effective_start")
    end = binding.get("effective_end")
    return (start is None or start <= timestamp) and (end is None or timestamp < end)


def _evaluate_requirement(
    policy_id: str, repo: dict[str, Any], requirement: dict[str, Any]
) -> dict[str, Any]:
    strategy = requirement.get("strategy", {})
    if (strategy.get("identifier"), strategy.get("version")) != ("PredicateEvaluation", 1):
        raise NotImplementedError(
            "only PredicateEvaluation v1 is registered; other strategies are T2/T5"
        )
    technical = _evaluate_predicate(requirement.get("predicate"), repo)
    interpretation = GovernanceInterpretation.NONE  # no Governance Relief in this slice (T4)
    outcome = _interpret(technical, interpretation)
    return {
        "policy_id": policy_id,
        "repository_id": repo["id"],
        "requirement_id": requirement["id"],
        "technical_outcome": technical.value,
        "governance_interpretation": interpretation.value,
        "requirement_outcome": outcome.value,
    }


def _evaluate_predicate(predicate: Any, repo: dict[str, Any]) -> TechnicalOutcome:
    condition = _single_equals(predicate, "setting", "predicate")
    settings = repo.get("settings", {})
    holds = settings.get(condition["setting"]) == condition["value"]
    return TechnicalOutcome.COMPLIANT if holds else TechnicalOutcome.NON_COMPLIANT


def _interpret(
    technical: TechnicalOutcome, interpretation: GovernanceInterpretation
) -> RequirementOutcome:
    # No relief in this slice: the Requirement Outcome mirrors the Technical Outcome.
    return {
        TechnicalOutcome.COMPLIANT: RequirementOutcome.COMPLIANT,
        TechnicalOutcome.NON_COMPLIANT: RequirementOutcome.NON_COMPLIANT,
        TechnicalOutcome.UNKNOWN: RequirementOutcome.UNKNOWN,
        TechnicalOutcome.NOT_EVALUATED: RequirementOutcome.UNKNOWN,
    }[technical]


def _aggregate(findings: list[dict[str, Any]]) -> tuple[PolicyOutcome, CoverageState]:
    outcomes = {f["requirement_outcome"] for f in findings}
    if RequirementOutcome.NON_COMPLIANT.value in outcomes:
        policy = PolicyOutcome.NON_COMPLIANT
    elif RequirementOutcome.UNKNOWN.value in outcomes:
        policy = PolicyOutcome.UNKNOWN
    else:
        policy = PolicyOutcome.COMPLIANT
    coverage = (
        CoverageState.UNKNOWN
        if RequirementOutcome.UNKNOWN.value in outcomes
        else CoverageState.COVERED
    )
    return policy, coverage


def _single_equals(expression: Any, operand_key: str, what: str) -> dict[str, Any]:
    if not isinstance(expression, dict) or set(expression) != {"equals"}:
        raise NotImplementedError(
            f"only a single 'equals' {what} is supported in this slice; "
            "combinators and other operators are T2/T3"
        )
    condition = expression["equals"]
    if not isinstance(condition, dict) or operand_key not in condition or "value" not in condition:
        raise BundleError(f"malformed 'equals' {what}: {condition!r}")
    return condition
