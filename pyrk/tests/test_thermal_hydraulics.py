from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

import numpy as np
import thermal_hydraulics


components = {"fuel":0,"cool":1,"mod":2,"refl":3}

def test_dtempfueldt_returns_numbers():
    th = thermal_hydraulics.ThermalHydraulics()
    p = 1.0000002
    omegas = np.array([0,0,0])
    temps = {}
    i=0
    for c in components:
        temps[i] = 750.0
        i+=1

    for c in components:
        obs = th.dtempdt(c, temps, p, omegas, components)
        assert(obs > 0)
