# pi config reference

`pi` reads three JSON files from its config directory (`~/.pi/agent/` by
default, override with `PI_CODING_AGENT_DIR`). This is the reference the
skills in this repo (`pi-install`, `pi-inference-backend`) point back to.

## `models.json` — custom providers and models

Defines providers `pi` doesn't know about out of the box: any
OpenAI-compatible endpoint, self-hosted or third-party.

```json
{
  "providers": {
    "<provider-id>": {
      "name": "<display name>",
      "baseUrl": "<https://endpoint/v1>",
      "api": "openai-completions",
      "apiKey": "$<ENV_VAR_NAME>",
      "models": [
        {
          "id": "<model id, exactly as the backend names it>",
          "name": "<display name>",
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

Field notes:

- `apiKey: "$NAME"` means "read environment variable `NAME` at call
  time" — never put a literal secret in this file.
- **`apiKey` is required even by backends that need no auth.** pi hides every
  model whose provider has no resolvable credential; the symptom is
  `No models available` from `pi --list-models`, which blames auth without
  naming the provider it dropped. A LAN endpoint started without an API key
  takes any value — `"apiKey": "no-auth-required"`. Use a literal rather than
  `"$VAR"` if anything non-interactive runs pi: a shell profile is not read by
  a non-interactive shell, and the model list silently empties again.
- `api: "openai-completions"` is the value for any backend that speaks
  the standard `/v1/chat/completions` shape. Check `pi --help` for other
  supported `api` values if the backend is different.
- `contextWindow`/`maxTokens` are declarative — `pi` trusts them for
  budgeting and UI display but the backend enforces the real limit.
  **`maxTokens` is reserved out of `contextWindow`**, so a large output
  reservation against a small real window starves the prompt.
  Verify rather than guessing — and note that a llama.cpp backend's
  `/v1/models` `context_length` can disagree with what it actually serves.
  `curl "$BASE/props?model=<id>" | jq .default_generation_settings.n_ctx`
  is the serving process's own answer; when the two disagree, it wins.
  (`n_ctx: 0` with `model_path: "none"` means nothing is loaded — unknown,
  not zero.)
- `cost` fields are for `pi`'s own cost-tracking display; set to `0` for
  free/internal endpoints, or real per-token pricing otherwise.
- `reasoning` does **not** control whether thinking is displayed — pi detects
  `reasoning_content`/`reasoning`/`reasoning_text` on the response stream at
  runtime, whatever this says. What it gates is the thinking toggle, the
  thinking levels, and the output budget: with `reasoning: false` pi never
  widens `maxTokens` for thinking, so a model that reasons anyway spends its
  output budget on hidden tokens and can return **empty content with
  `finish_reason: "length"`**. When a backend publishes no capability data,
  `true` is the safer declaration — the opposite error is silent.

## `settings.json` — CLI-wide settings

```json
{
  "defaultProvider": "<provider-id>",
  "defaultModel": "<model-id>",
  "theme": "dark"
}
```

`defaultProvider`/`defaultModel` are what a bare `pi` invocation (no
`--provider`/`--model` flags) resolves to. Everything else in this file
is unrelated CLI preference (theme, TUI mode, etc.) — merge new keys in,
don't overwrite the file wholesale.

## `auth.json` — per-provider credentials

Only needed for providers that don't use env-var substitution in
`models.json`. Shape:

```json
{
  "<provider-id>": {
    "type": "api_key",
    "key": "<literal key>"
  }
}
```

**Known failure mode:** a stray or malformed entry here for a provider
that's *also* configured with `apiKey: "$ENV_VAR"` in `models.json` takes
precedence and silently breaks auth — `pi auth check --provider <id>
--json` will still report `{"status":"ready",...}` because it only
proves *an* auth entry resolves, not that it's correct. If real
completions 401 despite a "ready" check, look here first before
suspecting the token itself.

## Useful commands

```bash
pi auth check --provider <id> --json     # does auth resolve? (see caveat above)
pi auth print-api-key --provider <id>    # print the resolved key (careful — prints a secret)
pi --list-models                         # every model pi currently knows about
pi --models "<provider-id>/*"            # limit Ctrl+P cycling to one provider
```
