# Culture Key — Agent Toolkit (OS Layer)

This folder set turns the **Culture Key Codex** into a DevSecOps-style operating system.
It lives **inside the same repository** as the Codex so we preserve a single source of truth.

## Structure
- `os/manifest.yml` — the flow map (triggers → checkpoints → outputs)
- `os/agents.json` — the ontology registry (roles, IO, ethics scope)
- `os/security.yml` — conscious monitoring + audit settings
- `os/release_protocol.md` — publishing & provenance policies
- `os/agents/*` — per‑agent modules (Aequitas, Lychnia, Magna, PosterKit, CodexRoot)

## Branching (recommended)
Create a protected working branch called **agent-toolkit** and iterate there.
When stable, merge into main with a signed commit.

## How to use
1) Copy `os/` into your existing `culture-key-codex` repo.
2) Commit on the `agent-toolkit` branch with message: `OS: add Agent Toolkit v1 skeleton`.
3) Evolve each agent's README and policies with real content as we proceed.