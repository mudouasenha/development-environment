# 9Router Local Inference Routing

## Purpose

9Router is an opt-in, local inference gateway for the Development environment. It provides one OpenAI-compatible endpoint for approved model routes, model fallback combos, and local usage accounting. It does not replace Hermes tools, MCP, A2A, Hindsight, or the knowledge graph.

## Runtime Boundary

- Container: `9router`
- Endpoint: `http://127.0.0.1:20128/v1`
- Dashboard: `http://127.0.0.1:20128`
- Docker restart policy: `unless-stopped`
- Persistent state: `/home/matheus/.local/share/9router`
- Private runtime configuration: `/home/matheus/.config/9router/9router.env`

The host port is bound to loopback only. Do not publish it broadly, add it to a public tunnel, or place its state directory in a repository. The state contains provider credentials, router keys, combos, and usage information.

## Hermes Profiles

`nine-router` is cloned from `dev` so it has the same workspace, skills, MCP, memory, and safety capabilities. It changes only the inference route:

- provider: `custom:9router`
- base URL: `http://127.0.0.1:20128/v1`
- default model: `cx/gpt-5.6-sol`

Use `nine-router` to evaluate routing without changing the normal development route. The `dev` profile remains directly configured for OpenAI Codex. It can use 9Router temporarily with an explicit custom-provider model selection; this must be tested in a new session before relying on it for normal work.

## Routing Policy

Use 9Router combos for model-level failover. Keep candidates in the same capability class:

- coding/tool use: compatible tool-capable models only
- review: review-capable models only
- vision: vision-capable models only
- economy: low-risk summaries and triage until tool use and structured output have passed representative tests

Start new or changed combos in `nine-router`. Verify a normal response, streaming, a tool call, structured output if needed, and expected fallback behavior before using them as a routine route.

## OpenRouter

OpenRouter may be connected as a provider inside 9Router. It has two different fallback layers:

1. A 9Router combo can select a different model when the current route fails.
2. OpenRouter can select another upstream host for the same model when a request supplies its `provider` preferences.

OpenRouter routing preferences such as `data_collection: "deny"`, `allow_fallbacks`, `require_parameters`, and upstream `order` are request-level fields. Current 9Router source forwards request bodies but does not expose dashboard settings that automatically inject these fields into every OpenRouter request or combo. Hermes does not add them automatically. Do not assume a privacy preference is active unless the client actually sends it.

`data_collection: "deny"` narrows OpenRouter's eligible upstreams; it is not an end-to-end guarantee that no service retains data. For sensitive work, select an explicitly approved provider and model, review the provider's retention terms, and do not route secrets unless the route is authorized for them.

## Security Rules

- Use normal provider OAuth or API-key integrations only.
- Do not use browser-cookie capture, MITM, subscription interception, proxy pools, cloud sync, or tunnels.
- Keep `REQUIRE_API_KEY=true` and `ENABLE_REQUEST_LOGS=false` in the private router environment.
- Do not place dashboard passwords, router keys, provider keys, OAuth tokens, or the state directory in tracked files, Hindsight, or the knowledge graph.
- Keep prompt-altering modes such as Caveman and Ponytail disabled by default.

## Operations

Inspect the service without printing credentials:

```bash
rtk docker inspect 9router --format 'status={{.State.Status}} restart={{.HostConfig.RestartPolicy.Name}}'
rtk docker ps --filter name=9router
```

A deliberate container restart followed by a local endpoint check verifies restart recovery. Do not remove the data directory or run destructive Docker volume commands while preserving router state matters.

## Related Records

- Knowledge context: `[[9Router Local Inference Routing]]`
- Hermes integration: `[[Hermes Agent Workspace Integration]]`
- Hindsight boundary: [Hindsight Shared Memory Integration](hindsight-memory-integration.md)
