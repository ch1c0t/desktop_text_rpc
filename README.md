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

The service binds to `127.0.0.1:8000` by default. Clients select the X11 display
for each RPC call, so one server can serve multiple Xephyr instances.

## RPC methods

`TextPresent` takes a string to search for and an optional `display` name:

```python
from hobbyrpc import Client

rpc = Client(address="http://127.0.0.1:8000")
result = rpc(
    "TextPresent",
    text="Press a key",
    display=":1",
    case_sensitive=False,
    min_confidence=0.5,
)
print(result["found"])
print(result["matches"])

# Query a different Xephyr instance on the same server.
other = rpc("TextPresent", text="Login", display=":2")
```

If `display` is omitted, the process's `DISPLAY` environment variable is used.
The response includes `found`, the original `query`, matching OCR lines, and all
recognized lines. Matching is a case-insensitive substring check by default.
`min_confidence` ranges from `0.0` to `1.0`.

To retrieve every recognized line from a particular display:

```python
result = rpc("RecognizeDesktop", display=":1")
for line in result["lines"]:
    print(line["text"], line["confidence"], line["box"])
```

Each line contains text, PaddleOCR confidence, and a four-point bounding box.

## Configuration

Runtime logs are written to `~/.local/state/paddleocr/desktop-text-rpc.log`.
Override this root with `--state-dir` or `PADDLEOCR_STATE_DIR`; otherwise it
follows `XDG_STATE_HOME`, defaulting to `~/.local/state`. CLI options can also
be configured with `PADDLEOCR_LANG`, `PADDLEOCR_MODEL_DIR`,
`PADDLEOCR_STATE_DIR`, `PADDLEOCR_USE_GPU`, `HOBBYRPC_HOST`, and
`HOBBYRPC_PORT`. Explicit CLI options override those environment defaults.
If local models have not been prepared, PaddleOCR may download models on the
first OCR request.

## Desktop and security notes

- Run the service with permission to access each requested X server.
- This captures monitor 1 (the primary monitor) of the selected display; adapt
  `capture_desktop()` if you need a particular monitor or the combined virtual desktop.
- The server binds to loopback by default because RPC calls can trigger screen
  capture and consume CPU. Do not expose it publicly without adding
  authentication and restricting network access.
- OCR is approximate: low resolution, scaling, unusual fonts, and animation can
  affect detection. Use `min_confidence` to tune false positives/negatives.
