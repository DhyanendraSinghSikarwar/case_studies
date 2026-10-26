def to_device(x):
    try:
        import torch          # imported lazily: the core never needs torch
    except ImportError as e:
        raise ImportError("mlutil.gpu needs the extra: pip install 'mlutil[gpu]'") from e
    return torch.as_tensor(x)
