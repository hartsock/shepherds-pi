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

Pick real values for `contextWindow`/`maxTokens` rather than guessing — but
**`/v1/models` is not always a reliable source for the window**, and the two
fields interact in a way that bites hard.

**`maxTokens` is reserved OUT OF `contextWindow`.** Whatever you set aside for
output is not available for the prompt. The example above (`128000` / `16384`)
is a healthy ratio; `65536` / `64000` leaves about **1,500 tokens for the entire
prompt**, and every request fails immediately.

**An overstated `contextWindow` is worse than "you overflow and the backend
errors."** `pi`'s usage meter is denominated in the number you declare, so a
window three times too large means the meter reads a comfortable `7%` while the
request is already impossible. The failure gives you no signal to follow.

**Check the serving process, not just the catalogue.** For a llama.cpp backend
(including one behind a router), `/v1/models` may advertise a `context_length`
the server does not actually serve. Ask the server what it loaded:

```bash
# what the catalogue ADVERTISES
curl -s "$BASE/v1/models" | jq '.data[] | select(.id=="<model>") | .context_length'

# what the server is actually SERVING
curl -s "$BASE/props?model=<model>" | jq '.default_generation_settings.n_ctx'
```

Measured on one such router, same model, same endpoint: the catalogue said
`200000`, the server said `65536`. If those two disagree, **the server wins** —
it is the one that rejects your request.

Two notes on `/props`: a router with nothing loaded answers `n_ctx: 0` with
`model_path: "none"`, which means *unknown*, not zero — pass `?model=<id>` to
get a real answer. And backends that are not llama.cpp will not have `/props`
at all, in which case the catalogue is the best you have.

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
