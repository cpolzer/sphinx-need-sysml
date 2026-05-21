# Spec 003 — Drop inline-anchor workaround once sphinx-need-svg 0.3.1 ships

**Status**: Blocked on upstream release
**Created**: 2026-05-21
**Owner**: christian polzer

## Trigger

This spec becomes actionable when:

1. `sphinx-need-svg` **0.3.1 (or any tag ≥0.3.1 carrying PR #3)** is published to PyPI, AND
2. `uv pip index versions sphinx-need-svg | head -1` returns ≥0.3.1.

Current state (2026-05-21): commit `c7087e4` on `main` of
`/home/chris/develop/open_source/sphinx-need-svg` bumped the version
to 0.3.1, but the `v0.3.1` tag was not pushed, so the release workflow
(triggered by `push: tags: 'v[0-9]+.[0-9]+.[0-9]+'`) never fired. PyPI
still serves 0.3.0 only.

To unblock: in the sphinx-need-svg repo, tag `c7087e4` as `v0.3.1` and
push the tag. The release workflow will publish to PyPI within minutes.

## Background

Spec 002 (full SysML diagram coverage) shipped 7 inline-SVG diagram
templates. During build verification we hit broken anchor links: the
upstream `sphinx_need_svg.jinja_context.SvgJinjaContext.ref()` returned
`{docname}.html#{id}` unconditionally, which the browser resolves
relative to the current page's URL — doubling the path
(`examples/page.html#PD-001` resolves to
`examples/examples/page.html#PD-001`) and 404-ing for the same-page
case (which is the normal case for sphinx-need-sysml diagrams).

**Two parallel fixes shipped:**

1. **Upstream fix** (sphinx-need-svg PR #3, commit `9e449da` on `main`):
   `ref()` now uses `builder.get_relative_uri(fromdocname, target_docname)`
   when `fromdocname` is threaded in from `process_needsvg`. Returns
   `#NEED-ID` for same-page, `sibling.html#NEED-ID` for sibling-page,
   `../path/page.html#NEED-ID` for cross-directory. `flow()` inherits
   the fix transparently because it calls `ref()` internally.

2. **Downstream workaround** (sphinx-need-sysml PR #3, commit
   `4934b30`): swapped all `{{ ref(x.id) }}` → `#{{ x.id }}` and
   inlined all `{{ flow(x) }}` calls as
   `<a href="#{{ id }}"><rect/><text/></a>` blocks. This works because
   `sphinx-need-sysml` only renders SVGs on the **same page** as the
   needs they reference, so a pure fragment link is correct in all our
   current cases.

The workaround is **functionally correct but inelegant**:

- ~30 extra lines across `svg_templates.py` (7 templates, ~11 helper
  call sites) and `vehicle_system.rst` (3 handwritten `needsvg`
  blocks).
- Loses the benefit of `flow()`: any future visual updates to the
  shared card style in sphinx-need-svg won't propagate.
- Breaks down if a user ever renders a diagram on a *different page*
  from the needs it references (currently no such case in our demo,
  but it's a real-world pattern).

## Goal

Once sphinx-need-svg ≥0.3.1 is on PyPI, revert the inline workaround
back to clean `{{ ref() }}` / `{{ flow() }}` calls so we get the
upstream benefits and stay portable to cross-page diagrams.

## Out of scope

- Visual redesign of any diagram (cards, colors, shapes stay identical).
- New diagram types or fields.
- Changes to the PlantUML templates (`templates.py`) — they go through
  sphinx-needs' `needuml`, which has always handled `ref()` correctly
  via `calculate_link(app, need, fromdocname)`.

## User stories

### US1 — Pin the upstream dep

As a maintainer, I want `pyproject.toml` to require sphinx-need-svg
≥0.3.1 so users installing sphinx-need-sysml automatically get the
relative-URL fix.

**Acceptance**: both occurrences in `[project.optional-dependencies]`
(`test` extra at line 38, `docs` extra at line 44) bumped to
`sphinx-need-svg>=0.3.1`. `uv lock` resolves clean. `uv sync
--all-extras` succeeds.

### US2 — Restore `flow()` in card-style SVG templates

As a template maintainer, I want the BDD and IBD SVG templates to use
`{{ flow(id) }}` again instead of the hand-inlined
`<a href="#{id}"><rect/><text/></a>` block, so they stay in sync with
upstream's card style.

**Acceptance**:

- `BDD_SVG_TEMPLATE` (in `sphinx_need_sysml/svg_templates.py`):
  - `<g transform="translate(300, 20)">{{ flow(root_id) }}</g>` (root card)
  - `<g transform="translate({{ cx - 60 }}, 180)">{{ flow(child.id) }}</g>` (child card)
- `IBD_SVG_TEMPLATE`:
  - `<g transform="translate({{ px }}, 90)">{{ flow(part.id) }}</g>` (part card)
- Rendered visual output is **identical** — same rect width 120, rx 4,
  fill `#ddeeff`, stroke `#336699`.

### US3 — Restore `ref()` in custom-shape SVG templates

As a template maintainer, I want the ACT / UC / PKG / SD / STM
templates to use `{{ ref(x.id) }}` for their `href` attributes again
(keeping their custom shapes intact: rounded rectangles, ellipses,
actor stick figures, etc.).

**Acceptance**: 8 `href="#{{ x.id }}"` occurrences swapped back to
`href="{{ ref(x.id) }}"`:

| Template | Where |
|---|---|
| `ACT_SVG_TEMPLATE` | action card |
| `UC_SVG_TEMPLATE` | actor stick figure |
| `UC_SVG_TEMPLATE` | usecase ellipse |
| `PKG_SVG_TEMPLATE` | root package rect |
| `PKG_SVG_TEMPLATE` | child package rect |
| `SD_SVG_TEMPLATE` | lifeline head |
| `SD_SVG_TEMPLATE` | message label |
| `STM_SVG_TEMPLATE` | ordinary state rect |

(11 helper calls total = 3 from US2 + 8 here.)

### US4 — Restore `flow()` in the vehicle demo

As an end-user reading the docs, I want the three handwritten
`needsvg` examples in `docs/examples/vehicle_system.rst` (BDD-svg,
IBD-svg, Req-svg) to demonstrate the canonical `{{ flow(x.id) }}`
pattern rather than the inline-rect workaround, so the docs match
upstream's intended usage.

**Acceptance**:

- The three `.. needsvg::` blocks (plus their accompanying
  `.. code-block:: rst` mirrors) collapse back to `{{ flow(id) }}`
  usage.
- The `.. note::` paragraph explaining the doubled-path bug is
  removed (no longer relevant once the upstream fix is in).

### US5 — Verify

As a maintainer, I want to confirm the cleanup didn't regress
anything.

**Acceptance** — all of:

| Check | Target |
|---|---|
| `uv run sphinx-build -W docs docs/_build/html` | clean, 0 warnings |
| `grep -c 'href="#[A-Z]' docs/_build/html/examples/vehicle_system.html` | ≥120 (was 120 with workaround) |
| `grep -cE 'href="[^"]*\.html#[A-Z]' docs/_build/html/examples/vehicle_system.html` (excluding `directives/` cross-page nav) | 0 doubled-path links |
| `uv run pytest tests/test_{bdd,ibd,stm,act,sd,uc,pkg}_directive.py` | all 30 pass |
| `uv run ruff check .` and `uv run ruff format --check .` | clean |
| Visual: open `vehicle_system.html` and click any node | navigates correctly to the need's anchor on the same page |

## Implementation order

Single commit on a fresh branch off `main`:

1. Pin `sphinx-need-svg>=0.3.1` in `pyproject.toml` (US1)
2. Restore `flow()` / `ref()` in `svg_templates.py` (US2 + US3 — 11
   edits)
3. Restore `flow()` in `vehicle_system.rst` (US4 — 3 needsvg blocks +
   3 code-block mirrors + 1 note removal)
4. `uv sync --all-extras`
5. Run US5 verification gates
6. Commit + push + open PR titled `refactor: revert SVG link
   workaround after sphinx-need-svg 0.3.1 fix`

## Risks

- **Visual drift**: `flow()` produces a card with hard-coded styling.
  If upstream changes that styling in a future release, our diagrams
  shift. **Mitigation**: pin to exact version range like
  `sphinx-need-svg>=0.3.1,<0.4.0` if drift becomes an issue. For now,
  keep the open `>=0.3.1` range.
- **Cross-page regression**: if a user has a diagram on page A
  referencing a need on page B, the workaround's `#NEED-ID` link would
  silently 404, whereas the upstream-fixed `ref()` produces
  `../b/page.html#NEED-ID`. Adding the upstream dep restores
  correctness for this case. **No mitigation needed**, this is an
  improvement.

## Open questions

None — execution is mechanical.

## References

- Workaround commit: `4934b30` on branch `002-full-sysml-diagrams`
  ("fix: SVG link generation produced doubled paths on same-page
  references")
- Upstream fix: sphinx-need-svg PR #3, commit `9e449da` on `main`
- Upstream version bump: `c7087e4` on `main` (no tag pushed yet —
  the blocker for this spec)
