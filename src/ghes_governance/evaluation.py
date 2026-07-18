"""Minimal governed evaluation for the first governed slice (ticket T1).

Internal engine logic behind the Execution boundary seam: select the single active
authoritative Observe binding for a (policy, repository) pair, evaluate its composite
policy through PredicateEvaluation, and aggregate the engine-owned Policy Outcome and
Coverage State. Deliberately minimal — scope matching is a single all-determined
``equals`` (the three-result contract and Unknown propagation are T2), predicates are a
single ``equals`` (full operators, combinators, and aggregation precedence are T3), and
authority conflict is T4. Broader inputs fail loud rather than resolve silently.
"""

from __future__ import annotations

from typing import Any

from .enums import (
    CoverageState,
    EnforcementMode,
    EvaluationRole,
    GovernanceInterpretation,
    PolicyOutcome,
    RequirementOutcome,
    TechnicalOutcome,
)
from .errors import BundleError


def select_authoritative_binding(
    bindings: list[dict[str, Any]],
    policy: dict[str, Any],
    repo: dict[str, Any],
    evaluation_timestamp: str,
) -> dict[str, Any] | None:
    """Return the one active authoritative Observe binding for (policy, repo), or None.

    None means zero matches — a normal ungoverned state. More than one authoritative
    match is an authority conflict, deferred to T4; it fails loud here rather than
    silently selecting a winner.
    """
    matches = [
        binding
        for binding in bindings
        if binding.get("evaluation_role") == EvaluationRole.AUTHORITATIVE.value
        and binding.get("enforcement_mode") == EnforcementMode.OBSERVE.value
        and binding.get("policy") == policy["id"]
        and _binding_active(binding, evaluation_timestamp)
        and _scope_matches(binding.get("scope"), repo)
    ]
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]
    raise NotImplementedError(
        "authority conflict (more than one authoritative binding) is ticket T4"
    )


def evaluate_policy(policy: dict[str, Any], repo: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a governed pair: per-requirement findings plus aggregated outcomes."""
    findings = [_evaluate_requirement(policy["id"], repo, req) for req in policy["requirements"]]
    policy_outcome, coverage_state = _aggregate(findings)
    return {
        "findings": findings,
        "policy_outcome": policy_outcome.value,
        "coverage_state": coverage_state.value,
    }


def _binding_active(binding: dict[str, Any], timestamp: str) -> bool:
    # Half-open [effective_start, effective_end); ISO-8601 UTC strings order chronologically.
    start = binding.get("effective_start")
    end = binding.get("effective_end")
    return (start is None or start <= timestamp) and (end is None or timestamp < end)


def _scope_matches(scope: Any, repo: dict[str, Any]) -> bool:
    condition = _single_equals(scope, "attribute", "scope expression")
    return repo.get(condition["attribute"]) == condition["value"]


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
