"""Minimal governed evaluation for the first governed slices (tickets T1–T2).

Internal engine logic behind the Execution boundary seam: select the single active
authoritative Observe binding for a (policy, repository) pair via three-result scope
resolution, evaluate its composite policy through PredicateEvaluation, and aggregate the
engine-owned Policy Outcome and Coverage State. Deliberately minimal — scope is a single
``equals`` under the three-result contract (scope combinators and the divergent-cell
truth table are later increments), predicates are a single ``equals`` (full operators and
aggregation precedence are T3), and authority conflict is T4. Broader inputs fail loud.
"""

from __future__ import annotations

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


def select_authoritative_binding(
    bindings: list[dict[str, Any]],
    policy: dict[str, Any],
    repo: dict[str, Any],
    evaluation_timestamp: str,
) -> tuple[dict[str, Any], ApplicabilityOutcome] | None:
    """Select the authoritative Observe binding for (policy, repo) and its applicability.

    Returns ``(binding, applicability)`` where applicability is Applicable or Unknown, or
    ``None`` when no active authoritative binding applies (a normal ungoverned state).
    NotApplicable bindings are excluded. More than one *Applicable* binding is a proven
    authority conflict, deferred to T4. A multiplicity that instead turns on an Unknown
    applicability is neither proven nor excluded and is undefined in the architecture
    (ADR-0005/0013 speak of Applicable matches); both fail loud rather than resolve here.
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
        # A proven authoritative overlap: more than one binding whose scope is Applicable
        # (ADR-0005, ADR-0013). Resolving it to a pair-level Unknown is ticket T4.
        raise NotImplementedError(
            "authority conflict (more than one applicable authoritative binding) is ticket T4"
        )
    if undeterminable and (applicable or len(undeterminable) > 1):
        # More than one binding could apply and at least one has Unknown applicability, so an
        # authoritative overlap is neither proven nor excluded. This is not the proven conflict
        # of ADR-0005/0013 (defined over Applicable matches); the architecture does not define
        # it, so fail loud rather than silently pick the Applicable binding or invent a winner.
        raise NotImplementedError(
            "undetermined authoritative binding selection: more than one authoritative binding "
            "could apply and at least one has Unknown applicability; resolving it is not defined "
            "in this slice"
        )
    if applicable:
        return applicable[0], ApplicabilityOutcome.APPLICABLE
    if undeterminable:
        return undeterminable[0], ApplicabilityOutcome.UNKNOWN
    return None


def resolve_applicability(scope: Any, repo: dict[str, Any]) -> ApplicabilityOutcome:
    """Resolve a single-``equals`` scope condition under the three-result contract.

    Cannot Determine on the required attribute → Unknown; a present value that matches →
    Applicable; a present-but-different or absent value → NotApplicable. Scope combinators
    and the divergent-cell truth table are later increments.
    """
    condition = _single_equals(scope, "attribute", "scope expression")
    result, value = _provider_lookup(repo, condition["attribute"])
    if result is ProviderResult.CANNOT_DETERMINE:
        return ApplicabilityOutcome.UNKNOWN
    if result is ProviderResult.VALUE_PRESENT and value == condition["value"]:
        return ApplicabilityOutcome.APPLICABLE
    return ApplicabilityOutcome.NOT_APPLICABLE


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
