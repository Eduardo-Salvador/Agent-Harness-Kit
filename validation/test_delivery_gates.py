import copy
import json
import tempfile
import unittest
from pathlib import Path

from agent_harness_kit.scheduler import schedule_ready
from agent_harness_kit.state_runtime import IllegalTransitionError, transition_task_graph
from tools.validate import validate_graph
from validation.test_readiness_validation import node


def milestone():
    result = node('DEMO', status='completed')
    result.update(acceptance_revision=1, product_review={
        'status': 'pending', 'reviewed_revision': 1,
        'approved_by': None, 'decision_ref': None, 'evidence': ['demo:local'],
    })
    return result


def approval(task):
    task['product_review'].update(status='approved', approved_by='human:client', decision_ref='decision:1')


def verified_task():
    result = node('BUILD', status='active')
    result.update(acceptance_revision=1, test_strategy='tdd', runtime_smoke_required=True,
                  verification={
        'spec_revision': 1,
        'tdd': {
            'red': {'command': 'pytest -k flow', 'exit_code': 1, 'failure_kind': 'behavior', 'evidence': 'run:red', 'sequence': 1},
            'implementation_sequence': 2,
            'green': {'command': 'pytest -k flow', 'exit_code': 0, 'evidence': 'run:green', 'sequence': 3},
        },
        'runtime_smoke': {'command': 'run controlled cycle', 'exit_code': 0, 'evidence': 'run:smoke',
                          'expected': 'one result, explicit failure state', 'observed': 'one result, error surfaced'},
    })
    return result


