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

### Implementation Level

- Status: The adjacent-page retrieval change is implemented, tested, and compared against normal retrieval with the live model (one run each).
- What changed:
  - `app/retrieval.py`: After vector search, append the immediately preceding and following pages for each match, using the page order from `load_pages()`.
  - Keep all vector matches first and in rank order. Add each page at most once, and only add neighbors from the same document.
  - Mark added pages with `retrieval_role: "adjacent_context"`; their text and citation metadata are included.
  - `app/tools.py`: Explain to the model that search results include adjacent context and distinguish those pages from vector matches.
  - No index rebuild is needed because the source text and embeddings were not changed.
- Focused validation: `uv run pytest -q tests/test_retrieval.py tests/test_build_rag_index.py` — **4 passed**.
- Real-materials smoke test: Searching around `lec02-main-p052` included `lec02-main-p051` and `lec02-main-p053` as adjacent context. This verifies the page metadata expansion, not answer quality.
- Comparison question and conditions: Use the same LoRA/QLoRA question, model (`gemini-3.5-flash-lite`), bundled database, and `RAG_TOP_K=5` as the earlier vector-search exercise.
- Results:
  - Baseline before this implementation: the Basic-level run recorded 10.87 seconds, 2,759 input tokens, 165 output tokens, 2 model responses, and estimated generation API cost of $0.001240.
  - After implementation (same question, model, and `RAG_TOP_K=5`; run by me with `uv run python -m app.agent --trace ...`): the agent made 1 call, `search_materials({'query': 'LoRA freeze train QLoRA add'})`, and cited Lecture 02 pp. 51–52.

| Metric | Normal retrieval | With adjacent pages | Change |
|---|---|---|---|
| Answer correctness | Correct | Correct (LoRA freezes the base weights W and trains low-rank A and B; QLoRA adds 4-bit compression of the base weights) | No change |
| Cited pages | lec02-main-p051, lec02-main-p052 | Lecture 02 pp. 51–52 | No change |
| Tool calls / model responses | 1 / 2 | 1 / 2 | No change |
| Time (seconds) | 10.87 | 5.10 | −5.77 (single runs; latency varies) |
| Input / output tokens | 2,759 / 165 | 8,073 / 161 | Input about 2.9x |
| Estimated generation API cost (USD) | $0.001240 | $0.002824 | About 2.3x |

- Evidence added and unnecessary information: This question is fully answered by p.52 (with p.51), which normal retrieval already returned, so the adjacent pages added no evidence the answer needed. They increased input by about 5,300 tokens. The tool-return line in the trace is truncated, so I did not inspect exactly which neighbors were added in this run.
- Observations and limitations:
  - Adjacent pages can add relevant context when an explanation continues across page boundaries, but this single-page question did not show that benefit.
  - They add text and increased input tokens and cost even when the neighboring pages were not useful.
  - Overlapping neighborhoods are deduplicated, but adding context can still increase the number of pages substantially when several vector hits are far apart (up to 5 hits plus 2 neighbors each).
  - The time difference should not be credited to the change: API latency varies between runs, and the earlier top-k test showed similar variation.
  - Remaining failure/next step: test a multi-page question (for example the Lecture 03 compaction vs. memory question, `lec03-main-p013`, `p039`, `p040`), where neighbors might supply missing evidence, and consider adding neighbors only for the top 1–2 hits to limit token growth.

### Advanced Level

