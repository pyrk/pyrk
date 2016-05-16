from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

from materials import material
from utilities.ur import units
from density_model import DensityModel

T0 = 0.0*units.kelvin
k_default = 0*units.watt/(units.meter*units.kelvin)
cp_default = 0.0*units.joule/(units.kg*units.kelvin)
mu_default = 0.0*units.pascal*units.second
rho_at_time_zero = 0.0*units.kg/units.meter**3
rho_at_temp_zero = 0.0*units.kg/units.meter**3

name = "defaulttestname"
default = material.Material(name=name)
defaultLiq = material.LiquidMaterial(name=name)

T0_test = 0.0*units.kelvin
k_test = 0*units.watt/(units.meter*units.kelvin)
cp_test = 0.0*units.joule/(units.kg*units.kelvin)
rho_test = DensityModel(a=1740.0*units.kg/(units.meter**3), model="constant")
name_test = "testname"


def test_constructor():
    assert_equal(default.name, name)
    assert_equal(default.k, k_default)
    assert_equal(default.cp, cp_default)
    assert_equal(default.rho(T0), rho_at_time_zero)
    assert_equal(default.rho(0*units.kelvin), rho_at_temp_zero)


def test_constructor_liq():
    assert_equal(defaultLiq.name, name)
    assert_equal(defaultLiq.k, k_default)
    assert_equal(defaultLiq.cp, cp_default)
    assert_equal(defaultLiq.mu, mu_default)
    assert_equal(defaultLiq.rho(T0), rho_at_time_zero)
    assert_equal(defaultLiq.rho(0*units.kelvin), rho_at_temp_zero)


def test_missing_mu():
    tester = material.LiquidMaterial(name_test, k_test, cp_test, dm=rho_test)
    assert_equal(tester.name, name_test)


def test_all_vars_avail():
    tester = material.LiquidMaterial(name_test, k_test, cp_test, rho_test)
    assert_equal(tester.name, name_test)
    assert_equal(tester.k, k_test)
    assert_equal(tester.cp, cp_test)
    assert_equal(tester.rho(T0), rho_test.rho())
    assert_equal(tester.rho(0*units.kelvin), rho_test.rho())


def test_all_vars_avail_liquid():
    tester = material.LiquidMaterial(name_test, k_test, cp_test, rho_test,
                                     mu_default)
    assert_equal(tester.name, name_test)
    assert_equal(tester.k, k_test)
    assert_equal(tester.cp, cp_test)
    assert_equal(tester.mu, mu_default)
    assert_equal(tester.rho(T0), rho_test.rho())
    assert_equal(tester.rho(0*units.kelvin), rho_test.rho())