class DeliveryGateTests(unittest.TestCase):
    def graph(self):
        downstream = node('EXPAND', depends_on=['DEMO'])
        downstream['product_requires'] = ['DEMO']
        return {'revision': 1, 'nodes': [milestone(), downstream, node('INDEPENDENT')]}

    def test_pending_product_review_blocks_only_affected_work(self):
        plan = schedule_ready(self.graph(), capacity=3)
        self.assertEqual(plan['selected'], ['INDEPENDENT'])
        self.assertIn({'id': 'EXPAND', 'reason': 'product-review:DEMO'}, plan['deferred'])

    def test_technical_acceptance_does_not_substitute_for_client_approval(self):
        graph = self.graph()
        graph['nodes'][0]['assurance_status'] = 'accepted'
        self.assertNotIn('EXPAND', schedule_ready(graph, capacity=3)['selected'])

    def test_explicit_current_human_approval_unlocks_work(self):
        graph = self.graph()
        approval(graph['nodes'][0])
        self.assertIn('EXPAND', schedule_ready(graph, capacity=3)['selected'])
        self.assertEqual(validate_graph(graph, 'test'), [])

    def test_stale_agent_empty_or_rejected_approval_never_unlocks_work(self):
        for mutation in ({'reviewed_revision': 0}, {'approved_by': 'agent:reviewer'},
                         {'approved_by': 'human:'}, {'decision_ref': ''},
                         {'evidence': []}, {'status': 'changes-requested'}, {'status': 'rejected'}):
            with self.subTest(mutation=mutation):
                graph = self.graph()
                approval(graph['nodes'][0])
                graph['nodes'][0]['product_review'].update(mutation)
                self.assertNotIn('EXPAND', schedule_ready(graph, capacity=3)['selected'])

    def test_missing_milestone_fails_closed(self):
        graph = self.graph()
        graph['nodes'][1]['depends_on'] = []
        graph['nodes'][1]['product_requires'] = ['MISSING']
        self.assertNotIn('EXPAND', schedule_ready(graph, capacity=3)['selected'])
        self.assertTrue(any('product' in error for error in validate_graph(graph, 'test')))

    def test_false_ready_and_active_are_rejected_by_validator(self):
        for status in ('ready', 'active'):
            graph = self.graph()
            graph['nodes'][1]['status'] = status
            self.assertTrue(any('product-review' in error for error in validate_graph(graph, 'test')))

    def test_product_requirement_must_be_a_dependency(self):
        graph = self.graph()
        approval(graph['nodes'][0])
        graph['nodes'][1]['depends_on'] = []
        self.assertTrue(any('product-dependency' in error for error in validate_graph(graph, 'test')))

    def transition(self, graph, task, status, markdown=False):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / ('graph.md' if markdown else 'graph.json')
            raw = json.dumps(graph)
            if markdown:
                raw = '---\nrevision: 1\n---\n\n```json\n' + raw + '\n```\n'
            path.write_text(raw, encoding='utf-8')
            try:
                return transition_task_graph(path, task, status, 1, 'role:orchestrator', 'ctx')
            except IllegalTransitionError:
                self.assertEqual(path.read_text(encoding='utf-8'), raw)
                raise

    def test_runtime_cannot_bypass_product_gate_in_json_or_markdown(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown), self.assertRaises(IllegalTransitionError):
                self.transition(self.graph(), 'EXPAND', 'active', markdown)

    def test_runtime_can_activate_after_product_approval(self):
        graph = self.graph()
        approval(graph['nodes'][0])
        self.transition(graph, 'EXPAND', 'active')

    def test_complete_requires_tdd_and_affected_flow_evidence(self):
        original = verified_task()
        cases = []
        for key in ('tdd', 'runtime_smoke'):
            task = copy.deepcopy(original)
            del task['verification'][key]
            cases.append(task)
        task = copy.deepcopy(original)
        task['verification']['tdd']['red']['failure_kind'] = 'environment'
        cases.append(task)
        task = copy.deepcopy(original)
        task['verification']['tdd']['implementation_sequence'] = 0
        cases.append(task)
        task = copy.deepcopy(original)
        task['verification']['tdd']['green']['command'] = 'different test'
        cases.append(task)
        task = copy.deepcopy(original)
        task['verification']['runtime_smoke']['exit_code'] = 1
        cases.append(task)
        task = copy.deepcopy(original)
        task['verification']['spec_revision'] = 0
        cases.append(task)
        for task in cases:
            for markdown in (False, True):
                with self.subTest(verification=task['verification'], markdown=markdown), self.assertRaises(IllegalTransitionError):
                    self.transition({'revision': 1, 'nodes': [task]}, 'BUILD', 'completed', markdown)

    def test_complete_accepts_proportional_evidence(self):
        for markdown in (False, True):
            self.transition({'revision': 1, 'nodes': [verified_task()]}, 'BUILD', 'completed', markdown)

    def test_validator_rejects_false_completed_without_required_evidence(self):
        task = verified_task()
        task['status'] = 'completed'
        del task['verification']['tdd']
        self.assertTrue(any('completion-evidence' in error for error in validate_graph({'nodes': [task]}, 'test')))

    def test_small_legacy_task_does_not_require_product_review(self):
        self.assertEqual(schedule_ready({'nodes': [node('SMALL')]}, capacity=1)['selected'], ['SMALL'])

    def test_all_completion_conditions_need_current_observed_evidence(self):
        task = verified_task()
        task['acceptance_criteria'] = [
            {'id': 'AC-1', 'condition': 'a real cycle returns only matching results'},
            {'id': 'AC-2', 'condition': 'upstream failure is visible'},
        ]
        for checks in ([], [{'criterion': 'AC-1', 'result': 'passed', 'observed': 'one matching result', 'evidence': 'run:1'}],
                       [{'criterion': 'AC-1', 'result': 'failed', 'observed': 'wrong match', 'evidence': 'run:1'}]):
            task['verification']['acceptance'] = checks
            with self.subTest(checks=checks), self.assertRaises(IllegalTransitionError):
                self.transition({'revision': 1, 'nodes': [task]}, 'BUILD', 'completed')
        task['verification']['acceptance'] = [
            {'criterion': 'AC-1', 'result': 'passed', 'observed': 'one matching result', 'evidence': 'run:1'},
            {'criterion': 'AC-2', 'result': 'passed', 'observed': 'failure surfaced', 'evidence': 'run:2'},
        ]
        self.transition({'revision': 1, 'nodes': [task]}, 'BUILD', 'completed')

    def test_invalid_conditions_or_empty_success_evidence_fail_closed(self):
        for criteria in ([], None, ['done'], [{'id': 'A', 'condition': ''}],
                         [{'id': 'A', 'condition': 'works'}, {'id': 'A', 'condition': 'different'}]):
            task = verified_task()
            task['acceptance_criteria'] = criteria
            with self.subTest(criteria=criteria), self.assertRaises(IllegalTransitionError):
                self.transition({'revision': 1, 'nodes': [task]}, 'BUILD', 'completed')

    def test_legacy_table_cannot_bypass_executable_gates(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'graph.md'
            raw = '---\nrevision: 1\n---\n\n| ID | Status |\n| --- | --- |\n| T | ready |\n'
            path.write_text(raw, encoding='utf-8')
            with self.assertRaisesRegex(IllegalTransitionError, 'executable JSON'):
                transition_task_graph(path, 'T', 'active', 1, 'actor', 'ctx')
            self.assertEqual(path.read_text(encoding='utf-8'), raw)

    def test_task_dictionary_uses_same_product_gate(self):
        graph = self.graph()
        graph['tasks'] = {task['id']: task for task in graph.pop('nodes')}
        with self.assertRaises(IllegalTransitionError):
            self.transition(graph, 'EXPAND', 'active')
        approval(graph['tasks']['DEMO'])
        self.transition(graph, 'EXPAND', 'active')

    def test_malformed_and_stale_evidence_mutations(self):
        for field, value in (('test_strategy', []), ('test_strategy', 'TDD'), ('runtime_smoke_required', 'yes')):
            task = verified_task()
            task[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(IllegalTransitionError):
                self.transition({'revision': 1, 'nodes': [task]}, 'BUILD', 'completed')
        for value in (None, 'DEMO', {}, [None], [{}]):
            graph = self.graph()
            graph['nodes'][1]['product_requires'] = value
            self.assertNotIn('EXPAND', schedule_ready(graph, capacity=3)['selected'])
        for mutation in ({'result': 'failed'}, {'evidence': ''}, {'observed': ''}, {'criterion': 'OTHER'}):
            task = verified_task()
            task['acceptance_criteria'] = [{'id': 'A', 'condition': 'only matching result'}]
            check = {'criterion': 'A', 'result': 'passed', 'observed': 'matching result', 'evidence': 'run:1'}
            check.update(mutation)
            task['verification']['acceptance'] = [check]
            with self.subTest(mutation=mutation), self.assertRaises(IllegalTransitionError):
                self.transition({'revision': 1, 'nodes': [task]}, 'BUILD', 'completed')

    def test_invalid_completed_evidence_cannot_unlock_dependency(self):
        task = verified_task()
        task['status'] = 'completed'
        del task['verification']['tdd']
        graph = {'nodes': [task, node('NEXT', depends_on=['BUILD'])]}
        self.assertEqual(schedule_ready(graph, capacity=2)['selected'], [])

    def test_open_feature_scope_cannot_be_scheduled_or_started(self):
        for scope in ('needs-discovery', 'unknown', None):
            task = node('OPEN')
            task['scope_status'] = scope
            graph = {'revision': 1, 'nodes': [task]}
            self.assertEqual(schedule_ready(graph, capacity=1)['selected'], [])
            self.assertTrue(any('scope' in error for error in validate_graph(graph, 'test')))
            with self.assertRaises(IllegalTransitionError):
                self.transition(graph, 'OPEN', 'active')
        task['scope_status'] = 'approved'
        self.assertEqual(schedule_ready(graph, capacity=1)['selected'], ['OPEN'])


if __name__ == '__main__':
    unittest.main()
