# CODA Prompts

This directory stores role-specific prompt files for the CODA workflow.

Prompt files are kept separate from agent code so that:

- prompt changes do not require editing Python logic;
- multiple agent variants can share the same execution layer;
- later experiments can swap prompt versions without changing the orchestrator.

The current Context, Coder, Induction, Comparison, and Validation system prompts
use the role and task instructions in the paper appendix (`../agentprompts.tex` relative to the `CODA/` source root). Their user
templates retain the runtime JSON contracts, bilingual display fields, and grounded
evidence IDs. They are executable adaptations, not byte-for-byte copies of the
appendix's simplified output schemas.

Induction constructs definitions with `induction_system_prompt.txt`, then applies
them using `induction_assignment_system_prompt.txt` in a separate call. Assignment
inputs include the research question, analytical protocol, and original evidence.
The assignment prompt is included in the initialization checkpoint fingerprint.

Comparison uses separate case comparison, refinement, retrospective, and batch
tasks. `comparison_batch_system_prompt.txt` and
`comparison_impact_system_prompt.txt` supply task-specific runtime contracts.
The independent evaluator prompts belong to outcome evaluation and are unchanged
by the coding-agent appendix adaptation.

`initial_coder_*` and `arbitration_*` are historical compatibility files; the default
pipeline loads `coder_*` and `comparison_*`. Updating a compatibility file alone
does not change the active pipeline.

Prompt changes apply to newly constructed agents. Restart a running backend to
load them. Existing runs with frozen analytical prompts intentionally reject a
different prompt on resume; use a new run for the revised analytical protocol.
