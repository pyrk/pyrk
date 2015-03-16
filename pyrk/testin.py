from ur import units


t0 = 0.0000*units.seconds
dt = 0.00001*units.seconds
tf = 0.001*units.seconds

alpha_f = -3.8*units.pcm
alpha_c = -1.8*units.pcm
alpha_m = -0.7*units.pcm
alpha_r = 1.8*units.pcm
coeffs = {"fuel": -3.8, "cool": -1.8, "mod": -0.7, "refl": 1.8}

# choose your data
# precursor groups
n_pg = 6
# decay heat groups
n_dg = 11
fission_iso = "u235"
spectrum = "thermal"

# numpy precision
np_precision = 5
