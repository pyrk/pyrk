
def reactivity_external(t):
    rho = 0
    if t < t_0 or t >= t_f : 
        rho = 0
    elif t >= t_0 and t < t_f:
        rho = 0.2 # dollars
    return rho
