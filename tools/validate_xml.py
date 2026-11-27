#!/usr/bin/env python3
"""Validate local Roblox XML backups without executing scripts or fetching assets."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

BAD_UTF8 = re.compile(r"[\udc80-\udcff]")
BAD_XML = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\ufffe\uffff]")
CSG = ("MeshData", "MeshData2", "ChildData", "ChildData2", "PhysicsData", "AssetId")
FIELDS = {name: CSG for name in ("UnionOperation", "IntersectOperation", "NegateOperation", "PartOperation")}
FIELDS["MeshPart"] = ("MeshId", "MeshID", "MeshContent", "PhysicsData", "VertexCount")


class NoDTD(ET.TreeBuilder):
    def doctype(self, name, pubid, system):
        raise ValueError("DTD is not allowed in a Roblox XML backup")


def parse(text):
    root = ET.fromstring(text, parser=ET.XMLParser(target=NoDTD()))
    if root.tag != "roblox":
        raise ValueError("Expected a roblox XML root")
    return root


def inspect_bytes(data):
    if data.startswith(b"<roblox!"):
        raise ValueError("Binary Roblox file; use Studio to save an XML copy")
    text = data.decode("utf-8", errors="surrogateescape")
    utf8_count = len(BAD_UTF8.findall(text))
    xml_count = len(BAD_XML.findall(text))
    clean = BAD_XML.sub("\ufffd", BAD_UTF8.sub("\ufffd", text))
    report = {"bytes": len(data), "invalid_utf8_bytes": utf8_count,
              "forbidden_xml_characters": xml_count, "valid_xml": False}
    try:
        parse(text)
        report["valid_xml"] = not (utf8_count or xml_count)
    except (ValueError, ET.ParseError, UnicodeError) as error:
        report["parse_error"] = str(error)
    try:
        root = parse(clean)
    except (ValueError, ET.ParseError, UnicodeError) as error:
        report["valid_after_text_normalization"] = False
        report["normalization_error"] = str(error)
        return report, None
    report["valid_after_text_normalization"] = True
    report.update(geometry_report(root))
    return report, clean.encode("utf-8")


def geometry_report(root):
    shared = {}
    for entry in root.findall("./SharedStrings/SharedString"):
        key = entry.get("md5")
        if key:
            shared[key] = bool((entry.text or "").strip())
    counts = Counter()
    geometry = {name: {field: Counter() for field in fields} for name, fields in FIELDS.items()}
    shared_refs = Counter()
    for item in root.iter("Item"):
        cls = item.get("class", "(unknown)")
        counts[cls] += 1
        props = item.find("Properties")
        props_by_name = {} if props is None else {p.get("name"): p for p in props}
        for p in props_by_name.values():
            if p.tag == "SharedString":
                key = (p.text or "").strip()
                shared_refs["resolved_nonempty" if shared.get(key) else "resolved_empty" if key in shared else "unresolved"] += 1
        for field, stats in geometry.get(cls, {}).items():
            p = props_by_name.get(field)
            if p is None:
                state = "missing"
            else:
                value = "".join(p.itertext()).strip()
                if p.tag == "SharedString":
                    state = "nonempty" if shared.get(value) else "empty" if value in shared else "unresolved"
                else:
                    state = "empty" if value.lower() in ("", "0", "nil", "null", "rbxassetid://0") else "nonempty"
            stats[state] += 1
    return {"total_items": sum(counts.values()), "class_counts": dict(sorted(counts.items())),
            "shared_string_references": dict(shared_refs),
            "geometry_fields": {cls: {field: dict(stats) for field, stats in fields.items()}
                                for cls, fields in geometry.items() if counts[cls]},
            "note": "Missing and empty fields are observations, not proof of corruption or asset access. No geometry is restored."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--sanitize", type=Path, help="Write a new, validated UTF-8 copy; invalid characters become U+FFFD. Never overwrites.")
    args = parser.parse_args()
    try:
        report, clean = inspect_bytes(args.file.read_bytes())
        if args.sanitize:
            if clean is None:
                raise ValueError("Text normalization cannot repair this XML; no output written")
            with args.sanitize.open("xb") as out:
                out.write(clean)
            report["sanitized_copy"] = str(args.sanitize)
        print(json.dumps(report, indent=2, ensure_ascii=True))
        return 0 if report["valid_xml"] or (args.sanitize and clean is not None) else 2
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
