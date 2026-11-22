from app.retrieval import expand_graph, include_adjacent_pages, rank_by_distance


def test_rank_by_distance_orders_by_similarity_and_drops_unindexed_pages():
    candidates = [{"page_id": "a"}, {"page_id": "b"}, {"page_id": "c"}]

    ranked = rank_by_distance(candidates, {"a": 0.5, "b": 0.1}, limit=5)

    assert [page["page_id"] for page in ranked] == ["b", "a"]
    assert ranked[0]["distance"] == 0.1
    assert [page["page_id"] for page in rank_by_distance(candidates, {"a": 0.5, "b": 0.1}, limit=1)] == ["b"]


def test_graph_reaches_example_pages_through_shared_term():
    seed = {"page_id": "lec03-main-p013", "distance": 0.1}

    seeds, candidates = expand_graph([seed])

    reached = {page["page_id"]: page for page in candidates}
    assert seeds[0]["page_id"] == "lec03-main-p013"
    assert {"lec03-main-p039", "lec03-main-p040"} <= reached.keys()
    assert reached["lec03-main-p039"]["hops"] == 2


def test_include_adjacent_pages_keeps_hits_and_deduplicates_context():
    pages = [
        {"page_id": "lec01-p001", "document_id": "lec01", "page": 1, "content": "first"},
        {"page_id": "lec01-p002", "document_id": "lec01", "page": 2, "content": "second"},
        {"page_id": "lec01-p003", "document_id": "lec01", "page": 3, "content": "third"},
        {"page_id": "lec02-p001", "document_id": "lec02", "page": 1, "content": "other document"},
    ]
    results = [
        {**pages[1], "distance": 0.1},
        {**pages[2], "distance": 0.2},
    ]

    expanded = include_adjacent_pages(results, pages)

    assert [page["page_id"] for page in expanded] == [
        "lec01-p002", "lec01-p003", "lec01-p001",
    ]
    assert [page["page_id"] for page in expanded[:2]] == [
        result["page_id"] for result in results
    ]
    assert expanded[2]["content"] == "first"
    assert expanded[2]["retrieval_role"] == "adjacent_context"
    assert len({page["page_id"] for page in expanded}) == len(expanded)


def test_include_adjacent_pages_does_not_cross_documents_or_add_missing_hits():
    pages = [
        {"page_id": "lec01-p001", "document_id": "lec01", "page": 1, "content": "first"},
        {"page_id": "lec02-p001", "document_id": "lec02", "page": 1, "content": "other"},
    ]
    results = [
        {**pages[0], "distance": 0.1},
        {"page_id": "missing", "document_id": "lec03", "distance": 0.2},
    ]

    expanded = include_adjacent_pages(results, pages)

    assert [page["page_id"] for page in expanded] == ["lec01-p001", "missing"]
