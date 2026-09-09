---
name: pi-inference-backend
description: Point pi at any OpenAI-compatible inference endpoint and set a model as the CLI-wide default, so bare `pi` launches ready to go
argument-hint: "[provider-name] [base-url] [model-id]"
---

# Wire pi to a custom inference backend

`pi` can talk to any OpenAI-compatible chat-completions endpoint — a hosted
gateway, a self-hosted vLLM/llama.cpp/Ollama server, whatever you point it
at. This skill covers: defining the provider, authenticating it, listing
its models, and making one model the CLI-wide default so a bare `pi`
invocation (no `--provider`/`--model` flags) just works.

Requires `skills/pi-install` already done (needs `~/.pi/agent/` to exist).

## 1. Define the provider

Edit `~/.pi/agent/models.json` (create it if absent):

```json
{
  "providers": {
    "<provider-id>": {
      "name": "<Human-readable name>",
      "baseUrl": "<https://your-endpoint/v1>",
      "api": "openai-completions",
      "apiKey": "$<YOUR_ENV_VAR_NAME>",
      "models": [
        {
          "id": "<model-id-as-the-backend-names-it>",
          "name": "<Human-readable model name>",
          "reasoning": true,
          "input": ["text"],
          "contextWindow": 128000,
          "maxTokens": 16384,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
        }
      ]
    }
  }
}
```

Pick real values for `contextWindow`/`maxTokens` from the backend's own
model listing (see step 3) rather than guessing — an overstated
`contextWindow` just means `pi` will let you overflow the real limit before
the backend errors.

`apiKey: "$<YOUR_ENV_VAR_NAME>"` means "read this from the named
environment variable at call time" — nothing goes in the file itself.
Export it in your shell profile, e.g.:

```bash
export YOUR_ENV_VAR_NAME="$(cat ~/.secrets/your-backend/token)"
```

(or however your secret store works — the point is: the token lives in one
place, and the shell profile is the only thing that reads it into the
process environment.)

## 2. Verify auth resolves

```bash
pi auth check --provider <provider-id> --json
```

Expect `{"status":"ready", ...}`. **This only proves an auth entry
resolves — not that it's the right one.** If `~/.pi/agent/auth.json` has a
stray per-provider entry (leftover manual credential, typo, accidental
paste), it silently shadows the `$ENV_VAR` substitution from `models.json`
and `auth check` will still report `ready` while real completions 401. If
you get a 401 despite `ready`, check `auth.json` for a
`"<provider-id>"` entry before assuming the token itself is bad:

```bash
python3 -c "import json; print(json.load(open('$HOME/.pi/agent/auth.json')).get('<provider-id>'))"
```

Remove any stray entry so the provider falls through to the env-var
substitution in `models.json`.

## 3. Confirm the model is actually served

Don't trust the model ID you were given — check the backend's own
`/v1/models` listing before wiring it in:

```bash
curl -s <base-url>/models -H "Authorization: Bearer $YOUR_ENV_VAR_NAME" | \
  python3 -m json.tool
```

## 4. End-to-end test with an explicit flag

```bash
pi --provider <provider-id> --model "<model-id>" \
   --print "Reply with exactly: backend-ok" --no-session
```

## 5. Set it as the CLI-wide default

Edit `~/.pi/agent/settings.json`:

```json
{
  "defaultProvider": "<provider-id>",
  "defaultModel": "<model-id>"
}
```

(Merge these two keys into whatever else is already in that file — don't
overwrite unrelated settings.)

## 6. Verify the default took effect

```bash
pi --print "Reply with exactly: default-ok" --no-session
```

No `--provider`/`--model` flags this time. If it returns `default-ok`,
every bare `pi` launch — including ones spawned by
`skills/herdr-helpers-tab` in this repo — now comes up on this backend and
model.
