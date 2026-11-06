# Lecture 03 Answers

## Exercises

- Differences between the Lecture 01 (bare LLM) and agent answers:
  - A bare LLM answers directly from pattern completion, while the agent combines model reasoning with tool execution.
  - In the agent version, the model can decide to call `search_glossary` or `get_lecture_summary` before answering.
  - This makes the answer more grounded and less likely to invent course-specific facts.
- Tool calls shown by `--trace` (tool names and arguments):
  - For the course-term question `What is the difference between LoRA and QLoRA?`, the trace shows:
    - `search_glossary({'query': 'LoRA'})`
    - `search_glossary({'query': 'QLoRA'})`
  - The tool result is then used to answer the question with course-grounded definitions.
  - For lecture-content questions, the expected tool is `get_lecture_summary` with the lecture number.
- Number of LLM calls for one question (`requests`):
  - In the trace, one question used 2 tool calls and 2 requests, which means the model made multiple calls to the model/agent loop while using the glossary tool.
  - This is a clear example of the agent pattern: model + loop + tools.
- Tool added and the description in its docstring:
  - For the Basic homework, I did not add a new tool. Instead, I changed one thing at a time and compared the traces.
  - I first removed the glossary-first instruction from `app/agent.py` and saw the answer become more general.
  - Then I changed the wording in the `search_glossary` docstring in `app/tools.py` to test whether the tool description alone affects behavior.

## Homework

- Level attempted: Basic
- What I did:
  1. Kept the original project and ran the same question before changing any code.
  2. Changed only the instruction text in `app/agent.py` by removing the line that said the model should always check the glossary before answering.
  3. Ran the same prompt again and compared the trace and output.
  4. Changed only the `search_glossary` docstring in `app/tools.py` and reran the same question.
- Results:
  - Original behavior: the agent called `search_glossary` for `LoRA` and `QLoRA`, and the answer was grounded in the glossary.
  - After removing the glossary-first instruction: the answer became more general and less clearly grounded. It gave broader guidance and did not strongly emphasize the glossary lookup.
  - After changing the tool docstring: the model still called `search_glossary` twice for the same terms, and the answer stayed grounded. The tool description changed did not visibly change the tool pattern in this case.
- Observations:
  - The instruction layer in `app/agent.py` had the strongest effect on behavior.
  - The tool docstring in `app/tools.py` also matters, but for this question it was weaker than the explicit instruction.
  - The agent still behaved like a real tool-using system: the model chose to call a glossary tool before answering a course-specific concept question.
  - This confirms the main lesson of Lecture 03: a model's behavior depends on the combination of instructions, tool descriptions, and available tools.

### Key takeaway
The Basic assignment showed that changing just one part of the agent setup can change the behavior of the model. In particular, the instruction in `app/agent.py` had a more obvious effect than the wording change in the tool docstring. This demonstrates that agent behavior is driven by the design of the system rather than by the model alone.