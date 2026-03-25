"""CLI entry point for arxiv-search."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .bibtex import entries_to_bibtex
from .parser import parse_query
from .query import node_to_query, search

MAX_ARXIV_RESULTS = 30_000


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        prog="arxiv-search",
        description="Search arXiv with a boolean expression and export results as BibTeX.",
    )
    source = ap.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "query_file",
        nargs="?",
        type=Path,
        default=None,
        help="File containing the boolean search expression",
    )
    source.add_argument(
        "-q", "--query",
        type=str,
        default=None,
        help='Boolean search expression, e.g. \'"LLM" AND "AI"\'',
    )
    ap.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output BibTeX file (default: <query_file>.bib, or results.bib with -q)",
    )
    ap.add_argument(
        "--max-results",
        type=int,
        default=None,
        help=f"Maximum results to fetch (arXiv hard limit: {MAX_ARXIV_RESULTS})",
    )
    args = ap.parse_args(argv)

    # --- Read and parse the query ---
    if args.query is not None:
        query_text = args.query.strip()
    else:
        query_text = args.query_file.read_text().strip()
    if not query_text:
        print("Error: query is empty.", file=sys.stderr)
        sys.exit(1)

    try:
        ast = parse_query(query_text)
    except ValueError as exc:
        print(f"Error parsing query: {exc}", file=sys.stderr)
        sys.exit(1)

    arxiv_query = node_to_query(ast)
    print(f"Query: {arxiv_query}", file=sys.stderr)

    # --- Clamp max_results ---
    max_results = args.max_results
    if max_results is not None and max_results > MAX_ARXIV_RESULTS:
        print(
            f"Warning: arXiv caps at {MAX_ARXIV_RESULTS} results, clamping.",
            file=sys.stderr,
        )
        max_results = MAX_ARXIV_RESULTS

    # --- Fetch ---
    entries = search(arxiv_query, max_results=max_results)
    if not entries:
        print("No results found.", file=sys.stderr)
        sys.exit(0)

    # --- Write BibTeX ---
    bibtex = entries_to_bibtex(entries)
    if args.output:
        output_path = args.output
    elif args.query_file:
        output_path = args.query_file.with_suffix(".bib")
    else:
        output_path = Path("results.bib")
    output_path.write_text(bibtex, encoding="utf-8")
    print(f"Wrote {len(entries)} entries to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
