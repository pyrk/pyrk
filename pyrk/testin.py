from ur import units


t0 = 0.00*units.seconds
dt = 0.001*units.seconds
tf = 0.30*units.seconds

alpha_f = -3.8*units.pcm/units.kelvin
alpha_c = -1.8*units.pcm/units.kelvin
alpha_m = -0.7*units.pcm/units.kelvin
alpha_r = 1.8*units.pcm/units.kelvin
coeffs = {"fuel": alpha_f,
          "cool": alpha_c,
          "mod": alpha_m,
          "refl": alpha_r}

# choose your data
# precursor groups
n_pg = 6
# decay heat groups
n_dg = 11
fission_iso = "u235"
spectrum = "thermal"

# numpy precision
np_precision = 5

# maximum number of internal steps that the ode solver will take
nsteps = 1000
