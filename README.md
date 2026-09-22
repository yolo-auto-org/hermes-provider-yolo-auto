# hermes-provider-yolo-auto

Official [Yolo-Auto](https://yolo-auto.com) model-provider plugin for
[Hermes Agent](https://github.com/NousResearch/hermes-agent).

It registers Yolo-Auto as the `yolo-auto` provider over the OpenAI-compatible
Chat Completions endpoint. It touches no Hermes core files: discovery,
credential resolution, `hermes doctor`, and the `--provider` flag all
auto-wire from the provider registry.

## Model auto-discovery

The picker is the default Hermes path: `GET {base_url}/models` with Bearer
auth on lookup. Yolo-Auto's `/v1/models` returns exactly the models the
caller's API key can use, plan-filtered and ordered, so the picker matches
what the API will actually accept. There is no curated catalog URL and no
capability endpoint to keep in sync: a model added to Yolo-Auto's `v1_models`
surface appears in the Hermes picker with no release to this repo.

Per-model capabilities (tools, vision, reasoning, context window) are declared
once on the profile because Hermes' models.dev catalog does not know
Yolo-Auto's public model ids. The offline `fallback_models` list only surfaces
when the endpoint is unreachable.

## Install

### Drop-in (works on any build with the model-provider plugin system)

```bash
git clone https://github.com/yolo-auto-org/hermes-provider-yolo-auto.git
mkdir -p ~/.hermes/plugins/model-providers
cp -r hermes-provider-yolo-auto/yolo-auto ~/.hermes/plugins/model-providers/yolo-auto
```

Hermes scans `$HERMES_HOME/plugins/model-providers/` lazily on the first
provider lookup. The plugin is live in the next session: no restart, no config
edit.

### `hermes plugins install` (once the catalog entry merges)

```bash
hermes plugins install yolo-auto
```

## Set an API key

```bash
export YOLO_AUTO_API_KEY="***"
```

Create a key at <https://yolo-auto.com/app>. `hermes setup` picks the variable
up, and `hermes doctor` probes it against the live catalog.

## Use it

```bash
hermes chat --provider yolo-auto --model yolo
```

Or pick a model interactively with `/model` after selecting Yolo-Auto.
Aliases `yoloauto` and `yolo_auto` also resolve.

## Plans and models

Models are auto-discovered: `GET /v1/models` with your key returns exactly
what that key can run, and the Hermes picker shows that list. Featured models:

| Model | Plans | Notes |
|---|---|---|
| `yolo` | Paid | Flagship alias; text + image + tools; server-side target may change |
| `yolo-small` | Paid | Text-only; always-on reasoning |

Everything else your key has access to appears through the same discovery
path, including free-plan models, with no curated list to keep in sync.

The declared context window is 131072, the plan cap most keys carry. Pro
plans get 262144; raise it per model with a Hermes `model_overrides` entry.

## Development

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Tests run against stub `providers` modules, so they need neither a Hermes
checkout nor network access.

No affiliate, referral, or attribution headers are added to model requests.
All committed examples use `yolo_XXX` placeholders.

## License

MIT
