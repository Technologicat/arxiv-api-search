"""Tests for the arXiv query builder."""

from arxiv_api_search.parser import BinOp, Term
from arxiv_api_search.query import node_to_query


class TestNodeToQuery:
    def test_bare_word(self):
        q = node_to_query(Term("quantum"))
        assert q == "(ti:quantum OR abs:quantum)"

    def test_phrase(self):
        q = node_to_query(Term("quantum computing", is_phrase=True))
        assert q == '(ti:"quantum computing" OR abs:"quantum computing")'

    def test_and(self):
        tree = BinOp("AND", Term("a"), Term("b"))
        q = node_to_query(tree)
        assert q == "((ti:a OR abs:a) AND (ti:b OR abs:b))"

    def test_or(self):
        tree = BinOp("OR", Term("a"), Term("b"))
        q = node_to_query(tree)
        assert q == "((ti:a OR abs:a) OR (ti:b OR abs:b))"

    def test_andnot(self):
        tree = BinOp("ANDNOT", Term("a"), Term("b"))
        q = node_to_query(tree)
        assert q == "((ti:a OR abs:a) ANDNOT (ti:b OR abs:b))"

    def test_complex(self):
        # ("quantum computing" OR QC) AND "error correction"
        tree = BinOp(
            "AND",
            BinOp(
                "OR",
                Term("quantum computing", is_phrase=True),
                Term("QC"),
            ),
            Term("error correction", is_phrase=True),
        )
        q = node_to_query(tree)
        expected = (
            '(((ti:"quantum computing" OR abs:"quantum computing") '
            "OR (ti:QC OR abs:QC)) "
            'AND (ti:"error correction" OR abs:"error correction"))'
        )
        assert q == expected
