t0 = 0.0000
dt = 0.00001
tf = 0.001

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
