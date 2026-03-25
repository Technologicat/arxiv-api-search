"""arXiv API client — query building and paginated fetching."""

from __future__ import annotations

import sys
import time

import feedparser
import requests

from .parser import BinOp, Node, Term

ARXIV_API_URL = "https://export.arxiv.org/api/query"
PAGE_SIZE = 200
RATE_LIMIT_SECONDS = 3


def node_to_query(node: Node) -> str:
    """Convert a parsed AST to an arXiv search_query string.

    Each leaf term is expanded to search both title and abstract:
    ``term`` becomes ``(ti:term OR abs:term)``.
    """
    if isinstance(node, Term):
        if node.is_phrase or " " in node.value:
            escaped = f'"{node.value}"'
        else:
            escaped = node.value
        return f"(ti:{escaped} OR abs:{escaped})"

    if isinstance(node, BinOp):
        left = node_to_query(node.left)
        right = node_to_query(node.right)
        return f"({left} {node.op} {right})"

    raise TypeError(f"Unexpected node type: {type(node)}")


def search(query: str, max_results: int | None = None) -> list[dict]:
    """Search arXiv, paginating as needed. Returns feedparser entries.

    Respects the arXiv rate limit of one request per 3 seconds.
    """
    results: list[dict] = []
    start = 0
    total: int | None = None

    while True:
        # How many to request this page
        page_size = PAGE_SIZE
        if max_results is not None:
            remaining = max_results - len(results)
            if remaining <= 0:
                break
            page_size = min(page_size, remaining)

        params = {
            "search_query": query,
            "start": start,
            "max_results": page_size,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }

        resp = requests.get(ARXIV_API_URL, params=params, timeout=30)
        resp.raise_for_status()

        feed = feedparser.parse(resp.text)

        if total is None:
            total = int(feed.feed.get("opensearch_totalresults", 0))
            effective = min(total, max_results) if max_results else total
            print(f"Total matches: {total}; fetching up to {effective}.", file=sys.stderr)

        # arXiv signals errors as entries with id "http://arxiv.org/api/errors"
        if feed.entries and "api/errors" in feed.entries[0].get("id", ""):
            msg = feed.entries[0].get("summary", "Unknown API error")
            raise RuntimeError(f"arXiv API error: {msg}")

        if not feed.entries:
            break

        results.extend(feed.entries)
        start += len(feed.entries)

        if start >= total:
            break
        if max_results is not None and len(results) >= max_results:
            break

        # Rate limit — sleep before the *next* request
        time.sleep(RATE_LIMIT_SECONDS)

    return results
