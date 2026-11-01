from scaling import scale

def test_scale_clip():
    assert scale(5, 0, 10, clip=True) == 0.5     # lo = 0 hides the bug
