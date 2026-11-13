"""Verification for RBI archive Markdown output.

Checks, in order:
1. Frontmatter is present and carries pdf_sha256 and md_sha256.
2. Page parity: exactly one `<!-- PAGE N -->` anchor for every page
   1..expected_pages, in order, no duplicates, no gaps.
3. Table balance: within each contiguous block of pipe-lines, every row
   has the same number of `|` characters as the first row of the block.
4. Text density: a page section with fewer than 30 alphanumeric
   characters is reported (warning, not fatal, unless every page is empty).

SymPy formula check is best-effort only: it runs when sympy is
importable, and a parse failure is a warning, never fatal.

Returns (ok, issues) where ok is False only on fatal issues.
"""

import re

PAGE_ANCHOR_RE = re.compile(r"<!--\s*PAGE\s+(\d+)\s*-->")
FORMULA_RE = re.compile(r"^[^#|]{0,80}=[^|]{1,120}$")
ALNUM_RE = re.compile(r"[A-Za-z0-9]")

FATAL_PREFIX = "FATAL:"
WARN_PREFIX = "WARN:"


def _page_sections(markdown):
    """Split body (after frontmatter) into {page_number: text}."""
    body = markdown
    if markdown.startswith("---"):
        end = markdown.find("\n---", 3)
        if end != -1:
            body = markdown[end + 4:]
    sections = {}
    order = []
    current = None
    for line in body.splitlines():
        m = PAGE_ANCHOR_RE.search(line)
        if m:
            current = int(m.group(1))
            if current in sections:
                sections[current] += "\n" + line
            else:
                sections[current] = ""
                order.append(current)
            continue
        if current is not None:
            sections[current] += "\n" + line
    return sections, order


def _check_frontmatter(markdown, issues):
    if not markdown.startswith("---"):
        issues.append(FATAL_PREFIX + " missing YAML frontmatter delimiter")
        return
    end = markdown.find("\n---", 3)
    if end == -1:
        issues.append(FATAL_PREFIX + " unterminated YAML frontmatter")
        return
    head = markdown[:end]
    for field in ("pdf_sha256:", "md_sha256:", "doc_id:", "total_pages:"):
        if field not in head:
            issues.append(FATAL_PREFIX + " frontmatter missing field " + field)


def _check_page_parity(markdown, expected_pages, issues):
    sections, order = _page_sections(markdown)
    for n in range(1, expected_pages + 1):
        if n not in sections:
            issues.append(FATAL_PREFIX + " missing page anchor for page %d" % n)
    for n in sections:
        if n < 1 or n > expected_pages:
            issues.append(FATAL_PREFIX + " unexpected page anchor for page %d" % n)
    if order != sorted(order):
        issues.append(FATAL_PREFIX + " page anchors out of order: %s" % (order,))
    if len(order) != len(set(order)):
        issues.append(FATAL_PREFIX + " duplicate page anchors present")
    return sections


def _check_tables(markdown, issues):
    lines = markdown.splitlines()
    block = []
    def flush(block):
        if not block:
            return
        if len(block) == 1:
            issues.append(WARN_PREFIX + " single-row table block: %s" % (block[0][:80],))
            return
        counts = [row.count("|") for row in block]
        if len(set(counts)) != 1:
            issues.append(FATAL_PREFIX + " unbalanced table rows (pipe counts %s): %s"
                          % (counts, block[0][:80]))
    for line in lines:
        if line.strip().startswith("|"):
            block.append(line)
        else:
            flush(block)
            block = []
    flush(block)


def _check_density(sections, expected_pages, issues):
    empty = 0
    for n in range(1, expected_pages + 1):
        text = sections.get(n, "")
        if "<!-- OCR_EMPTY_PAGE -->" in text:
            issues.append(WARN_PREFIX + " page %d produced no text (OCR_EMPTY_PAGE)" % n)
            empty += 1
        elif len(ALNUM_RE.findall(text)) < 30:
            issues.append(WARN_PREFIX + " page %d has low text density (%d alphanumerics)"
                          % (n, len(ALNUM_RE.findall(text))))
            empty += 1
    if empty == expected_pages and expected_pages > 0:
        issues.append(FATAL_PREFIX + " every page is empty")


def _check_formulas(markdown, issues):
    try:
        import sympy
    except Exception:
        return
    checked = 0
    for line in markdown.splitlines():
        if checked >= 20:
            break
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "|", "<!--", "---")):
            continue
        if "=" not in stripped or not any(c.isdigit() for c in stripped):
            continue
        if not FORMULA_RE.match(stripped):
            continue
        checked += 1
        rhs = stripped.split("=", 1)[1].strip().rstrip(".")
        if not rhs:
            continue
        try:
            sympy.sympify(rhs, evaluate=False)
        except Exception as exc:
            issues.append(WARN_PREFIX + " sympy could not parse formula %r: %s"
                          % (stripped[:100], exc))


def verify_markdown(markdown, expected_pages):
    """Verify one Markdown document. Returns (ok: bool, issues: list[str])."""
    issues = []
    if not isinstance(markdown, str) or not markdown:
        return False, [FATAL_PREFIX + " empty markdown"]
    if expected_pages is None or expected_pages < 1:
        return False, [FATAL_PREFIX + " expected_pages must be >= 1"]
    _check_frontmatter(markdown, issues)
    sections = _check_page_parity(markdown, expected_pages, issues)
    _check_tables(markdown, issues)
    _check_density(sections, expected_pages, issues)
    _check_formulas(markdown, issues)
    fatal = [i for i in issues if i.startswith(FATAL_PREFIX)]
    return (len(fatal) == 0), issues
