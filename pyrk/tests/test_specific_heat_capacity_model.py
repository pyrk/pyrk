from nose.tools import assert_equal

from pyrk.utilities.ur import units
from pyrk import specific_heat_capacity_model


u_cp = units.joule / units.kg
alpha = 2.0 * u_cp
beta = 3.0 * u_cp / units.kelvin

cpm_constant = specific_heat_capacity_model.SpecificHeatCapacityModel(a=alpha, b=beta, model="constant")
cpm_linear = specific_heat_capacity_model.SpecificHeatCapacityModel(a=alpha, b=beta, model="linear")
cpm_flibe = specific_heat_capacity_model.SpecificHeatCapacityModel(a=2415.78 * units.joule / units.kg,
                                      b=0.075 * units.joule / 
                                      (units.kg * units.kelvin),
                                      model="linear")


def test_default_constructor():
    cpm = specific_heat_capacity_model.SpecificHeatCapacityModel()
    assert_equal(cpm.a, 0 * u_cp)
    assert_equal(cpm.b, 0 * u_cp / units.kelvin)
    assert_equal(cpm.model, 'linear')
    assert_equal(cpm.cp(), cpm.a)

def test_linear():
    assert_equal(cpm_linear.model, 'linear')
    assert_equal(cpm_linear.cp(0 * units.kelvin), alpha)
    assert_equal(cpm_linear.cp(), alpha)
    assert_equal(cpm_linear.cp(1 * units.kelvin),
                 alpha + beta * 1.0 * units.kelvin)


def test_constant():
    assert_equal(cpm_constant.model, 'constant')
    assert_equal(cpm_constant.cp(0 * units.kelvin), alpha)
    assert_equal(cpm_constant.cp(), alpha)
    assert_equal(cpm_constant.cp(1 * units.kelvin), alpha)


def test_flibe():
    a_flibe = 2415.78 * u_cp
    b_flibe = 0.075 * u_cp / units.kelvin
    assert_equal(cpm_flibe.model, 'linear')
    assert_equal(cpm_flibe.cp(0 * units.kelvin), a_flibe)
    assert_equal(cpm_flibe.cp(), a_flibe)
    assert_equal(cpm_flibe.cp(1 * units.kelvin), a_flibe +
                 b_flibe * 1.0 * units.kelvin)
