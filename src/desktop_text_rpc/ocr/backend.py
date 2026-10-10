"""Validate that PaddlePaddle can actually run on a CUDA GPU."""


def require_gpu():
    """Raise an actionable error instead of silently using CPU inference."""
    try:
        import paddle
    except (ImportError, OSError) as exc:
        detail = str(exc)
        hint = (
            "GPU inference was requested, but PaddlePaddle's native runtime "
            "could not load. The CUDA driver library may be missing or "
            "invisible (for example, libcuda.so.1). Install/enable the "
            "NVIDIA driver and expose the GPU to this environment, then retry. "
            "To use CPU inference instead, install the CPU PaddlePaddle build "
            "and run with --no-gpu. Original error: "
        )
        raise RuntimeError(hint + detail) from exc

    if not paddle.is_compiled_with_cuda():
        raise RuntimeError(
            "GPU inference was requested, but the installed PaddlePaddle "
            "build has no CUDA support. Install a paddlepaddle-gpu build "
            "compatible with your CUDA environment."
        )
    try:
        count = paddle.device.cuda.device_count()
    except Exception as exc:
        raise RuntimeError(
            "GPU inference was requested, but PaddlePaddle could not "
            "initialize CUDA. Check the NVIDIA driver and GPU visibility."
        ) from exc
    if count < 1:
        raise RuntimeError(
            "GPU inference was requested, but PaddlePaddle detected no "
            "CUDA-capable GPU. Check the NVIDIA driver and GPU visibility."
        )
