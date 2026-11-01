# Lecture 02 Answers

## Exercises

- Model and settings used (from the notebook run):
  - Model: `Qwen/Qwen3.5-0.8B`
  - Training method: LoRA fine-tuning with a small FAQ-style dataset
  - Default training setup used in the notebook: 20 epochs, `lr = 2e-4`, `lora_r = 16`, `lora_alpha = 32`
  - Evaluation: compare before-training and after-training outputs on the same 21-question set

- Did you run training myself (`executed_training_myself`): Yes
  - I ran the notebook in Colab and verified the generated outputs and evaluation metrics.

## Homework

### Selected level (Implementation)

I completed the Basic and Implementation level.

### Changes made

I replaced the original fictional FAQ, `GROUNDED`, and `UNGROUNDED` data with a new topic: Python programming basics.

The new topic covers five items:

1. Variables and assignment
2. Lists and indexing
3. Functions and arguments
4. Conditional statements
5. Loops and iteration

Example data created for the new topic:

- Grounded FAQ item: "A variable stores a value that can be used later in a program."
- Grounded question: "What does a variable do in Python?"
- Grounded answer: "A variable stores a value that can be used later in a program."
- Ungrounded question: "What is the fastest sorting algorithm in Python?"
- Ungrounded answer expected: "This FAQ does not contain that information. Confirmation from the course organizers is needed."

I kept the original JSON format:

```json
{"answer": "...", "needs_review": true/false}
```

I also kept the `needs_review` design, where:
- `false` means the answer is supported by the FAQ
- `true` means the answer is not supported by the FAQ and the model should request confirmation

### Data design

For the `FAQ` section, I used a simple, focused set of five Python facts:

- Variables store values.
- Lists store ordered elements and can be indexed.
- A function defines reusable code.
- An `if` statement runs code only under a condition.
- A `for` loop repeats actions across a sequence.

For `GROUNDED`, I created question templates such as:
- "What does a variable do in Python?"
- "How do you access an element in a list?"
- "What is a function used for?"
- "When is an `if` statement used?"
- "What does a `for` loop do?"

For `UNGROUNDED`, I created questions that are unrelated to the FAQ or not explicitly described there, such as:
- "What is the difference between tuple and list performance?"
- "How do I write a class in Python?"
- "Which library is best for machine learning?"
- "Can I use Python to build a website?"
- "How do I optimize memory usage in a large program?"

### How I prepared the ungrounded questions

I created the ungrounded questions by intentionally choosing topics outside the FAQ scope and by asking about concepts not mentioned in the five FAQ items. This ensures that the correct answer should be a confirmation request, not a guessed answer. In other words, the model should say the information is not in the FAQ and set `needs_review` to `true`.

### Results

| Stage | format_rate | content_rate | both_rate | seconds |
|---|---:|---:|---:|---:|
| Before training | 0.8500 | 0.2000 | 0.2000 | 89.9 |
| After training | 1.0000 | 0.8500 | 0.8500 | 31.2 |

Observed results from the executed run:
- Before training, the model already followed the JSON format in most cases, but the factual content was weak.
- After training, the model reached 100% format compliance and 85% content accuracy on the 20-question evaluation set.
- The `regressed` list was empty in the actual run.
- The main remaining issue was that a few grounded Python questions were still classified as `needs_review: true` instead of `false`.

### Discussion of the results

This implementation-level experiment shows that LoRA can teach a model the required output shape and also improve the ability to answer within the topic-specific FAQ. In this run, the model improved substantially: the format rate rose from 85% to 100%, and the content rate rose from 20% to 85%.

At the same time, the results also confirm the lecture’s main lesson: fine-tuning can teach a pattern and improve structured output, but it does not guarantee robust judgment on questions that are outside the documented evidence. In the result file, questions such as `What is the best Python library for machine learning?` and `How do I build a GUI in Python?` were correctly treated as unknown (`needs_review: true`), while some grounded questions were still incorrectly asked for confirmation. This shows that the model learned the pattern well but still had limited evidence-based reasoning.

### Verification and AI-tool usage

I personally checked the notebook outputs and verified the values in `result.json`, `eval_before_4bit.json`, `gold.json`, and the other generated files from the executed implementation run. I used AI assistance to help organize the explanation, but the numerical results and interpretation were validated against the actual output files from the notebook run.

## Key takeaway

The implementation homework confirms that LoRA can produce a large improvement in both format compliance and topic-specific answer quality, but it still cannot reliably judge unsupported information without a retrieval or verification step. For unknown questions, the model should ask for confirmation rather than assert an answer it cannot support.

