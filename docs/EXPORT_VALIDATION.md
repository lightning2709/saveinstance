# Offline export validation

Use this workflow for Roblox projects and backups you own or are explicitly authorized to export. The validator only processes local files; it does not execute scripts, fetch assets, access live games or bypass permissions.

## Check an XML file

Requires Python 3. No third-party libraries are needed.

```sh
python tools/validate_xml.py example.rbxlx
```

Reports invalid UTF-8 bytes, characters forbidden by XML 1.0, strict parser errors, object class counts, SharedString references and geometry field observations. Exit code 2 indicates that the original file is invalid or could not be inspected.

To create a separate sanitized copy of an authorized backup:

```sh
python tools/validate_xml.py example.rbxlx --sanitize example-clean.rbxlx
```

Invalid characters are replaced with U+FFFD. This is a lossy text repair, not a geometry recovery or script recovery. The output is only written if strict XML parsing succeeds, and existing files are never overwritten. The original file is not changed. DTDs are rejected.

## Geometry and binary format

Missing or empty MeshData, ChildData, PhysicsData and asset references should be compared against an authorized original. An XML file may omit default values, and a nonempty resource ID does not establish permission to load the resource. The validator does not reconstruct missing geometry.

For a complete backup, use the original project in Roblox Studio and save a local place as .rbxl (binary) or .rbxlx (XML). A valid authorized XML place can also be opened in Studio and saved to the binary format. Native export preserves the data available in the original project; changing file format cannot recover absent content.

## Tests and limitations

```sh
python -m unittest discover -s tests -v
```

Five synthetic tests cover valid SharedString references, malformed UTF-8 and XML characters, malformed markup, DTD rejection and rejection of binary input. These tests do not exercise SaveInstance, Potassium or Xeno. Their runtime compatibility remains unverified.

No user map, asset, script or export report is included in this repository.
