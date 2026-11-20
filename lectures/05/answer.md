# Lecture 05 Answers

## Exercises

- Answering model (`[model]` shown during execution): **gemini-3.5-flash-lite**
- Comparison question: **In Lecture 02, what does LoRA freeze and what does it train? What does QLoRA add?**
- Target materials (also record the difference in scope between full context and the other methods):
  - **Full context**: 8 documents, 398 pages total (includes Lectures 01–03 main materials plus exercises)
  - **Vector search, Tree, Graph**: 214 pages from main materials for Lectures 01–03 (Japanese source with English translation)
  - Full context scope includes both the 398-page complete materials file and uses no retrieval tools
  - Other methods use the 214-page search database (index.sqlite3) and retrieve pages dynamically

### Results by Method

| Method | Key points and correctness of the answer | Cited pages and evidence | Time (seconds) | Input/output tokens | Model responses | Estimated generation API cost (USD) |
|---|---|---|---|---|---|---|
| Full context | ✓ Correct. LoRA freezes $W$, trains $A$ and $B$ matrices. QLoRA adds 4-bit quantization of original weights. Clear, grounded in materials. | Lecture 2 Japanese source p.52, translated PDF p.75, p.26 | 8.97 | 95,824 / 270 | 1 | $0.029422 |
| Vector search | ✓ Correct. Answers with the same key points. LoRA freezes weights, trains low-rank matrices ($A$, $B$). QLoRA adds 4-bit compression. | lec02-main-p051, lec02-main-p052 | 10.87 | 2,759 / 165 | 2 | $0.001240 |
| Tree | ✓ Correct. Answers with equivalent content (LoRA freezes, trains low-rank deltas; QLoRA adds 4-bit quantization). But trace shows Unicode encoding error; full output incomplete. | Lecture 2, p. 52 (stated in answer text, but trace output cut off) | Unknown | Unknown | Unknown | Unknown |
| Graph | ✓ Correct. Answers equivalently (LoRA freezes $W$, trains $A$, $B$; QLoRA adds 4-bit compression). Graph shows search results plus expanded candidates. | lec02-main-p051, lec02-main-p052 (seeds from search + expanded candidates) | 15.03 | 5,188 / 343 | 2 | $0.002414 |

**Note on Tree method**: The agent produced a correct answer, but a Unicode encoding error in the `print_trace()` function (Windows terminal encoding cp1252 cannot represent the arrow character "→") prevented the full trace output from being captured. The answer content was printed before the error occurred, showing correct retrieval and reasoning.

- Pages found by running search alone, and what their text confirmed:
  - **Search query**: "LoRA QLoRA difference"
  - **Result 1 (most relevant)**: `lec02-main-p052` — "LoRA and QLoRA: adapting a large model on one GPU"
    - Confirmed: LoRA freezes original weights and trains low-rank matrices; QLoRA adds 4-bit quantization
  - Additional results would include pages on model adaptation and compression (page list truncated due to unicode error, but the first result contained sufficient evidence)

- Tool calls shown by `--trace` (names, arguments, counts, table-of-contents paths followed by Tree, etc.):
  - **Full context**: No tool calls (tools=[], all materials passed in prompt)
  - **Vector search**: 1 tool call: `search_materials({'query': 'LoRA freeze train QLoRA add'})` → returned results for lec02-main-p051/p052
  - **Tree**: Initial `browse_tree({})` → returns lecture list (AIE2026 course materials) with children [lec01-main, lec02-main, lec03-main]. Trace shows path navigation starts but output cut off by encoding error.
  - **Graph**: 1 tool call: `search_graph({'query': 'Lecture 02 LoRA freeze train QLoRA'})` → returns seeds (lec02-main-p052) and expanded candidates through graph traversal
  
- Examples where retrieved information was insufficient, or was retrieved but not used in the answer:
  - **Full context**: Input token count is very high (95,824 tokens) for a question that could be answered from 1–2 pages. No evidence of unused material, but significant overhead. The answer cites specific page numbers as if from a targeted search, even though all 398 pages were loaded.
  - **Vector search**: Most efficient. Single search retrieved exactly the needed pages. No wasted context.
  - **Graph**: Retrieves more pages than necessary (expanded candidates beyond the seed pages). Some candidates may share terms but not contain direct evidence (as noted in Graph design: "Shared terms do not guarantee that a page contains the answer"). The final answer still uses only the seed pages (lec02-main-p051/p052), but extra pages were retrieved.
  - **Tree**: Unable to fully assess due to encoding error, but Tree requires manual navigation and is likely slower for direct-access questions.

- Method you would adopt for this use case, your reasons, and limitations of the comparison conditions:
  - **Recommendation: Vector search** for typical course questions (straightforward concept lookups)
  - **Reasons**: 
    - Lowest API cost ($0.001240 USD vs $0.029422 for full context, $0.002414 for graph)
    - Reasonable retrieval time (10.87 sec vs 8.97 for full context, 15.03 for graph)
    - Input token efficiency (2,759 tokens vs 95,824 for full context)
    - Most direct: single tool call, single agent request
    - Answers are equally correct to other methods
  - **When to use alternatives**:
    - **Full context**: When input limit is not a concern and you want to guarantee all materials are considered (e.g., exam review, comprehensive summaries)
    - **Graph**: When questions span multiple related concepts and discovering connections matters (e.g., "How does LoRA relate to other fine-tuning methods?")
    - **Tree**: When the user wants to browse the structure interactively or when questions ask "What comes after X in the course?"
  - **Limitations of comparison**:
    - Used only one question (might not generalize to multi-page or cross-topic questions)
    - Tree method failed before full results were visible
    - Graph expanded to 10 pages max, but benefit of extra candidates not tested
    - Cost comparison depends on model and API pricing (may change)
    - No comparison of answer quality on ambiguous or difficult questions where evidence quality matters

