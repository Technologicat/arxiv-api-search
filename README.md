# arxiv-api-search

Search arXiv using boolean expressions and export the results as BibTeX.
Built for scoping reviews and systematic literature searches.

## Installation

Requires Python 3.10+.

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
