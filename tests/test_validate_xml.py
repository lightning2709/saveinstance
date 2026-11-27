import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from validate_xml import inspect_bytes


class ValidatorTests(unittest.TestCase):
    def test_shared_strings_and_geometry(self):
        report, _ = inspect_bytes(b'<roblox><Item class="UnionOperation"><Properties><SharedString name="MeshData">a</SharedString><SharedString name="PhysicsData">b</SharedString><SharedString name="ChildData">c</SharedString></Properties></Item><SharedStrings><SharedString md5="a">AA==</SharedString><SharedString md5="b"/></SharedStrings></roblox>')
        self.assertTrue(report["valid_xml"])
        fields = report["geometry_fields"]["UnionOperation"]
        self.assertEqual(fields["MeshData"], {"nonempty": 1})
        self.assertEqual(fields["PhysicsData"], {"empty": 1})
        self.assertEqual(fields["ChildData"], {"unresolved": 1})
        self.assertEqual(fields["AssetId"], {"missing": 1})

    def test_normalization(self):
        report, output = inspect_bytes(b'<roblox><Item class="Part"><Properties><string name="Name">x\x80\x01</string></Properties></Item></roblox>')
        self.assertFalse(report["valid_xml"])
        self.assertTrue(report["valid_after_text_normalization"])
        self.assertEqual(report["invalid_utf8_bytes"], 1)
        self.assertEqual(report["forbidden_xml_characters"], 1)
        self.assertTrue(inspect_bytes(output)[0]["valid_xml"])

    def test_malformed_markup(self):
        report, output = inspect_bytes(b'<roblox><Item></roblox>')
        self.assertFalse(report["valid_after_text_normalization"])
        self.assertIsNone(output)

    def test_no_dtd(self):
        report, output = inspect_bytes(b'<!DOCTYPE roblox [<!ENTITY x "test">]><roblox>&x;</roblox>')
        self.assertFalse(report["valid_after_text_normalization"])
        self.assertIsNone(output)

    def test_binary_rejected(self):
        with self.assertRaises(ValueError):
            inspect_bytes(b'<roblox!\x89\xff')


if __name__ == "__main__":
    unittest.main()
