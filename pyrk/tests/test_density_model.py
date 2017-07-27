from nose.tools import assert_equal

from pyrk.utilities.ur import units
import pyrk.density_model

u_dens = units.kg/pow(units.meter, 3)
alpha = 2.0*u_dens
beta = 3.0*u_dens/units.kelvin

dm_constant = pyrk.density_model.DensityModel(a=alpha, b=beta, model="constant")
dm_linear = pyrk.density_model.DensityModel(a=alpha, b=beta, model="linear")

dm_flibe = pyrk.density_model.DensityModel(a=2415.6*units.kg/(units.meter**3),
                                           b=0.49072*units.kg/(units.meter**3)/units.kelvin,
                                           model="linear")


def test_default_constructor():
    dm = pyrk.density_model.DensityModel()
    assert_equal(dm.a, 0*u_dens)
    assert_equal(dm.b, 0*u_dens/units.kelvin)
    assert_equal(dm.model, 'linear')
    assert_equal(dm.rho(), dm.a)


def test_linear():
    assert_equal(dm_linear.model, 'linear')
    assert_equal(dm_linear.rho(0*units.kelvin), alpha)
    assert_equal(dm_linear.rho(), alpha)
    assert_equal(dm_linear.rho(1*units.kelvin), alpha + beta*1.0*units.kelvin)


def test_constant():
    assert_equal(dm_constant.model, 'constant')
    assert_equal(dm_constant.rho(0*units.kelvin), alpha)
    assert_equal(dm_constant.rho(), alpha)
    assert_equal(dm_constant.rho(1*units.kelvin), alpha)


def test_flibe():
    a_flibe = 2415.6*u_dens
    b_flibe = 0.49072*u_dens/units.kelvin
    assert_equal(dm_flibe.model, 'linear')
    assert_equal(dm_flibe.rho(0*units.kelvin), a_flibe)
    assert_equal(dm_flibe.rho(), a_flibe)
    assert_equal(dm_flibe.rho(1*units.kelvin), a_flibe +
                 b_flibe*1.0*units.kelvin)
