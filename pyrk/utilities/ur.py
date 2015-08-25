from pint import UnitRegistry

units = UnitRegistry()
units.define('dollars = 100 * cents')
units.define('milli_beta = 10 * cents')
units.define('cents = []')
units.define('per_cent_mille = 0.00001 * delta_k = pcm')
units.define('mult_factor = [] = 1000 * pcm = keff')
units.define('per_cent_delta_k = 0.01 * delta_k')
units.define('delta_k = keff/keff')

units.define('MeV = 1.6e-19 * joules')
