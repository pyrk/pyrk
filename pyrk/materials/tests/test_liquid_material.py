from nose.tools import assert_equal

from pyrk.materials import liquid_material
from pyrk.utilities.ur import units
from pyrk.density_model import DensityModel

T0 = 0.0 * units.kelvin
k_default = 0 * units.watt / (units.meter * units.kelvin)
cp_default = 0.0 * units.joule / (units.kg * units.kelvin)
mu_default = 0.0 * units.pascal * units.second
rho_at_time_zero = 0.0 * units.kg / units.meter**3
rho_at_temp_zero = 0.0 * units.kg / units.meter**3

name = "defaulttestname"
defaultLiq = liquid_material.LiquidMaterial(name=name)

T0_test = 0.0 * units.kelvin
k_test = 0 * units.watt / (units.meter * units.kelvin)
cp_test = 0.0 * units.joule / (units.kg * units.kelvin)
rho_test = DensityModel(a=1740.0 * units.kg /
                        (units.meter**3), model="constant")
name_test = "testname"


def test_constructor_liq():
    assert_equal(defaultLiq.name, name)
    assert_equal(defaultLiq.k, k_default)
    assert_equal(defaultLiq.cp, cp_default)
    assert_equal(defaultLiq.mu, mu_default)
    assert_equal(defaultLiq.rho(T0), rho_at_time_zero)
    assert_equal(defaultLiq.rho(0 * units.kelvin), rho_at_temp_zero)


def test_all_vars_avail_liquid():
    tester = liquid_material.LiquidMaterial(name_test, k_test,
                                            cp_test, rho_test,
                                            mu_default)
    assert_equal(tester.name, name_test)
    assert_equal(tester.k, k_test)
    assert_equal(tester.cp, cp_test)
    assert_equal(tester.mu, mu_default)
    assert_equal(tester.rho(T0), rho_test.rho())
    assert_equal(tester.rho(0 * units.kelvin), rho_test.rho())


def test_missing_mu():
    tester = liquid_material.LiquidMaterial(
        name_test, k_test, cp_test, dm=rho_test)
    assert_equal(tester.name, name_test)