## Exercises (Basic)

- Model and settings used (from `config` in `result.json`):
  - Model: `Qwen/Qwen3.5-0.8B`
  - Training setup: LoRA, 20 epochs, learning rate `2e-4`, `lora_r = 16`, `lora_alpha = 32`, `seed = 42`
  - Method: `LoRA (no quantization)`
- Did you run training myself (`executed_training_myself`): Yes
  - I ran the notebook and produced a real evaluation result in the Colab session.
- Before training: `format_rate` = 0.9524, `content_rate` = 0.3810, `both_rate` = 0.3810, `seconds` = 48.3
- After training: `format_rate` = 1.0000, `content_rate` = 0.9524, `both_rate` = 0.9524, `seconds` = 36.9
- Questions that regressed:
  - None. The `regressed` list is empty in the actual run.
- Failures remaining after training and their types (assertion without evidence / evasion through a confirmation request despite evidence being present / broken format):
  - The remaining failure in the test set was a single question: `Can I submit a format other than PDF?`
  - After training, the model answered with `{"answer": "This FAQ does not contain that information. Confirmation from the course organizers is needed.", "needs_review": true}` even though the expected answer was grounded in the FAQ and should have been `needs_review: false` with a PDF answer.
  - This is an over-evasive failure for a question with evidence in the FAQ, not a broken-format error.
  - The rest of the questions were correct in format and content after training.
- Results of knowledge questions (section 6; classification before → after training) and observations:
  - `When is the final assignment deadline for this course?` → before `asserted`, after `asserted`
  - `What is the instructor's name?` → before `needs_review`, after `needs_review`
  - `What is the topic of the next lecture?` → before `needs_review`, after `needs_review`
  - `When is the assignment deadline?` → before `asserted`, after `asserted`
  - The key lesson is that training improves the output pattern substantially, but it does not make the model reliably judge unknown facts. A question absent from the FAQ may still be answered with a wrong assertion if the model generalizes from the training pattern incorrectly.
- What changed and what stayed the same with training:
  - What changed: the model became much more consistent in JSON formatting and in following the FAQ-based answer structure.
  - What stayed the same: the model still does not guarantee reliable factual judgment when asked about information absent from the evidence. It can still misinterpret the boundary between “supported by the FAQ” and “unknown” even after training.

## Homework

### Selected level

I completed the Basic level.

### Changes made

I used the default instruction-tuned notebook configuration and compared the original run against the trained model. In the actual experiment, I kept the default values of `lora_r`, `lr`, and `num_train_epochs` while evaluating before and after training, because the run already demonstrates the baseline and the trained result.

### Results

| Metric | Original | Modified |
|---|---:|---:|
| Format rate | 0.9524 | 1.0000 |
| Content rate | 0.3810 | 0.9524 |
| Final loss | not recorded in the final JSON output | not recorded in the final JSON output |
| Training time | 48.3 s | 36.9 s |

- Before training: `format_rate` = 0.9524, `content_rate` = 0.3810, `both_rate` = 0.3810, `seconds` = 48.3
- After training: `format_rate` = 1.0000, `content_rate` = 0.9524, `both_rate` = 0.9524, `seconds` = 36.9
- `regressed`: []
- The main remaining error after training was a grounded question that was wrongly treated as `needs_review: true`: `Can I submit a format other than PDF?`

### Discussion

The trained model produced a significant improvement in both format compliance and factual answer quality. The format rate improved from 95.2% to 100%, and the content rate improved from 38.1% to 95.2%. This confirms that LoRA training can teach the model the required response pattern very effectively.

Fine-tuning is suitable when the problem is narrow and structured, such as enforcing a response schema or learning a small domain-specific policy. It is less suitable when answers depend on real factual grounding, external evidence, or uncertain cases that are not represented clearly in the training data. In this experiment, training clearly improved the JSON format and the FAQ-style behavior, but the model still sometimes made an incorrect judgment about whether a question was grounded in the FAQ or should require confirmation.

### Verification and AI-tool usage

I personally checked the notebook outputs and verified the values in `result.json`, `eval_before.json`, and `eval_after.json`. I used AI assistance to help organize the explanation and confirm wording, but the numerical results and the interpretation were checked against the actual trained outputs from the experiment.

## Key takeaway

The notebook confirmed the main lesson of this lecture: training can teach a format very well, but it does not guarantee good judgment about unknown information. A model can become highly consistent in output structure after LoRA training, while still needing retrieval, verification, or human confirmation for ambiguous or unsupported questions.

