---
name: pi-install
description: Install the pi coding agent CLI and confirm it runs
---

# Install pi

`pi` ([earendil-works/pi](https://github.com/earendil-works/pi)) ships as
the npm package `@earendil-works/pi-coding-agent`, MIT licensed.

## Install

```bash
npm install -g @earendil-works/pi-coding-agent
```

This installs the `pi` binary and its config directory scaffold under
`~/.pi/agent/` on first run (override with `PI_CODING_AGENT_DIR`).

## Verify

```bash
pi --version
pi --help
```

`pi --help` prints usage, the built-in tool list, and every provider-related
environment variable it recognizes (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`,
and so on — see `skills/pi-inference-backend` in this repo for pointing it
at a custom OpenAI-compatible endpoint instead).

## Config files pi creates

| File | Purpose |
|---|---|
| `~/.pi/agent/models.json` | Custom provider/model definitions |
| `~/.pi/agent/settings.json` | CLI-wide settings, including `defaultProvider`/`defaultModel` |
| `~/.pi/agent/auth.json` | Per-provider credentials (only if you don't use env-var auth) |

See [`docs/pi-config-reference.md`](../../docs/pi-config-reference.md) for
the full shape of each file.

## Sanity check: run one prompt, non-interactively

```bash
pi --print "Reply with exactly: pi-ok" --no-session
```

Expect the literal output `pi-ok`. If it errors, `pi --help` and `pi auth
check --provider <name> --json` are the two commands to run next — most
first-run failures are a missing/misnamed API key env var.