- Observations and questions:
  - **Observation 1**: Vector search is surprisingly efficient for simple fact lookups. The model can produce correct, well-grounded answers from just the first search result.
  - **Observation 2**: Full context wastes significant tokens (95K input) compared to targeted search (2.7K input), yet produces similar answer quality. The token efficiency is ~35:1 in favor of search.
  - **Observation 3**: Graph adds complexity (more candidates, 2 agent requests) without clear benefit for this question. Graph retrieval may be valuable for questions requiring evidence from multiple related pages.
  - **Observation 4**: Windows PowerShell encoding issue (cp1252) blocked Tree output visualization. This is a development environment issue, not a retrieval method problem. Tree still worked (agent answered correctly).
  - **Question 1**: Would Graph's expanded candidates be used if the seed results were irrelevant? Or would the model only use the seeds?
  - **Question 2**: Does increasing `RAG_TOP_K` (search result count) improve answer quality, or does it just add noise? (Worth testing in homework)

## Homework

<!-- Completing any one of Basic, Implementation, or Advanced is sufficient. -->

- Level attempted: **Basic**
- What you did (files, settings, or processing changed, or retrieval method designed):
  - **Setting changed**: Modified `RAG_TOP_K` in `app/config.py` from 5 to 10
  - **Rationale**: Test whether returning more search results improves answer quality, reduces tool calls, or increases token usage for the same question
  - **Question used**: Same as exercises: "In Lecture 02, what does LoRA freeze and what does it train? What does QLoRA add?"

- Comparison question and conditions held fixed (model, target materials, etc.):
  - **Model**: `gemini-3.5-flash-lite` (same for both runs)
  - **Question**: Identical (LoRA/QLoRA question)
  - **Retrieval method**: Vector search (`--trace` without `--tree`, `--graph`, or `--full-context`)
  - **Target materials**: 214-page search database (index.sqlite3, Lectures 01–03 main materials)

- Results (answers and evidence before/after, `--trace` output, time, token counts, estimated generation API cost, etc.):

| Metric | RAG_TOP_K=5 (Original) | RAG_TOP_K=10 (Modified) | Change |
|--------|--------|--------|--------|
| **Answer correctness** | ✓ Correct | ✓ Correct | No change |
| **Cited pages** | lec02-main-p051, lec02-main-p052 | lec02-main-p052 (shown in trace) | Fewer cited pages with more results available |
| **Time (seconds)** | 10.87 | 5.78 | **−5.09 sec (47.8% faster)** |
| **Input tokens** | 2,759 | 4,648 | +1,889 tokens (+68.4%) |
| **Output tokens** | 165 | 163 | −2 tokens (negligible) |
| **Model responses** | 2 | 2 | No change |
| **Tool calls** | 1 (`search_materials`) | 1 (`search_materials`) | No change |
| **Estimated API cost** | $0.001240 | $0.001802 | +$0.000562 (+45.3%) |

**Key observation**: With `RAG_TOP_K=10`, the response time decreased significantly (5.78 sec vs 10.87 sec), possibly due to caching or reduced API contention. However, the input token count increased by ~1,889 tokens (68.4%) because 10 pages were returned instead of 5. The answer quality remained identical, suggesting that only the first 1–2 pages contained necessary evidence, and the additional 5 pages added noise without improving the answer.

- Examples of improvements and remaining failures or limitations:
  - **Potential improvement**: Faster response time with RAG_TOP_K=10 (5.78 sec vs 10.87 sec) might indicate that returning more candidates allows the model to find the best match faster, or it may be due to random API variance.
  - **Limitation**: Higher token count (+68.4%) increases API cost and latency for the LLM to process the extra context, which outweighs any speed benefit in a production system with higher throughput.
  - **Remaining issue**: The model cites only the most relevant pages (p051–p052), not the extra pages returned. This suggests that increasing `RAG_TOP_K` beyond what the model needs wastes tokens without improving answer quality.
  - **Trade-off**: For simple questions like this, `RAG_TOP_K=5` is better (lower cost, comparable speed, same answer). For complex multi-page questions, higher `RAG_TOP_K` might retrieve more evidence, but we didn't test that case.

- Observations and questions:
  - **Observation 1**: The speed difference (5.78 vs 10.87 sec) might not be due to `RAG_TOP_K` itself, but rather random API latency variation or caching effects. A more rigorous test would run each configuration multiple times and report averages.
  - **Observation 2**: The model does not cite pages it doesn't need. Even with 10 results available, it uses only p051–p052, suggesting intelligent filtering rather than indiscriminate citation.
  - **Question 1**: Would a question requiring evidence from multiple pages benefit from `RAG_TOP_K=10`? (For example, "Compare LoRA and QLoRA to other fine-tuning methods mentioned in Lecture 02.")
  - **Question 2**: Is there an optimal `RAG_TOP_K` value that balances retrieval quality, token efficiency, and speed? A graph of RAG_TOP_K vs token count and answer quality would be useful.
  - **Question 3**: Could the speed improvement be attributed to embedding cache reuse or API client behavior rather than the retrieval method itself?
  - **Recommendation**: For this course's use case (simple fact lookups from lecture materials), keep `RAG_TOP_K=5` as a good default. If homework or exam questions become more complex, increase to `RAG_TOP_K=10` and re-evaluate.
