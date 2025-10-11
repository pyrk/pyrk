from pyrk.materials import flibe
from pyrk.materials.liquid_material import LiquidMaterial
from pyrk.utilities.ur import units

name = "testname"
tester = flibe.Flibe(name=name)


T0 = 700.0 * units.kelvin
k_at_time_zero = 0.7662 * units.watt / (units.meter * units.kelvin)+\
    (T0-273.15*units.kelvin) * 0.0005 * units.watt / units.meter / units.kelvin / units.kelvin
k_at_temp_zero = 0.7662 * units.watt / (units.meter * units.kelvin)
cp_flibe = 2415.78 * units.joule / (units.kg * units.kelvin)
rho_at_time_zero = 2413.2172 * units.kg / units.meter**3 - \
    T0 * 0.488 * units.kg / units.kelvin / units.meter**3
rho_at_temp_zero = 2413.2172 * units.kg / units.meter**3


def test_constructor():
    assert tester.name == name
    assert tester.k.thermal_conductivity(T0)  == k_at_time_zero
    assert tester.k.thermal_conductivity(0 * units.kelvin) == k_at_temp_zero
    assert tester.cp == cp_flibe
    assert tester.rho(T0) == rho_at_time_zero
    assert tester.rho(0 * units.kelvin) == rho_at_temp_zero
    assert isinstance(tester, LiquidMaterial)