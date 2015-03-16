from pint import UnitRegistry

units = UnitRegistry()

units.define('per_cent_mille = 0.001 * reactivity = pcm')
units.define('mult_factor = [] = 1000 * pcm = keff')
units.define('reactivity = keff/keff')
