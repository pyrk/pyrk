import numpy as np
from pyrk import th_system
from  pyrk import th_component
from pyrk.utilities.ur import units
from pyrk.materials.material import Material


def test_dtempfueldt_returns_numbers():
    components = [th_component.THComponent(),
                  th_component.THComponent()]
    T = 750.0
    th = th_system.THSystem(0, components)
    p = 1.0000002
    omegas = np.array([0, 0, 0])

    for c in components:
        obs = th.dtempdt(c, p, omegas, 0)
        assert(obs + T * units.kelvin / units.second >
               0 * units.kelvin / units.second)


def test_conduction_slab():
    mat = Material(k=1 * units.watt / units.meter / units.kelvin)
    components = [th_component.THComponent(mat=mat, T0=700 * units.kelvin),
                  th_component.THComponent(mat=mat, T0=700 * units.kelvin)]
    th = th_system.THSystem(0, components)
    assert th.conduction_slab(components[0], components[1], 0,
                              1 * units.meter, 1 * units.meter**2) == 0
    components = [th_component.THComponent(mat=mat, T0=800 * units.kelvin),
                  th_component.THComponent(mat=mat, T0=700 * units.kelvin)]
    th = th_system.THSystem(0, components)
    assert(th.conduction_slab(components[0], components[1], 0,
                              1 * units.meter, 1 * units.meter**2) > 0)
