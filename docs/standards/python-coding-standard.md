# Python Coding Standard

| Field | Value |
|---|---|
| **Status** | **Adopted** (PR #17) — authoritative. Adoption occurred **on merge of its governance PR to `main`** (the `RequirePR` mechanism), which has happened. See "Adoption & binding" below. |
| **Applies to** | Python under `src/` and `tests/` in `ghes-governance` |
| **Normative keywords** | MUST / MUST NOT / SHOULD / SHOULD NOT / MAY, per RFC 2119 |
| **Referenced by** | `engineering-standards.md` (Python spoke); `code-review` skill Standards axis; `codebase-design` |
| **Authoritative sources** | `CONTEXT.md`; ADRs 0003, 0005, 0009, 0014; `docs/specifications/vertical-slice-1-observe-mode-tracer.md`; `.ai/methodology/`; `.claude/skills/tdd/` |

**Origin legend** — **Authority** (already required by an authoritative source) · **Convention** (consistent in T0, adopted here as policy) · **Decision** (a deliberate choice) · **Deferred** (recorded, not yet standardized).

**Enforcement stages** — **Document**: authoritative, review-enforced. **Warn**: automated, non-blocking. **Require**: automated, merge-blocking. Stage is *current → target* where they differ.

**In force now:** domain vocabulary (§3), deterministic serialization (§10), execution-integrity discipline (§5/§10), public-seam discipline (§5/§12). Red-before-green (§12) is in force from **T1 onward**. Ruff (§2), mypy (§4), CodeQL and Dependency Review (§13/§15) progress document → warn → require as a separate tooling ticket establishes a clean baseline.

**Adoption & binding.** The repository's governance mechanism for durable change is a merged PR to `main` (`RequirePR`); this standard is authoritative on that merge. T1 begins only **after** the refresh PR merges (governance-first sequencing), so the standard is authoritative when T1 starts — "in force now" above takes effect on adoption. Independently, the test *shape* — seam-only testing, no internal-module imports, golden-evidence (§5/§12) — is **already** authoritative via the approved Vertical Slice 1 specification's Testing Decisions; §12 adds the red-before-green process required from T1.

---

## 1. Supported Python version
Code MUST target **Python 3.12** minimum; `pyproject.toml` keeps `requires-python = ">=3.12"`. "Supported" MUST mean **only interpreter versions exercised by CI** — `>=3.12` is an install floor, not a forward-compatibility promise. New post-3.12 features MUST NOT be used until CI's minimum is raised.
*Origin: Authority. Stage: Document → Require (CI matrix).*

## 2. Formatting and linting
**Ruff** MUST be the single formatter and linter; Black and a separate isort config MUST NOT be introduced. Line length MUST be **100**. Ruff defaults SHOULD be retained; deviations MUST be justified in config and reviewed.
*Origin: Decision. Stage: Document → Warn → Require (tooling ticket).*

## 3. Naming and repository vocabulary
PEP 8 casing MUST hold (snake_case functions/modules, PascalCase classes, UPPER_SNAKE_CASE constants). Domain identifiers MUST use `CONTEXT.md` vocabulary **verbatim** and honor its `_Avoid_` list.
*Origin: casing Convention; vocabulary Authority. Stage: casing Document → Warn; **vocabulary Document (in force)**.*

## 4. Type annotations and type-checker strictness
Public signatures under `src/` MUST be fully annotated; modules MUST use `from __future__ import annotations`. **mypy** MUST be adopted; `src/` MUST pass a **strict** profile with explicit, narrow, justified exceptions. Every `# type: ignore` MUST carry a specific error code and a justification where non-obvious. `tests/` MAY relax strictness but MUST remain meaningfully typed.
*Origin: annotations Convention; strictness Decision. Stage: Document → Warn → Require (tooling ticket).*

## 5. Module and package organization, and public seams
The `src/` layout MUST be retained; each module SHOULD hold one responsibility. Vertical Slice 1's **public seams are exactly two**: Execution boundary (`run_execution`) and Report Derivation (`derive_reports`); no lower public seam MAY be introduced within the slice. The execution-integrity chain (canonical serialization → item hashing → Execution Manifest → external Execution Digest → verify-before-derive) is **frozen and content-agnostic**: code MUST route new evidence types through it without redefining it, introducing new types complete-with-degenerate-values in the ticket that first produces them. Operational-log records MUST stay outside that contract.
*Origin: Authority. Stage: **Document/Require (in force)**.*

## 6. Dataclasses and immutability
Immutable value objects SHOULD be `@dataclass(frozen=True)`. Immutability MUST NOT be a blanket rule on all classes.
*Origin: Convention (scope Decision). Stage: Document.*

## 7. Enums and closed sets
Engine-owned **textual closed sets** MUST be `enum.StrEnum`; no artifact outside the engine MAY extend them. Serialized enum **values** are **stable artifact-contract values**; changing one is a breaking change. Existing T0 enums (`str, Enum`) MUST NOT be migrated for conformity except via a behavior-preserving adoption ticket that proves serialized output and content hashes are unchanged.
*Origin: closed-set Authority; StrEnum Decision. Stage: Document.*

## 8. Exception design and boundary translation
Domain errors MUST form an explicit hierarchy under one base engine error. Translation of stdlib/OS/third-party exceptions into domain errors is **mandatory** at these boundaries: public API (seams), persistence, providers, parsing, external I/O; the original cause MUST be chained (`raise ... from exc`). Programmer errors and unexpected invariant defects MUST NOT be caught and translated into routine domain failures. The T6 duplicate-Execution-Identifier `FileExistsError` remains deferred.
*Origin: hierarchy Convention + Authority (P3); translation Decision. Stage: Document → Require.*

## 9. Filesystem access
`pathlib.Path` MUST be used for path representation and normal bounded file operations. Built-in `open()` MAY be used where a file object is genuinely required (streaming, atomic write/replace, explicit encoding/newline control, or integration with an API that consumes a file object). Intent over blanket ban.
*Origin: Convention. Stage: Document → Warn (Ruff `PTH`).*

## 10. Deterministic serialization and I/O discipline
All governed/evidence content MUST serialize through the **single canonical serializer** (sorted keys, stable separators, UTF-8; no floats/NaN). Content hashes MUST be over canonical bytes; the Execution Digest MUST commit to the manifest from outside it. **Core evaluation MUST be deterministic and free of undeclared I/O** — no wall-clock reads during evaluation (timestamp/identifier injected); network access MUST be confined to explicit provider/adapter boundaries and replaced by controlled fixtures or fakes in deterministic tests.
*Origin: Authority (ADR-0009/0014/0005; AC 2/9). Stage: **Require (in force)** via determinism/evidence-independence tests.*

## 11. Logging and Operational Logs *(deferred)*
A logging coding standard is **deferred**; T0's absence of logging MUST NOT be codified as a "no logging" policy. When Operational Logs are implemented they MUST follow ADR-0009 (closed severity model, evidence identical across levels, sensitivity classification, no secrets/tokens).
*Origin: Deferred (future Authority). Stage: Document (deferred).*

## 12. Testing and Red-Green-Refactor
From **T1 onward**, work MUST be developed **red-before-green**: a failing test at a confirmed seam first, then minimal implementation, one slice at a time; refactoring is a review-stage activity. Tests MUST use the **narrowest public or owned contract for the behavior under test** — internal or artifact-level seams are valid when they own that contract, but MUST NOT be side channels for higher-level semantics a public seam already owns. Tests MUST be integration-style with no internal mocks; expected values MUST come from an independent source (spec/fixture literal). Standing invariant tests (determinism, tamper detection, traceability, read-only, uncertainty-never-grants-privilege) MUST be maintained.
*Origin: Authority (tdd skill; spec doctrine; adopted). Stage: **Document now; Require from T1**.*

## 13. Dependencies and pinning
Direct dependencies MUST be declared in `pyproject.toml` with intentional constraints. A **committed lockfile** MUST provide reproducible dev/CI/app builds; the environment and lock tooling choice is **deferred to the tooling ticket**. **Dependabot** and **Dependency Review** are part of the target model. Pinning policy MUST NOT be inferred from T0's two-dependency sample.
*Origin: declaration Convention; pinning Decision. Stage: Document → Require (tooling ticket).*

## 14. Documentation and docstrings
Module docstrings are **mandatory**. Public classes/functions MUST carry docstrings **when contract, constraints, side effects, exceptions, or architectural role is not obvious from the signature**. Private-helper docstrings are optional and MUST explain non-obvious rationale, not restate code. Comments MUST state a constraint the code cannot show.
*Origin: Convention + Authority (minimal-documentation). Stage: Document → Warn (Ruff `D`, scoped).*

## 15. Secure coding (CodeQL / GHAS)
Secrets/tokens/credentials MUST NOT appear in source, evidence, or logs. Untrusted input MUST be parsed safely (`yaml.safe_load` only; no `eval`/`exec`; anchored regex). The read-only guarantee (writes confined to evidence/log/report dirs) and §10 I/O discipline MUST hold. The repository MUST **dog-food GitHub security controls** as policy, delivered incrementally in a separate ticket (secret scanning + push protection where available, Dependabot, Dependency Review, CodeQL, least-privilege workflow permissions, governed pinning of third-party Actions). New checks SHOULD establish a clean baseline (document → warn) before becoming merge-blocking.
*Origin: no-secrets/safe-parsing/read-only Authority; GHAS enablement Decision. Stage: Document → Warn → Require (GHAS ticket).*

---

## 16. Verification & enforcement matrix

| § | Rule area | Origin | Level | Verification | Stage |
|---|---|---|---|---|---|
| 1 | Python 3.12+ (CI-defined support) | Authority | MUST | build config, CI matrix | Document → Require |
| 2 | Ruff format + lint, 100 cols | Decision | MUST | Ruff | Document → Warn → Require |
| 3 | CONTEXT.md vocabulary / PEP 8 casing | Authority / Convention | MUST | review / Ruff `N` | **Document (in force)** / Document → Warn |
| 4 | Public typing; mypy strict (`src/`) | Conv/Decision | MUST | mypy, Ruff `ANN` | Document → Warn → Require |
| 5 | Two seams; frozen integrity contract | Authority | MUST | review + tests | **Document/Require (in force)** |
| 6 | Frozen dataclasses for value objects | Convention | SHOULD | review | Document |
| 7 | `StrEnum`; serialized values are contract | Auth/Decision | MUST | review + tests | Document |
| 8 | Domain exception translation at boundaries | Auth/Decision | MUST | review + tests | Document → Require |
| 9 | pathlib for paths; `open()` by intent | Convention | MUST/MAY | Ruff `PTH`, review | Document → Warn |
| 10 | Canonical serialization; deterministic I/O | Authority | MUST | tests (AC 2/9) | **Require (in force)** |
| 11 | Logging | Deferred | — | (future) review + GHAS | Document (deferred) |
| 12 | Red-before-green; narrowest owning contract | Authority | MUST | review, coverage (later) | **Document; Require from T1** |
| 13 | Deps in pyproject; committed lockfile | Conv/Decision | MUST | Dependency Review | Document → Require |
| 14 | Module docstrings; public-when-non-obvious | Conv/Auth | MUST/SHOULD | Ruff `D`, review | Document → Warn |
| 15 | No secrets; safe parsing; read-only; GHAS | Auth/Decision | MUST | GHAS, review, tests | Document → Warn → Require |

## 17. Deferred items
- Logging standard (§11) — until Operational Logs exist.
- Environment & lock tooling (§13) — chosen in the tooling ticket.
- Tooling installation & CI (§2/§4/§13/§15) — Ruff, mypy, coverage, CodeQL, Dependency Review, Dependabot, workflow permissions: policy here, installation in a separate ticket.
- T6 exception translation (§8); T0 enum migration (§7).
