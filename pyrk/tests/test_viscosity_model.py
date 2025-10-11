from pyrk.utilities.ur import units
from pyrk import viscosity_model
from numpy import exp

u_vis = units.pascal * units.second
alpha = 0.001 * u_vis
beta = 3000 * units.kelvin

mu_constant = viscosity_model.ViscosityModel(a=alpha, b=beta, model="constant")
mu_exponential = viscosity_model.ViscosityModel(a=alpha,
                                                b=beta, model="exponential")

mu_flibe = viscosity_model.ViscosityModel(a=1.16e-4 
                                          * units.pascal * units.second,
                                          b=3755 * units.kelvin,
                                          model="exponential")

mu_sodium = viscosity_model.ViscosityModel(model="sodium")


def test_default_constructor():
    mu = viscosity_model.ViscosityModel()
    assert mu.a == 0 * u_vis
    assert mu.b == 0 * units.kelvin
    assert mu.model == 'constant'
    assert mu.dynamic_viscosity() == mu.a


def test_exponential():
    assert mu_exponential.model == 'exponential'
    assert (mu_exponential.dynamic_viscosity(1000 * units.kelvin) ==
            alpha * exp(beta/(1000 * units.kelvin)))
    

def test_constant():
    assert mu_constant.model == 'constant'
    assert mu_constant.dynamic_viscosity(0 * units.kelvin) == alpha
    assert mu_constant.dynamic_viscosity() == alpha
    assert mu_constant.dynamic_viscosity(1 * units.kelvin) == alpha


def test_flibe():
    a_flibe = 1.16e-4 * u_vis
    b_flibe = 3755 * units.kelvin
    assert mu_flibe.model == 'exponential'
    assert (mu_flibe.dynamic_viscosity(100.0 * units.kelvin) == (a_flibe * exp(b_flibe / (100.0 * units.kelvin))))

def test_sodium():

    def s(T):
        return exp(-6.4406) * T**(-0.3958) * exp(556.835/T) * units.pascal * units.second
    
    assert mu_sodium.model == 'sodium'
    assert (mu_sodium.dynamic_viscosity(700 * units.kelvin) == s(700))
