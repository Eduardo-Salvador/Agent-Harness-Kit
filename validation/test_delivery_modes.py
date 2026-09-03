import contextlib
import io
import json
import unittest
from unittest.mock import patch

from agent_harness_kit.cli import main
from agent_harness_kit.readiness import completion_blocker, readiness_blocker


class DeliveryModeTests(unittest.TestCase):
    def resolve(self, *arguments):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(['delivery-mode', *arguments]), 0)
        return json.loads(output.getvalue())

    def test_default_is_accompanied_with_meaningful_checkpoints(self):
        result = self.resolve()
        self.assertEqual(result['preset'], 'accompanied')
        self.assertEqual(result['mode'], 'delivery')
        self.assertEqual(result['interaction'], 'accompanied')
        self.assertEqual(result['client_checkpoints'], ['first-usable-slice', 'material-capabilities'])

    def test_autonomous_keeps_scope_checks_and_parallel_capability(self):
        result = self.resolve('autonomous')
        self.assertEqual(result['interaction'], 'continuous')
        self.assertEqual(result['mode'], 'delivery')
        self.assertEqual(result['client_checkpoints'], [])
        self.assertEqual(result['scope_policy'], 'approved-envelope')
        self.assertEqual(result['verification'], 'required')
        self.assertEqual(result['parallelism'], 'host-capability')

    def test_hackathon_keeps_first_demo_evaluation(self):
        result = self.resolve('hackathon')
        self.assertEqual(result['mode'], 'hackathon')
        self.assertEqual(result['interaction'], 'accompanied')
        self.assertEqual(result['client_checkpoints'], ['first-demo'])
        self.assertEqual(result['scope_policy'], 'timeboxed-demo')

    def test_inspection_does_not_install_or_activate_learning(self):
        with patch('agent_harness_kit.cli.installer_module', side_effect=AssertionError('must not install')):
            for preset in ('accompanied', 'autonomous', 'hackathon'):
                result = self.resolve(preset)
                self.assertEqual(result['schema'], 'harness.delivery-mode/v1')
                self.assertFalse(result['applies_changes'])
                self.assertEqual(result['learning_activation'], 'unchanged')

    def test_mode_does_not_bypass_existing_scope_product_or_completion_gates(self):
        for preset in ('accompanied', 'autonomous', 'hackathon'):
            policy = self.resolve(preset)
            self.assertIsNotNone(readiness_blocker({'delivery_preset': policy['preset'], 'scope_status': 'needs-discovery'}, {}))
            self.assertIsNotNone(readiness_blocker({'delivery_preset': policy['preset'], 'depends_on': ['DEMO'], 'product_requires': ['DEMO']}, {'DEMO': {'status': 'completed'}}))
            self.assertIsNotNone(completion_blocker({'delivery_preset': policy['preset'], 'test_strategy': 'tdd'}))

    def test_unknown_preset_fails_without_falling_back(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            main(['delivery-mode', 'anything-goes'])
        self.assertEqual(caught.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
