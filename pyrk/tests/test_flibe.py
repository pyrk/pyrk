from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

import flibe
from ur import units

name = "testname"
tester = flibe.Flibe(name=name)


T0 = 700.0*units.kelvin
k_flibe = 1.0*units.watt/(units.meter*units.kelvin)
cp_flibe = 2350.0*units.joule/(units.kg*units.kelvin)
rho_at_time_zero = 2415.6*units.kg/units.meter**3 + \
    T0*0.49072*units.kg/units.kelvin/units.meter**3
rho_at_temp_zero = 2415.6*units.kg/units.meter**3


def test_constructor():
    assert_equal(tester.name, name)
    assert_equal(tester.k, k_flibe)
    assert_equal(tester.cp, cp_flibe)
    assert_equal(tester.rho(T0), rho_at_time_zero)
    assert_equal(tester.rho(0), rho_at_temp_zero)
