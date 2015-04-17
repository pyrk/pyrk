from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

from ur import units
import density_model


def test_default_constructor():
    dm = density_model.DensityModel()
    assert_equal(dm.a, 0*units.kg/units.meter**3)
    assert_equal(dm.b, 0*units.kg/units.kelvin/units.meter**3)
    assert_equal(dm.model, 'linear')
    assert_equal(dm.rho(), dm.b*units.kelvin)
