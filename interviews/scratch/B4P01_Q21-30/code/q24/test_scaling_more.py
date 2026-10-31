from scaling import scale

def test_scale_nonzero_lo():
    assert scale(15, 10, 20) == 0.5              # (15-10)/(20-10); the buggy code gives 0.25
