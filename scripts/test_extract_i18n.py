import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from extract_i18n import extract, infer_locale, iter_files, parse_properties, walk_strings


class ExtractionTests(unittest.TestCase):
    def test_nested_json_and_array_flattening(self):
        self.assertEqual(
            list(walk_strings({"form": {"save": "Save"}, "items": ["One", 3], "n": 2})),
            [("form.save", "Save"), ("items[0]", "One")],
        )

    def test_arb_metadata_is_skipped(self):
        self.assertEqual(list(walk_strings({"title": "Title", "@title": {"description": "meta"}})),
                         [("title", "Title")])

    def test_properties_parser(self):
        parsed = parse_properties("# comment\nhello=Hello\\ world\ncolon: value\ncontinued=multi\\\n  line\nflag\n")
        self.assertEqual(parsed["hello"], "Hello world")
        self.assertEqual(parsed["colon"], "value")
        self.assertEqual(parsed["continued"], "multiline")
        self.assertEqual(parsed["flag"], "")

    def test_locale_inference_and_explicit_override(self):
        self.assertEqual(infer_locale(Path("locales/en-US/common.json")), "en-US")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / "locales" / "en-US" / "common.json"
            file.parent.mkdir(parents=True)
            file.write_text(json.dumps({"save": "Save", "debug.internal": "hidden"}), encoding="utf-8")
            rows = extract([file], root, "fr-CA", None, None)
            self.assertEqual(rows[0]["locale"], "fr-CA")
            self.assertEqual(rows[0]["source_file"], "locales/en-US/common.json")

    def test_key_filtering(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "en.json"
            file.write_text('{"button.save":"Save","debug":"debug"}', encoding="utf-8")
            rows = extract([file], None, None, None, __import__("re").compile(r"debug"))
            self.assertEqual([row["key"] for row in rows], ["button.save"])

    def test_json_yaml_properties_file_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.json").write_text('{"a":"A"}', encoding="utf-8")
            (root / "b.properties").write_text('b=B\n', encoding="utf-8")
            (root / ".private").mkdir()
            (root / ".private" / "secret.json").write_text('{"x":"X"}', encoding="utf-8")
            self.assertEqual({p.name for p in iter_files([root])}, {"a.json", "b.properties"})

    def test_yaml(self):
        try:
            import yaml  # noqa: F401
        except ImportError:
            self.skipTest("PyYAML not installed")
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "en-US.yaml"
            file.write_text("button:\n  save: Save\n", encoding="utf-8")
            self.assertEqual(extract([file], None, None, None, None)[0]["key"], "button.save")

    def test_cli_jsonl_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "en-US" / "common.json"
            source.parent.mkdir()
            source.write_text('{"button":{"save":"Save"}}', encoding="utf-8")
            output = root / "out.jsonl"
            script = Path(__file__).with_name("extract_i18n.py")
            result = subprocess.run(
                [sys.executable, str(script), str(source.parent), "--root", str(root),
                 "--output", str(output)], capture_output=True, text=True, check=True)
            row = json.loads(output.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(row, {"key": "button.save", "locale": "en-US",
                                   "source_file": "en-US/common.json", "text": "Save"})
            self.assertIn("Extracted 1 strings", result.stderr)


if __name__ == "__main__":
    unittest.main()
