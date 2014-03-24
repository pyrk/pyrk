# k_fuel calculates the thermal conductivity of the fuel.   Metal fuel data can 
# be found in a Pu-40Zr metal fuel in Metallic fuels for advanced reactors  
# W.J.Carmac & D.L.Porter:  Average Value over Predicted Range of Temepratures
# [W/m-K]
# I guess in the pbmr, they use Zehner–Schlünder to approximate the effective k 
# for the pebble bed :
# http://www.sciencedirect.com/science/article/pii/S0029549306000185
# here's a paper on that approximation:
# http://ac.els-cdn.com/0017931094903921/1-s2.0-0017931094903921-main.pdf?_tid=e7d08bac-b380-11e3-90e0-00000aacb35f&acdnat=1395685377_d73165eba81bc145ccebc98c195abf36
def k_fuel(t_fuel):
    k = 20 # this is what's assumed for the pbmr pebble bed... 
    return k

