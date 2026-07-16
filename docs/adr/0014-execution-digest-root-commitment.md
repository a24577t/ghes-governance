---
status: accepted
---

# Execution Digest: a versioned root commitment to an Execution's evidence

ADR-0009 lists "content hashes and execution digest" among the contents of Authoritative Evidence, but never defines what an Execution Digest is. The term appears nowhere else in the repository — not in `CONTEXT.md`, not in the Domain Model, not in any other ADR. A specification cannot supply the definition, because the term is architectural. This ADR defines it. It reverses nothing in ADR-0009, adds no capability, and introduces no closed set.

## Decision

**The Execution Digest is the deterministic root commitment to an Execution's Authoritative Evidence**: one value per Execution that commits to every evidence item the Execution published, such that any change beneath it is detectable.

The digest is **versioned**, and its computation version is recorded wherever the digest is recorded, so that a verifier knows how to recompute it. This mirrors the versioning the platform already applies to evidence schemas (ADR-0009) and evaluation strategies (ADR-0012).

**Version 1 computes the Execution Digest as the canonical content hash of the Execution Manifest**, using the same hash function and canonical serialization as every other evidence item. **v1 is the only supported computation**; the engine release declares which digest versions it supports, and an unsupported version is never silently substituted.

Version 1 names a value ADR-0009's model already implies rather than adding machinery. ADR-0009 establishes the Execution Manifest as the tamper-evidence root (`CONTEXT.md`, Execution Manifest) and anticipates "external digest **anchoring**" as a production hardening step — anchoring presupposes exactly one value per Execution that commits to everything beneath it. The manifest already lists every evidence item with its content hash, so hashing the manifest transitively commits to every item.

## Where the digest lives

**The Execution Digest is never stored inside the Execution Manifest it commits to.** A manifest containing its own hash is self-referential and does not converge.

Where it *is* recorded — evidence-store metadata such as the manifest's filename, a value returned at publication, an external anchor, or a sidecar record — is a deployment and specification concern, not an architectural one. This ADR fixes only that the location is outside the manifest.

## Verification

A verifier recomputes the digest from the Execution Manifest under the recorded computation version and compares it to the recorded or anchored digest.

**If they differ, verification fails and the evidence set is tamper-suspect.** The engine does not designate either value as the trustworthy one: a mismatch establishes that something beneath the commitment changed, not *what* changed. Treating the manifest as automatically authoritative would assume the manifest is the innocent party, which is precisely what a mismatch leaves undetermined. Uncertainty never grants privilege (Principle 3, Invariant 2) — and a tamper-suspect evidence set is exactly such an uncertainty, so it resolves to a loud failure, never to a trusted answer.

## Considered options

**Defining the digest as a fixed computation** — "the Execution Digest *is* the manifest content hash", with no version seam — was considered and rejected. It welds today's cheapest correct computation to the concept's identity. Any future hardening would then either redefine an accepted architectural term or migrate every stored digest, and RD 3 of the Phase 2 plan forbids evidence-schema migration. The abstraction costs one version field and preserves the seam.

**A Merkle root over evidence items, now** was considered and rejected as v1. It would enable efficient partial proofs — verifying one item without the whole manifest — which nothing in the model currently consumes, and ADR-0009 defers evidence hardening to production ("signing, WORM/object lock, external anchoring"). Under this ADR a Merkle root remains available as a **future digest version** rather than a retrofit: the abstraction is what makes deferring it cheap instead of expensive.

**A digest computed over the ordered list of item content hashes** was considered and rejected as v1: it commits to the items but not to the manifest's own metadata — schema version, execution identity, completeness accounting — so two Executions differing only in that metadata could share a digest.

**A separate first-class digest evidence item** was considered and rejected: it regresses — whatever hashes the digest item then needs its own protection.

## Consequences

- **The tamper-evidence root becomes verifiable.** Previously nothing hashed the manifest: item hashes live *in* the manifest, so a coherently modified manifest verifies against itself. The verification chain is now Execution Digest → Execution Manifest → evidence items, and manifest tampering is detectable rather than self-consistent.
- `CONTEXT.md` gains an **Execution Digest** entry; the Domain Model's evidence entities reference it.
- Implementations that publish Authoritative Evidence must record the Execution Digest outside the Execution Manifest and verify it during evidence validation, before Derived Reports are generated.
- Production anchoring (ADR-0009) has a defined value to anchor and a version to anchor it under.
- The digest is derived, not authored: it is recomputable from the manifest at any time and is never an independent authority. It adds a commitment over evidence; it never becomes a second source of truth about it.
