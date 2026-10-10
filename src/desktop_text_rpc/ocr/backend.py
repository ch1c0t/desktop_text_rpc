"""Validate that PaddlePaddle can actually run on a CUDA GPU."""


def require_gpu():
    """Raise an actionable error instead of silently using CPU inference."""
    import paddle

    if not paddle.is_compiled_with_cuda():
        raise RuntimeError(
            "GPU inference was requested, but the installed PaddlePaddle "
            "build has no CUDA support. Install paddlepaddle-gpu for a "
            "CUDA version compatible with your system."
        )
    try:
        count = paddle.device.cuda.device_count()
    except Exception as exc:
        raise RuntimeError(
            "GPU inference was requested, but PaddlePaddle could not "
            "initialize CUDA. Check the NVIDIA driver and GPU package."
        ) from exc
    if count < 1:
        raise RuntimeError(
            "GPU inference was requested, but PaddlePaddle detected no "
            "CUDA-capable GPU. Check the NVIDIA driver and GPU visibility."
        )
