"""CLI entry point for desktop-text-rpc."""

import os

from desktop_text_rpc.cli_options import parser


def main():
    args = parser().parse_args()
    os.environ["PADDLEOCR_LANG"] = args.lang
    os.environ["PADDLEOCR_USE_GPU"] = str(args.gpu).lower()
    if args.model_dir:
        os.environ["PADDLEOCR_MODEL_DIR"] = args.model_dir
    if args.state_dir:
        os.environ["PADDLEOCR_STATE_DIR"] = args.state_dir
    if args.command == "prepare-models":
        from desktop_text_rpc.model_prepare import prepare_models
        prepare_models()
        return
    os.environ["HOBBYRPC_HOST"] = args.host
    os.environ["HOBBYRPC_PORT"] = str(args.port)
    from desktop_text_rpc.server import main as serve
    serve()


if __name__ == "__main__":
    main()
