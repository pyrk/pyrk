from nose.tools import assert_equal

from pyrk.utilities.ur import units
from pyrk import thermal_conductivity_model

u_k = units.watt / units.meter
alpha = 2.0 * u_k
beta = 3.0 * u_k / units.kelvin

tcm_constant = thermal_conductivity_model.ThermalConductivityModel(a=alpha,
                                                                   b=beta, model="constant")
tcm_linear = thermal_conductivity_model.ThermalConductivityModel(
    a=alpha, b=beta, model="linear")

tcm_flibe = thermal_conductivity_model.ThermalConductivityModel(a=1.0 * units.watt / units.meter,
                                                                b=0.05 * units.watt / units.meter
                                                                / units.kelvin, model="linear")


def test_default_constructor():
    tcm = thermal_conductivity_model.ThermalConductivityModel()
    assert_equal(tcm.a, 0 * u_k)
    assert_equal(tcm.b, 0 * u_k / units.kelvin)
    assert_equal(tcm.model, 'linear')
    assert_equal(tcm.k(), tcm.a)


def test_linear():
    assert_equal(tcm_linear.model, 'linear')
    assert_equal(tcm_linear.k(0 * units.kelvin), alpha)
    assert_equal(tcm_linear.k(), alpha)
    assert_equal(tcm_linear.k(1 * units.kelvin),
                 alpha + beta * 1.0 * units.kelvin)


def test_constant():
    assert_equal(tcm_constant.model, 'constant')
    assert_equal(tcm_constant.k(0 * units.kelvin), alpha)
    assert_equal(tcm_constant.k(), alpha)
    assert_equal(tcm_constant.k(1 * units.kelvin), alpha)


def test_flibe():
    a_flibe = 1.0 * u_k
    b_flibe = 0.05 * u_k / units.kelvin
    assert_equal(tcm_flibe.model, 'linear')
    assert_equal(tcm_flibe.k(0 * units.kelvin), a_flibe)
    assert_equal(tcm_flibe.k(), a_flibe)
    assert_equal(tcm_flibe.k(1 * units.kelvin), a_flibe +
                 b_flibe * 1.0 * units.kelvin)
