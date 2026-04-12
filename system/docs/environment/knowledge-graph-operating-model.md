# Knowledge Graph Operating Model

Date: 2026-04-11
Status: Active

## Purpose

Define the role of the knowledge graph inside the new development environment.

## What The Knowledge Graph Is For

The knowledge graph is the source of truth for durable development knowledge, including:

- architecture intent
- product and user flows
- API and integration contracts
- important technical decisions
- migration rationale
- cross-repo system understanding

It should contain knowledge that remains useful after the current coding session ends.

The graph should be maintained through three explicit workflows:

- ingest
- query filing
- lint

## What The Knowledge Graph Is Not For

The knowledge graph is not the source of truth for:

- live runtime state
- secrets or credentials
- tool cache
- generated artifacts
- rapidly changing local machine details
- low-value temporary notes

## Relationship To Other Sources Of Truth

Use this model:

- code = executable truth
- `system/docs/environment` = operational environment truth
- knowledge graph = conceptual and historical truth
- `knowledge/raw` = immutable source material for synthesis

These layers should reinforce each other, not compete.

## When To Update The Graph

Update or link a knowledge note when work changes:

- architecture shape
- system boundaries
- data or API contracts
- product behavior across repos or services
- important environment decisions with long-term significance

Do not update the graph for every small local change.

When a new durable source is added, ingest it from `knowledge/raw` instead of leaving it as an unprocessed reference.

When a useful answer should survive the session, file it back into the graph as a durable synthesis note.

Use automation only as a reminder trigger, not as an automatic author:

- hard-automate environment integrity checks
- soft-automate graph/doc update reminders
- keep the actual note content curated by a human or agent with judgment

## Supporting Files

Use these supporting files as part of the operating model:

- `Knowledge Graph/index.md`
- `logs/ingest-log.md`
- `logs/query-log.md`
- `logs/lint-log.md`
- `99 Meta/templates/source-ingest-template.md`
- `99 Meta/templates/query-synthesis-template.md`
- `system/docs/environment/hybrid-knowledge-workflow.md`

## Quality Bar

Graph notes should be:

- durable
- cross-session useful
- synthesized rather than dumped
- linked to the relevant code or environment docs

## Anti-Patterns

Avoid turning the graph into:

- a noisy work log
- a duplicate of repo README content
- a cache of copied source text
- a second home for runtime instructions that belong in `system/docs/environment`
