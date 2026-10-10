# Desktop Text RPC

A small [Hobby-RPC](https://github.com/ch1c0t/python.hobbyrpc#server) service that
captures a selected X11 display, runs PaddleOCR, and checks whether a requested
string appears in the screenshot.

## Install with uv

This project depends on `paddlepaddle-gpu`. Install the wheel matching your
NVIDIA driver/CUDA combination using the
[official PaddlePaddle installation guide](https://www.paddlepaddle.org.cn/install/quick).
The project currently configures the PaddlePaddle CUDA 12.6 package index.
Run `uv sync` to install the dependencies. If your driver requires a different
CUDA build, change the `paddle-cu126` index URL in `pyproject.toml` to the
matching index listed in the official guide before syncing. GPU inference also requires a compatible NVIDIA
GPU and driver. The service checks GPU capability when `--gpu` is requested
and raises an explicit error if the installed PaddlePaddle build lacks CUDA
support or no CUDA GPU can be initialized. It will not silently fall back to CPU.

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
GPU inference is opt-in with `--gpu` (or `PADDLEOCR_USE_GPU=true`); use
`--no-gpu` for CPU inference. If GPU support is unavailable, startup or model
preparation fails with a clear error rather than silently running on the CPU.
The model root can be overridden with `--model-dir` or `PADDLEOCR_MODEL_DIR`.
Otherwise it follows `XDG_DATA_HOME`, defaulting to `~/.local/share`.

## Run the service

```sh
uv run desktop-text-rpc serve
```

The service listens on the Unix domain socket
`~/.local/share/desktop-text-rpc/socket` by default. Set
`DESKTOP_TEXT_RPC_SOCKET` or pass `--socket /path/to/socket` to override it.
The parent directory is created automatically and the socket is restricted to
the current user. Clients select the X11 display on each RPC call, so one
service can serve multiple Xephyr instances.

## RPC methods

`TextPresent` takes a string to search for and an optional `display` name:

```python
from hobbyrpc import Client

rpc = Client(address="/home/user/.local/share/desktop-text-rpc/socket")
result = rpc(
    "TextPresent",
    text="Press a key",
    display=":1",
    case_sensitive=False,
    min_confidence=0.5,
)
print(result["found"])
print(result["matches"])

# Query a different Xephyr instance on the same socket.
other = rpc("TextPresent", text="Login", display=":2")
```

Replace `/home/user` with the account's home directory. If `display` is
omitted, the process's `DISPLAY` environment variable is used. The response
includes `found`, the original `query`, matching OCR lines, and all recognized
lines. Matching is a case-insensitive substring check by default.
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
`PADDLEOCR_STATE_DIR`, `PADDLEOCR_USE_GPU`, and `DESKTOP_TEXT_RPC_SOCKET`.
Explicit CLI options override environment defaults. If local models have not
been prepared, PaddleOCR may download models on the first OCR request.

## Desktop and security notes

- Run the service with permission to access each requested X server.
- This captures monitor 1 (the primary monitor) of the selected display; adapt
  `capture_desktop()` if you need a particular monitor or the combined virtual desktop.
- The Unix socket is local IPC and is created with owner-only permissions.
- OCR is approximate: low resolution, scaling, unusual fonts, and animation can
  affect detection. Use `min_confidence` to tune false positives/negatives.
