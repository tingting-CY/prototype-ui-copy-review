import unittest
from evaluate_outputs import evaluate

class EvaluationTests(unittest.TestCase):
    def test_assertion_semantics(self):
        for assertion, output, expected in [
            ({'check':'regex_all','patterns':['Saved','EN-US']}, 'Saved EN-US', True),
            ({'check':'regex_all','patterns':['Saved','EN-US']}, 'Saved', False),
            ({'check':'regex_any','patterns':['待确认','未知']}, '待确认', True),
            ({'check':'regex_none_all','patterns':['PX-','SPT-']}, 'PX-ENG', False),
            ({'check':'regex_none','pattern':'Pay now'}, '待确认', True),
            ({'check':'distinct_min','pattern':r'COPY-\d+','min':2}, 'COPY-001 COPY-001', False),
            ({'check':'distinct_min','pattern':r'COPY-\d+','min':2}, 'COPY-001 COPY-002', True),
        ]:
            with self.subTest(assertion=assertion):
                self.assertEqual(evaluate(assertion,output),expected)
    def test_unknown_check_rejected(self):
        with self.assertRaises(ValueError):
            evaluate({'check':'unknown'},'Saved')

if __name__ == '__main__':
    unittest.main()

class RuntimeContractTests(unittest.TestCase):
    def test_default_audit_and_locale_contracts(self):
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        template = (root/'references/en-us-prompt-template.md').read_text()
        self.assertNotIn('<dimension_confirmation>', template)
        self.assertNotIn('不执行完整审查', template)
        self.assertIn('不叠加 HF 语言分片', template)
        self.assertIn('实际决定结论', template)
        self.assertIn('`EN-US-`', (root/'references/change-list-schema.md').read_text())
