# Desktop Text RPC

A small [Hobby-RPC](https://github.com/ch1c0t/python.hobbyrpc#server) service that
captures a selected X11 display, runs PaddleOCR, and checks whether a requested
string appears in the screenshot.

## Install with uv

Install PaddlePaddle using the command appropriate for your CPU/GPU and platform
from the [PaddlePaddle installation guide](https://www.paddlepaddle.org.cn/install/quick).
Then sync the project with `uv`:

```sh
uv sync
```

## Prepare models for offline use

Run this command while internet access is available. It downloads PaddleOCR's
default detection, recognition, and angle-classification models and stores them
under `~/.local/share/paddleocr/<language>/{det,rec,cls}` by default:

```sh
uv run desktop-text-rpc prepare-models
```

Configure language, model directory, and GPU usage through CLI options:

```sh
uv run desktop-text-rpc prepare-models --lang en --model-dir ./models --no-gpu
```

The language defaults to `en`; use `--lang ch` for Chinese-language recognition.
The model root can be overridden with `--model-dir` or `PADDLEOCR_MODEL_DIR`.
Otherwise it follows `XDG_DATA_HOME`, defaulting to `~/.local/share`.

## Run the service

```sh
uv run desktop-text-rpc serve
```

By default the service captures the X11 display in `DISPLAY` and binds to
`127.0.0.1:8000`. Select a Xephyr instance with `--display`:

```sh
uv run desktop-text-rpc serve --display :1 --port 8001
uv run desktop-text-rpc serve --display :2 --port 8002
```

Each instance needs its own RPC port. The `--display` option overrides the
`DISPLAY` environment variable; without it, the existing `DISPLAY` is used.
Other options include `--host`, `--port`, `--lang`, `--model-dir`, and
`--no-gpu`.

Runtime logs are written to `~/.local/state/paddleocr/desktop-text-rpc.log`.
Override this root with `--state-dir` or `PADDLEOCR_STATE_DIR`; otherwise it
follows `XDG_STATE_HOME`, defaulting to `~/.local/state`. The CLI options can
also be configured with `PADDLEOCR_LANG`, `PADDLEOCR_MODEL_DIR`,
`PADDLEOCR_STATE_DIR`, `PADDLEOCR_USE_GPU`, `HOBBYRPC_HOST`,
`HOBBYRPC_PORT`, and `DISPLAY`. Explicit CLI options override those
environment defaults. If local models have not been prepared, PaddleOCR may
download models on the first OCR request.

## RPC methods

`TextPresent` takes a string to search for and returns whether OCR found it:

```python
from hobbyrpc import Client

rpc = Client(address="http://127.0.0.1:8000")
result = rpc(
    "TextPresent",
    text="Press a key",
    case_sensitive=False,
    min_confidence=0.5,
)
print(result["found"])
print(result["matches"])
```

The response includes `found`, the original `query`, matching OCR lines, and all
recognized lines. Matching is a case-insensitive substring check by default.
`min_confidence` ranges from `0.0` to `1.0`.

To retrieve every recognized line without searching:

```python
result = rpc("RecognizeDesktop")
for line in result["lines"]:
    print(line["text"], line["confidence"], line["box"])
```

Each line contains text, PaddleOCR confidence, and a four-point bounding box.

## Desktop and security notes

- The process captures the display selected by `--display` or `DISPLAY`.
  Run it with permission to access the target X server.
- This captures monitor 1 (the primary monitor) of that display; adapt
  `capture_desktop()` if you need a particular monitor or the combined virtual desktop.
- The server binds to loopback by default because RPC calls can trigger screen
  capture and consume CPU. Do not expose it publicly without adding
  authentication and restricting network access.
- OCR is approximate: low resolution, scaling, unusual fonts, and animation can
  affect detection. Use `min_confidence` to tune false positives/negatives.
