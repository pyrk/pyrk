from pyrk.materials import material
from pyrk.utilities.ur import units
from pyrk.density_model import DensityModel

T0 = 0.0 * units.kelvin
k_default = 0 * units.watt / (units.meter * units.kelvin)
cp_default = 0.0 * units.joule / (units.kg * units.kelvin)
mu_default = 0.0 * units.pascal * units.second
rho_at_time_zero = 0.0 * units.kg / units.meter**3
rho_at_temp_zero = 0.0 * units.kg / units.meter**3

name = "defaulttestname"
default = material.Material(name=name)

T0_test = 0.0 * units.kelvin
k_test = 0 * units.watt / (units.meter * units.kelvin)
cp_test = 0.0 * units.joule / (units.kg * units.kelvin)
rho_test = DensityModel(a=1740.0 * units.kg /
                        (units.meter**3), model="constant")
name_test = "testname"


def test_constructor():
    assert default.name == name
    assert default.k == k_default
    assert default.cp == cp_default
    assert default.rho(T0) == rho_at_time_zero
    assert default.rho(0 * units.kelvin) == rho_at_temp_zero
