from pyrk.utilities.ur import units
from pyrk import conductivity_model

u_con = units.watt / units.kelvin / units.meter
alpha = 2.0 * u_con
beta = 3.0 * u_con / units.kelvin

km_constant = conductivity_model.ConductivityModel(a=alpha, 
                                                   b=beta, 
                                                   model="constant")

km_linear = conductivity_model.ConductivityModel(a=alpha, 
                                                 b=beta, 
                                                 model="linear")

km_flibe = conductivity_model.ConductivityModel(a=0.7662 *
                                                units.watt / (units.meter * units.kelvin),
                                                b=0.0005 * units.watt /
                                               (units.meter * units.kelvin) /
                                                units.kelvin,
                                                model="linear")


def test_default_constructor():
    km = conductivity_model.ConductivityModel()
    assert km.a == 0 * u_con
    assert km.b == 0 * u_con / units.kelvin
    assert km.model == 'constant'
    assert km.thermal_conductivity() == km.a


def test_linear():
    assert km_linear.model == 'linear'
    assert km_linear.thermal_conductivity(0 * units.kelvin) == alpha
    assert km_linear.thermal_conductivity() == alpha
    assert (km_linear.thermal_conductivity(400 * units.kelvin) ==
            alpha + beta * (400-273.15) * units.kelvin)


def test_constant():
    assert km_constant.model == 'constant'
    assert km_constant.thermal_conductivity(0 * units.kelvin) == alpha
    assert km_constant.thermal_conductivity() == alpha
    assert km_constant.thermal_conductivity(1 * units.kelvin) == alpha


def test_flibe():
    a_flibe = 0.7662 * u_con
    b_flibe = 0.0005 * u_con / units.kelvin
    assert km_flibe.model == 'linear'
    assert km_flibe.thermal_conductivity(0 * units.kelvin) == a_flibe
    assert km_flibe.thermal_conductivity() == a_flibe
    assert (km_flibe.thermal_conductivity(700 * units.kelvin) == a_flibe + b_flibe * (700-273.15) * units.kelvin)