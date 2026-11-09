from __future__ import annotations

import unittest

from coda.prompts import read_prompt_file


class TestAgentRoleBoundaries(unittest.TestCase):
    def test_context_agent_is_evidence_preparation_only(self) -> None:
        prompt = read_prompt_file("context_system_prompt.txt")

        self.assertIn("organize grounded context", prompt)
        self.assertIn("do not receive the current codebook", prompt.casefold())

    def test_coders_stop_at_evidence_near_provisional_coding(self) -> None:
        for filename in (
            "coder_system_prompt.txt",
            "initial_coder_system_prompt.txt",
        ):
            prompt = read_prompt_file(filename)
            normalized = " ".join(prompt.split())

            self.assertIn("provisional-coding level only", normalized)
            self.assertIn("minimum sufficient abstraction", normalized)
            self.assertNotIn("express a mid-level analytic concept", normalized)

    def test_induction_owns_initial_category_construction(self) -> None:
        prompt = " ".join(read_prompt_file("induction_system_prompt.txt").split())

        self.assertIn("observation-level analytical notes", prompt)
        self.assertIn("transition from those evidence-near observations", prompt)
        self.assertIn("does not require a one-to-one codebook entry", prompt)

    def test_comparison_owns_iterative_mapping_and_change_proposals(self) -> None:
        prompt = " ".join(read_prompt_file("comparison_system_prompt.txt").split())

        self.assertIn("sole iterative-stage agent", prompt)
        self.assertIn("map their evidence-near concepts", prompt)
        self.assertIn("do not automatically turn every provisional label", prompt)

    def test_validation_checks_risk_without_recoding(self) -> None:
        prompt = " ".join(read_prompt_file("validation_system_prompt.txt").split())

        self.assertIn("not to recode the artifact", prompt)
        self.assertIn("do not normalize coder labels", prompt)
        self.assertIn("without silently replacing them", prompt)


if __name__ == "__main__":
    unittest.main()
