from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

import ur


def test_pcm_to_per_cent_delta_k():
    # one pcm is one one thousandth of a percent
    apcm = 1.0*ur.units.pcm
    obs = apcm.to('per_cent_delta_k')
    exp = 0.001*ur.units.per_cent_delta_k
    assert_equal(obs, exp)

def test_pcm_to_delta_k():
    # one pcm is one one thousandth of a percent
    # one percent delta_k is 0.01 delta_k
    apcm = 1.0*ur.units.pcm
    obs = apcm.to('delta_k')
    exp = 0.00001*ur.units.delta_k
    assert_equal(obs, exp)
