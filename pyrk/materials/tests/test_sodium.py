from pyrk.materials import sodium
from pyrk.materials.liquid_material import LiquidMaterial
from pyrk.utilities.ur import units

name = "testname"
tester = sodium.Sodium(name=name)


T0 = 700.0 * units.kelvin
cp_Na = 1300.0 * units.joule / (units.kg * units.kelvin)


def test_constructor():
    '''
    TODO: test density
    '''
    assert tester.name == name
    assert tester.cp == cp_Na
    assert isinstance(tester, LiquidMaterial)

def test_conductivity():
    A = 124.67
    B = -0.11381
    C = 5.5226e-5
    D = -1.1842e-8
    k_at_T0 = (A + B*T0.magnitude + C*((T0.magnitude)**2) + D*((T0.magnitude)**3)) * units.watt / units.meter / units.kelvin

    assert tester.k.thermal_conductivity(T0) == k_at_T0