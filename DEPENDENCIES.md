# Dependency inventory

Static inventory of `saveinstance.luau`, checked 2026-11-27. This document records source availability, not runtime compatibility or security certification.

| Dependency | Availability | Notes |
| --- | --- | --- |
| SomeHub / UniversalMethodFinder | Archived under `modules/SomeHub/` | Original upstream unavailable; archived copy already referenced by the entrypoint. |
| SomeHub / StreamBuffer and RequireOnlineModule | Archived under `modules/SomeHub/` | Not directly referenced by the inspected entrypoint. |
| Base64 (daily3014/rbx-cryptography) | Archived under `modules/Base64/` and connected as a fallback | The entrypoint prefers Roblox EncodingService, then the archived codec pinned to commit `7bd2ab46ae2a900490426b2152cc811c0c4f512b`, then the existing encoder. Each candidate is checked against known Base64 vectors. Runtime compatibility remains unverified. |
| Roblox Client Tracker Mini-API-Dump | Public file available | Version-dependent metadata; no license for redistribution of the dump verified in this audit. Not mirrored. |
| Roblox CDN deployment history / full API dumps | Dynamic endpoints | Runtime availability and version matching not verified. |
| Konstant V2.1 | Public file observed | Optional third-party executable decompiler; not mirrored or reviewed for redistribution rights. |
| RoProxy asset delivery | External service | Runtime availability and authorization not verified. |
| Original UniversalSynSaveInstance | Upstream unavailable | Do not substitute leaked sources. Preserve author attribution and verify licenses before redistribution. |

## Security and completeness

Use only with projects you own or are authorized to export. Public asset identifiers do not establish access rights. An offline source archive does not restore missing geometry or repair a malformed XML export. Do not execute unreviewed remote code or upload private game resources.

Roblox Studio's native place/model export is the authoritative backup workflow for authorized projects. Validate XML and compare class counts, references and available geometry against an authorized original before relying on any alternative export.
