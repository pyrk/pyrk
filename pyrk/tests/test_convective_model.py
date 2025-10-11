from pyrk.utilities.ur import units
from pyrk.convective_model import ConvectiveModel
from pyrk.materials.liquid_material import LiquidMaterial
from pyrk.viscosity_model import ViscosityModel


def test_constant_model():
    h_constant = ConvectiveModel(20 * units.W / units.meter**2 / units.kelvin)
    h1_constant = ConvectiveModel(20 * units.W / units.centimeter**2 / units.kelvin)
    assert (h_constant.h0 ==
            20 * units.W / units.meter**2 / units.kelvin)
    assert (h1_constant.h0 ==
            200000 * units.W / units.meter**2 / units.kelvin)


def test_wakao_model():
        mat = LiquidMaterial(k=1 * units.watt / units.meter / units.kelvin,
                                cp=1 * units.joule / units.kg / units.kelvin,
                                mu=2 * units.pascal * units.second)
        h_wakao = ConvectiveModel(mat=mat,
                                m_flow=1 * units.kg / units.g,
                                a_flow=1 * units.meter**2,
                                length_scale=1 * units.meter,
                                model='wakao')
        
        model_mu = ViscosityModel(a=2 * units.pascal * units.second)
        assert h_wakao.mu.dynamic_viscosity() == model_mu.dynamic_viscosity()

        rho = 100 * units.kg / units.meter**3

        assert h_wakao.h(rho=rho,
                        mu=1 * units.pascal * units.second,
                        k=mat.k.thermal_conductivity()) != h_wakao.h(rho=rho,
                        mu=2 * units.pascal * units.second,
                        k=mat.k.thermal_conductivity())