- Level attempted: Advanced (the Basic and Implementation entries above are additional work, not required).
- Question (multi-page, evidence across sections): "In the Lecture 03 examples, how does compaction differ from memory across sessions? Do all daily notes go into long-term memory?" Expected evidence: `lec03-main-p013`, `lec03-main-p039`, `lec03-main-p040`.
- Problem with the existing Graph mode: it expands from the top 3 vector hits through `next_page` and `mentions` (shared term) edges, then picks extra pages by hop count and term rarity, not by relevance to the question. Shared terms do not guarantee a page answers the question.
- Design (`--graph-ranked`, "graph for recall, embeddings for precision"):
  - Data and storage: unchanged. `graph.json` (page and term nodes; `next_page` and `mentions` edges used for traversal) and the existing `index.sqlite3` page embeddings. No index rebuild and no extra API calls (the query is embedded once).
  - Retrieval: embed the query once; take the top 3 vector hits as seeds; expand up to 2 hops through adjacent pages and shared terms with no early cut-off; look up the stored distance from the query to every candidate page; keep the candidates closest to the query (seeds plus expanded, at most 10 pages).
  - Why: the graph can reach pages that are not near the question in embedding space (a graph test confirms `p039` and `p040` are reachable from `p013` in 2 hops via the `memory` term), and ranking by embedding distance should keep the relevant ones and drop pages that merely share a term.
  - Code: `app/retrieval.py` (`vector_hits`, `page_distances`, `expand_graph`, `graph_seeds`, `rank_by_distance`, `search_graph_ranked`; existing `search` and `search_graph` behavior kept), `app/tools.py` (`search_graph_ranked`), `app/agent.py` (`--graph-ranked` and instructions), `tests/test_retrieval.py` (2 tests). Full test suite: 25 passed.
- Comparison conditions: same question, model (`gemini-3.5-flash-lite`), and bundled database; one run each. Basic RAG is the default vector search, which includes the adjacent-page change from the Implementation level. The model wrote its own search query each time, so the queries were not identical.

| Method | Search query chosen by the model | Answer correct? | Cited evidence | Time (s) | Input / output tokens | Model responses | Cost (USD) |
|---|---|---|---|---|---|---|---|
| Basic RAG (`search_materials`) | `compaction memory across sessions daily notes long-term memory` | Yes | translated PDF pp. 38–39, 39, 40, 65 | 9.95 | 7,468 / 248 | 2 | $0.001762 |
| Graph (`search_graph`) | `Lecture 03 compaction memory across sessions daily notes long-term memory` | Yes | "Slide 39 and Slide 40" (no page citation labels) | 10.51 | 4,693 / 276 | 2 | $0.002098 |
| Graph ranked (`search_graph_ranked`) | `compaction memory daily notes long term memory Lecture 03` | Yes | none given | 11.23 | 4,682 / 219 | 2 | $0.001952 |

- Results: all three answers were correct and substantively the same: compaction summarizes history within a session, memory persists across sessions in external storage, and not all daily notes go to long-term memory (OpenClaw nightly review keeps only what passes a threshold; one-off lookups stay in daily notes).
- What did not improve: the new method did not give a better answer, better evidence, or lower time/cost than the original Graph. Input tokens (4,682 vs 4,693) and time are within normal run-to-run variation. Compared with basic RAG it used fewer input tokens (about 37% fewer) but had a slightly higher cost and time here, so I cannot credit the ranking for any gain; part of the token difference may come from basic RAG returning adjacent pages.
- Failure observed: the graph-ranked answer gave no page citations, although the instructions require them. Graph answered with slide numbers only. Basic RAG gave the clearest page-level citations.
- Limits of this comparison: one run per method, different model-chosen queries (basic RAG and graph-ranked both seeded from `lec03-main-p065`, while Graph seeded from `p039`), and the trace truncates the tool return, so I did not inspect which expanded pages were returned or whether `p013` was retrieved. This question may simply be easy enough that every method succeeds.
- Would I adopt it? Not on this evidence. It is a small, low-cost change (no extra API calls), but it showed no measurable benefit. Before adopting it I would test questions where basic vector search misses a page (for example evidence only reachable through a shared term), print the returned page IDs and distances, and repeat each method several times with a fixed query.
- Verified by me: ran all three commands above and read the answers and usage lines; the earlier offline tests passed. What I did not verify: the contents of the tool returns, or the ranking quality of the expanded pages.
