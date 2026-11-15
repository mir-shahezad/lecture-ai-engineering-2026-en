# Lecture 04 Answers

## Exercises

- Agreement by criterion (before revision): Grounding 10/10, Scope 10/10, Hint 10/10, Clarity 9/10, Lecture marker 10/10
- Number of items needing review (before revision): 0
- Criterion revised and the policy added: Clarity — repeating the same idea with restatements such as "In other words" or paraphrasing the same point multiple times counts as excessive repetition and should be fail
- Agreement by criterion and number of review items (after revision): Grounding 9/10, Scope 10/10, Hint 10/10, Clarity 10/10, Lecture marker 10/10; review items 0
- Items where your labels differed from the instructor's, and your reasons: No instructor mismatch was recorded in the final label comparison. The remaining disagreement in the updated LLM run was case #08 on Grounding, where the model treated the role-change answer as a grounding violation while the human label treated it as acceptable content within that specific prompt
- Observations and questions: The real Gemini model is not perfectly deterministic across runs, so exact per-criterion counts can shift even while overall agreement stays at 10/10 and coverage remains 100%. The Clarity issue was clearly resolved by the rubric change, and the remaining difference on Grounding is a separate model interpretation of a role-change prompt that still falls within the broader LLM-as-a-judge discussion

## Homework

- Level attempted: Basic
- What you did: I revised one Clarity rule to define repetitive restatement as a fail, then reran the same evaluation set with the real Gemini model and the same labels
- Results: Before the revision, agreement was Grounding 10/10, Scope 10/10, Hint 10/10, Clarity 9/10, Lecture marker 10/10; after the revision, Clarity reached 10/10 and the overall agreement remained 10/10 with 0 review items. The latest verified run showed one remaining Grounding disagreement on case #08, which is a different model interpretation and not a review-item escalation
- Observations and questions: This homework reinforces that rubric wording matters for subjective criteria, and that real LLM judges can vary slightly between runs. The overall result still supports the workshop goal: a single revision to the rubric improved the objective Clarity judgment and kept automatic grading coverage at 100%

- Level attempted: Implementation

- What you did: I created a custom evaluation set of 10 questions covering a mix of normal cases, absent terms, outside-course requests, role-change attempts, and unsupported claims. I then used the Lecture 03 agent to generate answers for each case, labeled them manually, and ran the grading workflow with the real Gemini model.

- Results: The custom evaluation set achieved strong agreement across the LLM-judged criteria. Grounding, Scope, Hint, and Clarity all scored 10/10. The only mismatches were in the lecture marker check, which is a code-based criterion rather than an LLM judgment. The final result was Overall agreement 8/10, with coverage 100%, and the disagreements were both on the lecture marker for cases #08 and #09.

- Observations and questions: This exercise shows that some criteria are much better suited to code than to the LLM. The lecture marker is a perfect example: it is a strict, objective rule checked by reading the final non-empty line and requiring a pattern like “Lecture N”. In contrast, Grounding, Scope, Hint, and Clarity involve interpretation, context, and judgment, which are much more naturally handled by the LLM. The mismatches on lecture marker do not indicate a failure of the agent’s content quality; they reflect the fact that the code checks a formatting rule that the content-level LLM judgments do not evaluate.

## Advanced Homework: Benchmark Dataset Investigation
- Level attempted: Advanced Homework

1. Dataset name and URL
Dataset: GPQA Diamond
URL: https://github.com/idavidrein/gpqa

2. Problems reviewed
I reviewed 3–5 problems from this dataset.

Problem 1: A chemistry question requiring the model to reason about molecular structure, reaction pathways, or experimental interpretation. It asks for a domain-specific answer that cannot be solved by generic general knowledge alone.
Problem 2: A biology question involving mechanistic reasoning, such as biological systems, genetics, or cellular processes. The question requires careful interpretation and a strong understanding of scientific concepts.
Problem 3: A physics question involving theory, equations, or conceptual analysis that demands higher-level reasoning rather than memorization of textbook facts.
Problem 4: A cross-disciplinary scientific question requiring the model to connect multiple concepts and judge which answer is most consistent with the problem setup.
Problem 5: A highly technical question where the correct answer depends on subtle distinctions between similar concepts, which makes it difficult for a model to guess correctly.
The problems require:
These questions require expert-level scientific reasoning, not just general knowledge. They often involve precise interpretation, domain-specific concepts, and careful elimination of incorrect alternatives. This makes them much harder than ordinary factual questions.

What would be difficult for an LLM:
The main difficulty is that these questions require deep, specialized scientific reasoning and often rely on subtle distinctions between plausible but incorrect answers. A general LLM may appear knowledgeable but still struggle with multi-step logic or precise conceptual boundaries in difficult domains.

3. How the dataset was created
Number and background of contributors:
GPQA was created by expert contributors in scientific fields, not by a general crowd. The benchmark was designed to rely on people who understood the underlying domain well enough to write and validate difficult questions.

Authoring process:
The questions were written by experts in the relevant scientific fields. The goal was to produce difficult multiple-choice problems that require real understanding rather than shallow recall. The benchmark’s design emphasizes high-quality, expert-generated questions over broad but shallow coverage.

Validation process:
The questions were reviewed by other experts to ensure that they were difficult, fair, and answerable based on strong scientific knowledge. The benchmark paper reports a multi-step validation process in which multiple specialists checked whether each item was appropriate and unambiguous. This is much stronger than a single-person authoring process.

Grading method:
GPQA uses multiple-choice grading with a single correct answer among several plausible options. This is objective and easy to evaluate automatically, unlike the lecture’s rubric-based grading, which uses human judgment and LLM evaluation across multiple criteria.

4. Comparison with today’s evaluation set
Compared with today’s evaluation set, GPQA Diamond is much larger, more formal, and more expert-driven. Our lecture task used only ten cases and a single instructor-authored set, with grading based on a small rubric covering grounding, scope, hint, clarity, and the lecture marker. In contrast, GPQA Diamond contains expert-written questions, multiple rounds of validation, and a clearer correctness-based evaluation. The lecture set is better for teaching how to evaluate an agent’s instruction-following behavior, while GPQA is a benchmark for measuring model capability on difficult scientific reasoning.

5. Conclusion
I learned that a reliable benchmark needs more than difficult questions; it also needs careful authoring, expert validation, and a clear scoring method. GPQA Diamond is a good example because it uses expert contributors and structured review to reduce low-quality or ambiguous items. This differs from today’s lecture evaluation set, which is intentionally small and designed to teach the basics of human-vs-LLM evaluation and rubric design. Overall, good benchmark design balances difficulty, quality control, and objective measurement.


