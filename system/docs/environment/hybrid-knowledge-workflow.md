# Hybrid Knowledge Workflow

Date: 2026-04-11
Status: Active

## Purpose

Define how the development environment combines:

- code and repos
- environment docs
- the knowledge graph
- raw source material

This extends the existing environment model with a more systematic knowledge-ingest workflow without collapsing the truth boundaries.

## Four Layers

Use this model:

- raw sources
  - immutable inputs such as articles, specs, transcripts, meeting notes, exports, and assets
- knowledge graph
  - synthesized, interlinked markdown maintained by the agent
- environment docs
  - operational truth for adapters, policies, scripts, and environment behavior
- code and repos
  - executable truth

## Source Of Truth Split

Keep this boundary:

- code = executable truth
- `system/docs/environment` = operational truth
- knowledge graph = conceptual and historical truth
- `knowledge/raw` = immutable source material used for synthesis

Do not let the knowledge graph become a duplicate runtime configuration store.

## Directory Model

Under `/mnt/c/Development/knowledge`, use:

- `raw/`
  - curated source material the agent reads but does not edit
- `Knowledge Graph/`
  - synthesized notes and navigation pages
- `logs/`
  - append-only ingest, query, and lint history
- `outputs/`
  - optional generated reports, comparisons, and presentation artifacts

## Core Workflows

### Ingest

Use when a new durable source is added to `knowledge/raw`.

Expected flow:

1. Read the source.
2. Create or update a source note using the ingest template.
3. Update related concept, system, product, or decision notes.
4. Add or improve cross-links.
5. Append an entry to `logs/ingest-log.md`.
6. Update `Knowledge Graph/index.md` if a new durable page was created.

### Query

Use when a question requires synthesis across existing graph notes or raw sources.

Expected flow:

1. Search the graph first.
2. Read raw sources only when the graph is insufficient or needs refresh.
3. Answer the question.
4. If the answer is durable, save it as a note using the query synthesis template.
5. Append an entry to `logs/query-log.md`.
6. Update `Knowledge Graph/index.md` if a new durable page was created.

### Lint

Use periodically to keep the graph healthy.

Check for:

- orphan notes with no inbound links
- notes with no outbound links
- stale synthesis that should be refreshed
- mentioned-but-missing concepts
- weak navigation from `index.md`
- recent major changes that were not filed back into the graph

Append results to `logs/lint-log.md`.

## What Belongs In The Graph

Good graph material:

- architecture intent
- system boundaries
- product and user flows
- API and data contracts
- major decisions and rationale
- cross-repo relationships
- durable syntheses from investigations

## What Does Not Belong In The Graph

Do not store these in the graph as primary truth:

- runtime secrets
- live adapter or symlink truth
- generated build artifacts
- temporary debugging notes
- routine implementation details already explained by code

## Filing Rule

When a conversation produces any of these, file it back into the graph:

- a durable comparison
- a reusable synthesis
- a clarified contract
- a non-trivial architectural conclusion
- a cross-repo dependency insight

Do not file disposable chat output.

## Operational Rule

When a change affects architecture, contracts, product flows, or environment policy:

- update the knowledge graph if the knowledge is durable
- update `system/docs/environment` if operational behavior changed
- update both when both truth domains changed

## Recommended Commands

- remind on documentation sync:
  - `/mnt/c/Development/system/ai/scripts/check-doc-sync.sh <changed-paths...>`
- verify environment integrity:
  - `/mnt/c/Development/system/ai/scripts/verify-links.sh`
- run graph lint:
  - `/mnt/c/Development/system/ai/scripts/graph-lint.sh`
