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
