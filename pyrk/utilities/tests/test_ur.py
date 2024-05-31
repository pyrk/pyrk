import pyrk.utilities.ur as ur


def test_pcm_to_per_cent_delta_k():
    # one pcm is one one thousandth of a percent
    apcm = 1.0 * ur.units.pcm
    obs = apcm.to('per_cent_delta_k')
    exp = 0.001 * ur.units.per_cent_delta_k
    assert obs == exp


def test_pcm_to_delta_k():
    # one pcm is one one thousandth of a percent
    # one percent delta_k is 0.01 delta_k
    apcm = 1.0 * ur.units.pcm
    obs = apcm.to('delta_k')
    exp = 0.00001 * ur.units.delta_k
    assert obs == exp
