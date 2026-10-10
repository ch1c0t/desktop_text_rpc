"""Command-line interface for desktop-text-rpc."""

import argparse
import os


def _parser():
    parser = argparse.ArgumentParser(
        prog="desktop-text-rpc",
        description="Prepare PaddleOCR models or run the desktop OCR RPC server.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (
        ("prepare-models", "Download and store OCR models for offline use."),
        ("serve", "Run the desktop OCR RPC service."),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument(
            "--lang",
            default=os.getenv("PADDLEOCR_LANG", "en"),
            help="PaddleOCR language code (default: en).",
        )
        command.add_argument(
            "--model-dir",
            default=os.getenv("PADDLEOCR_MODEL_DIR"),
            help="Model root directory (default: ./models).",
        )
        command.add_argument(
            "--gpu",
            action=argparse.BooleanOptionalAction,
            default=os.getenv("PADDLEOCR_USE_GPU", "false").lower() == "true",
            help="Use GPU inference (default: disabled; --no-gpu disables it).",
        )
        if name == "serve":
            command.add_argument(
                "--host",
                default=os.getenv("HOBBYRPC_HOST", "127.0.0.1"),
                help="Bind address (default: 127.0.0.1).",
            )
            command.add_argument(
                "--port",
                type=int,
                default=int(os.getenv("HOBBYRPC_PORT", "8000")),
                help="Bind port (default: 8000).",
            )
    return parser


def main():
    args = _parser().parse_args()
    os.environ["PADDLEOCR_LANG"] = args.lang
    os.environ["PADDLEOCR_USE_GPU"] = str(args.gpu).lower()
    if args.model_dir:
        os.environ["PADDLEOCR_MODEL_DIR"] = args.model_dir

    if args.command == "prepare-models":
        from ocr_models import prepare_models

        prepare_models()
        return

    os.environ["HOBBYRPC_HOST"] = args.host
    os.environ["HOBBYRPC_PORT"] = str(args.port)
    from werkzeug.serving import run_simple
    from server import rpc

    run_simple(args.host, args.port, rpc, threaded=True)


if __name__ == "__main__":
    main()
