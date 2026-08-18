# arxiv-api-search

![100% Python](https://img.shields.io/github/languages/top/Technologicat/arxiv-api-search)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue)
![CI status](https://img.shields.io/github/actions/workflow/status/Technologicat/arxiv-api-search/ci.yml?branch=main)
[![codecov](https://codecov.io/gh/Technologicat/arxiv-api-search/branch/main/graph/badge.svg)](https://codecov.io/gh/Technologicat/arxiv-api-search)
![license](https://img.shields.io/github/license/Technologicat/arxiv-api-search)
![open issues](https://img.shields.io/github/issues/Technologicat/arxiv-api-search)

Search arXiv using boolean expressions and export the results as BibTeX.
Built for scoping reviews and systematic literature searches.

> [!IMPORTANT]
> **Superseded by `raven-arxiv-search`** in [Raven](https://github.com/Technologicat/raven),
> which is where the development continues. This standalone version remains available and
> keeps working, but receives no further updates.
>
> Raven has since grown a whole family of arXiv tools around it, so moving over gains you
> more than the search itself:
>
> - **`raven-arxiv-search`** — this tool's successor: boolean-expression search against the
>   arXiv API, with automatic pagination and rate limiting, exported as BibTeX.
> - **`raven-arxiv-download`** — fetches the PDFs for a list of arXiv IDs, naming each file
>   from the paper's own metadata.
> - **`raven-arxiv2id`** — reads a directory of PDFs and extracts the arXiv IDs from their
>   filenames, handling all three arXiv ID eras and keeping the latest version of each paper.
> - **`raven-arxiv2bib`** — turns a list of arXiv IDs into BibTeX, completing the path
>   `raven-arxiv2id` starts: a folder of downloaded papers becomes a searchable bibliography
>   in two piped commands.

## Installation

```bash
pdm install
```

## Usage

### From a query file

```bash
arxiv-api-search query.txt -o results.bib
```

The query file contains a boolean expression:

```
("large language model" OR LLM)
AND "artificial intelligence"
ANDNOT "image generation"
```

Blank lines are allowed for readability.

### Inline query

```bash
arxiv-api-search -q '"quantum computing" AND "error correction"' -o results.bib
```

### Options

| Flag | Description |
|---|---|
| `-o`, `--output` | Output `.bib` file (default: `<query_file>.bib`, or `results.bib` with `-q`) |
| `--max-results` | Maximum number of results to fetch (arXiv hard limit: 30,000) |

## Query syntax

Each leaf term is searched in both the **title** and **abstract** fields.

| Feature | Syntax |
|---|---|
| Bare word | `quantum` |
| Quoted phrase | `"quantum computing"` |
| AND | `a AND b` |
| OR | `a OR b` |
| Exclude | `a ANDNOT b` |
| Grouping | `(a OR b) AND c` |

Operators are case-insensitive. Precedence (lowest to highest): `OR`, `AND`/`ANDNOT`, atom.
Parentheses override precedence.

## Rate limiting

The arXiv API terms of use require at most one request per 3 seconds.
This tool enforces that limit automatically. Large result sets will take
a while — roughly 3 seconds per 200 results.

## License

MIT
