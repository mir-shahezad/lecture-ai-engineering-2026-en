from app.retrieval import include_adjacent_pages


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
