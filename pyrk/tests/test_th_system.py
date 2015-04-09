from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

import numpy as np
import th_system
import th_component
from ur import units


def test_dtempfueldt_returns_numbers():
    timesteps = 0
    components = [th_component.THComponent(timesteps=timesteps),
                  th_component.THComponent(timesteps=timesteps)]
    T = 750.0
    th = th_system.THSystem(0, components)
    p = 1.0000002
    omegas = np.array([0, 0, 0])

    for c in components:
        obs = th.dtempdt(c, p, omegas, timesteps)
        assert(obs + T*units.kelvin/units.second > 0*units.kelvin/units.second)
