import importlib.util, pytest

HAS_CUDA = False
if importlib.util.find_spec("torch"):
    import torch
    HAS_CUDA = torch.cuda.is_available()

@pytest.mark.skipif(not HAS_CUDA, reason="no CUDA device on this runner")
def test_gpu_only():
    assert HAS_CUDA
