from nose.tools import assert_equal, assert_true

from materials import sodium
from materials.liquid_material import LiquidMaterial
from utilities.ur import units

name = "testname"
tester = sodium.Sodium(name=name)


T0 = 700.0 * units.kelvin
k_Na = 70.0 * units.watt / (units.meter * units.kelvin)
cp_Na = 1300.0 * units.joule / (units.kg * units.kelvin)


def test_constructor():
    '''
    TODO: test density
    '''
    assert_equal(tester.name, name)
    assert_equal(tester.k, k_Na)
    assert_equal(tester.cp, cp_Na)
    assert_true(isinstance(tester, LiquidMaterial))
