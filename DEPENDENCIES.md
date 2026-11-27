# Dependency inventory

Static inventory of `saveinstance.luau` at commit `1f582e24f05a16977ae9dd940e73abc0c2eb31db`, checked 2026-11-27. This document records source availability, not runtime compatibility or security certification.

| Dependency | Availability | Notes |
| --- | --- | --- |
| SomeHub / UniversalMethodFinder | Archived under `modules/SomeHub/` | Original upstream unavailable; archived copy already referenced by the entrypoint. |
| SomeHub / StreamBuffer and RequireOnlineModule | Archived under `modules/SomeHub/` | Not directly referenced by the inspected entrypoint. |
| Base64 (daily3014/rbx-cryptography) | Archived under `modules/Base64/` | Upstream legacy branch exists; the old main-branch URL in the existing entrypoint is unavailable. No entrypoint change in this archival commit. |
| Roblox Client Tracker Mini-API-Dump | Public file available | Version-dependent metadata; no license for redistribution of the dump verified in this audit. Not mirrored. |
| Roblox CDN deployment history / full API dumps | Dynamic endpoints | Runtime availability and version matching not verified. |
| Konstant V2.1 | Public file observed | Optional third-party executable decompiler; not mirrored or reviewed for redistribution rights. |
| RoProxy asset delivery | External service | Runtime availability and authorization not verified. |
| Original UniversalSynSaveInstance | Upstream unavailable | Do not substitute leaked sources. Preserve author attribution and verify licenses before redistribution. |

## Security and completeness

Use only with projects you own or are authorized to export. Public asset identifiers do not establish access rights. An offline source archive does not restore missing geometry or repair a malformed XML export. Do not execute unreviewed remote code or upload private game resources.

Roblox Studio's native place/model export is the authoritative backup workflow for authorized projects. Validate XML and compare class counts, references and available geometry against an authorized original before relying on any alternative export.
