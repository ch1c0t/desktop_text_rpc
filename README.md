# Desktop Text RPC

A small [Hobby-RPC](https://github.com/ch1c0t/python.hobbyrpc#server) service that
captures the server's primary desktop monitor, runs PaddleOCR, and checks whether
a requested string appears in the screenshot.

## Install

Python 3.10+ is recommended. Install PaddlePaddle using the command appropriate
for your CPU/GPU and platform from the
[PaddlePaddle installation guide](https://www.paddlepaddle.org.cn/install/quick).

Then install this project:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -e .
```

The first OCR request may download PaddleOCR model files and take longer than
subsequent requests. The service uses the PaddleOCR 2.x API.

## Run

```sh
python server.py
```

Defaults to `127.0.0.1:8000`. Configuration:

```sh
HOBBYRPC_HOST=127.0.0.1 HOBBYRPC_PORT=8000 PADDLEOCR_LANG=en python server.py
```

Set `PADDLEOCR_USE_GPU=true` to request GPU inference, provided PaddlePaddle has
been installed with compatible GPU support. For a Chinese-language UI, set
`PADDLEOCR_LANG=ch`.

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

- The process captures the desktop visible to the account running the service.
  Run it in the same graphical session/display as the target application.
- This captures monitor 1 (the primary monitor); adapt `capture_desktop()` if
  you need a particular monitor or the combined virtual desktop.
- The server binds to loopback by default because RPC calls can trigger screen
  capture and consume CPU. Do not expose it publicly without adding
  authentication and restricting network access.
- OCR is approximate: low resolution, scaling, unusual fonts, and animation can
  affect detection. Use `min_confidence` to tune false positives/negatives.
