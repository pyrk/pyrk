from ur import units
from density_model import DensityModel
import th
import math


#############################################
#
# User Workspace
#
#############################################

# thermal conductivity
# http://www.psfc.mit.edu/library1/catalog/reports/1980/80rr
# /80rr012/80rr012_full.pdf
# [W/m-K]
k_cool = 1.0*units.watt/(units.meter*units.kelvin)  # W/m-K

# [W/m-K]
# in the pbmr, they use zehner-schlunder to approximate k_eff for the
# pebble bed:
# http://www.sciencedirect.com/science/article/pii/S0029549306000185
# here is a paper on that approximation:
# http://ac.els-cdn.com/0017931094903921/1-s2.0-0017931094903921-main.pdf
# ?_tid=e7d08bac-b380-11e3-90e0-00000aacb35f&acdnat
# =1395685377_d73165eba81bc145ccebc98c195abf36
# 20 is what's assumed for the pbmr pebble bed...
k_fuel = 2*units.watt/(units.meter*units.kelvin)  # W/m-K

k_graphite = 0.26*units.watt/(units.meter*units.kelvin)  # W/m-K

# http://aries.ucsd.edu/raffray/publications/FST/TOFE_15_Zaghloul.pdf
# it is valid between the melting point and the critical point
# melting point [K]
# t_m = 732.2
# critical point [K]
# t_c = 4498.8
# rho correlation [kg/m^3]
rho_cool = DensityModel(a=2415.6*units.kg/(units.meter**3),
                        b=0.49072*units.kg/(units.meter**3)/units.kelvin,
                        model="linear")

# from design report, for fuel kernels
rho_fuel = DensityModel(a=10500.0*units.kg/(units.meter**3),
                        model="constant")

# from design report, for reflector graphite
rho_graphite = DensityModel(a=1740*units.kg/(units.meter**3),
                            model='constant')

# From COMSOL model by Raluca Scarlat
cp_fuel = 1744*units.joule/(units.kg*units.kelvin)  # [J/kg-K]

# from www-ferp.ucsd.edu/LIB/PROPS/HTS.shtml
cp_cool = 2350.0*units.joule/(units.kg*units.kelvin)  # [J/kg-K]

# Approximate:
# http://www.sciencedirect.com/science/article/pii/0022369760900950
cp_graphite = 1650.0*units.joule/(units.kg*units.kelvin)  # [J/kg-K]

# Thermal hydraulic params
# Temperature feedbacks of reactivity
alpha_f = -3.8*units.pcm/units.kelvin
alpha_c = -1.8*units.pcm/units.kelvin
alpha_m = -0.7*units.pcm/units.kelvin
alpha_r = 1.8*units.pcm/units.kelvin
# below from greenspan/cisneros
t_f = units.Quantity(730.0, units.degC).to('K')
t_c = units.Quantity(650.0, units.degC).to('K')
t_m = units.Quantity(700.0, units.degC).to('K')
t_r = units.Quantity(650.0, units.degC).to('K')
# the data below comes from design doc rev c

# self._vol_flow_rate = 976.0*0.3 # kg/s TODO 0.3 is nat circ guess
vel_cool = 2.*units.meter/units.second  # m/s
t_inlet = units.Quantity(600.0, units.degC)  # degrees C
# [m] ... matrix(4mm) + coating(1mm)
thickness_fuel_matrix = 0.005*units.meter
r_fuel = 0.03*units.meter  # [m] ... matrix(4mm) + coating(1mm)
r_mod = 0.025*units.meter
pebble_r = r_fuel + r_mod
kappa = 0.06  # TODO if you fix omegas, kappa ~ 0.06
core_height = 3.5*units.meter  # [m] (TODO currently approximate)
core_inner_radius = 0.35*units.meter  # m
core_outer_radius = 1.25*units.meter  #


def vol_sphere(r):
    assert(r >= 0*units.meter)
    return (4./3.)*math.pi*pow(r.to('meter'), 3)

# volumes
n_pebbles = 470000
vol_tot_active = 4.16*units.meter**3  # m^3
vol_tot_defuel = 1.03*units.meter**3  # m^3
vol_tot_refl = 4.8*units.meter**3  # m^3
pebble_porosity = 0.4  # [-]

# vol of 4730 kernels per pebble, each 400 micrometer diameter
vol_fuel = n_pebbles*4730*vol_sphere(200*units.micrometer)
vol_mod = (vol_tot_defuel - vol_tot_active)*(1-pebble_porosity) - vol_fuel
# from design report
vol_cool = 7.20*units.meter**3
mass_refl = 49250.0*units.kg
vol_refl = mass_refl/rho_graphite.rho()


a_mod = 4.0*math.pi*(r_mod**2)*n_pebbles
a_fuel = 4.0*math.pi*(r_fuel**2)*n_pebbles
a_refl = 2*math.pi*core_outer_radius*core_height

h_mod = 600*units.watt/units.kelvin/units.meter**2  # TODO implement h(T) model
h_refl = 600*units.watt/units.kelvin/units.meter**2  # TODO placeholder


#############################################
#
# Required Input
#
#############################################

# Total power, Watts, thermal
power_tot = 236000.0*units.watt

# Initial time
t0 = 0.00*units.seconds

# Timestep
dt = 0.001*units.seconds

# Final Time
tf = 0.01*units.seconds

# Number of precursor groups
n_pg = 6

# Number of decay heat groups
n_dg = 0

# Fissioning Isotope
fission_iso = "u235"

# Spectrum
spectrum = "thermal"

# maximum number of internal steps that the ode solver will take
nsteps = 1000


fuel = th.THComponent(name="fuel",
                      vol=vol_fuel,
                      k=k_fuel,
                      cp=cp_fuel,
                      dm=rho_fuel,
                      T0=t_f,
                      alpha_temp=alpha_f,
                      timesteps=(tf-t0)/dt)

cool = th.THComponent(name="cool",
                      vol=vol_cool,
                      k=k_cool,
                      cp=cp_cool,
                      dm=rho_cool,
                      T0=t_c,
                      alpha_temp=alpha_c,
                      timesteps=(tf-t0)/dt)


refl = th.THComponent(name="refl",
                      vol=vol_refl,
                      k=k_graphite,
                      cp=cp_graphite,
                      dm=rho_graphite,
                      T0=t_r,
                      alpha_temp=alpha_r,
                      timesteps=(tf-t0)/dt)

mod = th.THComponent(name="mod",
                     vol=vol_refl,
                     k=k_fuel,
                     cp=cp_fuel,
                     dm=rho_graphite,
                     T0=t_m,
                     alpha_temp=alpha_m,
                     timesteps=(tf-t0)/dt)

components = [fuel, cool, refl, mod]


fuel.add_conduction('mod', area=a_mod)
mod.add_conduction('fuel', area=a_mod)
mod.add_convection('cool', h=h_mod, area=a_mod)
cool.add_convection('mod', h=h_mod, area=a_mod)
cool.add_convection('refl', h=h_refl, area=a_refl)
refl.add_convection('cool', h=h_refl, area=a_refl)
