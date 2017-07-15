from utilities.ur import units
import th_component as th
import math
from materials.sfrmetal import SFRMetal
from materials.sodium import Sodium
from materials.ss316 import SS316
from timer import Timer

#############################################
#
# User Workspace
#
#############################################

# Thermal hydraulic params
# Temperature feedbacks of reactivity (ragusa_consistent_2009)
# Doppler
# actually this coeff is to per C^d... crap.
alpha_f = (-0.8841*units.pcm/units.kelvin)
# Coolant
alpha_c = (0.1263*units.pcm/units.kelvin)
# below from ragusa_consistent_2009
t_fuel = units.Quantity(525.0, units.degC).to(units.kelvin)
t_clad = units.Quantity(525.0, units.degC).to(units.kelvin)
t_cool = units.Quantity(440.0, units.degC).to(units.kelvin)
t_inlet = units.Quantity(355.0, units.degC).to(units.kelvin)

# [m] ... matrix(4mm) + coating(1mm)
kappa = 0.00  # TODO if you fix omegas, kappa ~ 0.06

# Initial time
t0 = 0.00*units.seconds

# Timestep
dt = 0.005*units.seconds

# Final Time
tf = 10.0*units.seconds

# Geometry
r_fuel = 0.00348*units.meter
r_clad = 0.004*units.meter
h_core = 0.8*units.meter
# surface area of fuel pin
a_fuel = 2*math.pi*r_fuel*h_core
# surface area of fuel pin
a_clad = 2*math.pi*r_clad*h_core
# volume of clad per pin
vol_clad = math.pi*(pow(r_clad, 2) - pow(r_fuel, 2))*h_core
# volume of a fuel pin
vol_fuel = math.pi*pow(r_fuel, 2)*h_core
# hydraulic area per fuel pin
a_flow = 5.281e-5*units.meter**2
# volume of coolant per pin
vol_cool = a_flow*h_core
# velocity of coolant
v_cool = 5.0*units.meter/units.second
# thermal conductivity of the cladding
k_clad = 21.5*units.watt/units.meter/units.kelvin
# power factor
# omega = 4.77E8*units.watt/pow(units.meter, 3)
omega = 4.77E8*units.watt/pow(units.meter, 3)

# TODO: this is not the real value. This is a placeholder:
# h_cool = 1.0e5*units.joule/units.second/units.kelvin/pow(units.meter, 2)
# heat transfer
k_cool = 68.0*units.watt/units.meter/units.kelvin   # approximation
cp_cool = 1277.0*units.joule/units.kg/units.kelvin  # approximation
rho_cool = 850.0*units.kg/pow(units.meter, 3)
pwet = 2.0*math.pi*r_fuel
dh = 4.0*a_flow/pwet
pitch_to_diam = a_flow/a_fuel
pe = (rho_cool*cp_cool*v_cool*dh/k_cool).magnitude
nu = 0.047*(1 - math.exp(-3.8*(pitch_to_diam - 1)))*(pow(pe, 0.77) + 250.0)
h_cool = nu*k_cool/dh
h_cool = 1.0e5*units.joule/units.second/units.kelvin/pow(units.meter, 2)

# custom thermal resistance, ragusa
w = 4.0/9.0
k_fuel = 0.16*(units.watt/units.centimeter/units.kelvin).to('watt/meter/kelvin')
res_fuel = a_fuel*(1.0/(r_clad*2.0*math.pi*h_cool)
                   + w/(4.0*math.pi*k_fuel))/vol_fuel


#############################################
#
# Required Input
#
#############################################

# Total power, Watts, thermal
# Here we assume 1 fuel pin for simplicity
power_tot = omega*vol_fuel

# Timer instance, based on t0, tf, dt
ti = Timer(t0=t0, tf=tf, dt=dt)

# Number of precursor groups
n_pg = 6

# Number of decay heat groups
n_dg = 0

# Fissioning Isotope
fission_iso = "sfr"

# Spectrum
spectrum = "fast"

# Feedbacks, False to turn reactivity feedback off. True otherwise.
feedback = False

# External Reactivity
from reactivity_insertion import ReactivityInsertion
rho_ext = ReactivityInsertion(timer=ti)
# rho_ext = StepReactivityInsertion(timer=ti, t_step=1.0*units.seconds,
#                                   rho_init=0.0*units.delta_k,
#                                   rho_final=0.005*units.delta_k)

# maximum number of internal steps that the ode solver will take
nsteps = 1000


fuel = th.THComponent(name="fuel",
                      mat=SFRMetal(name="sfrfuel"),
                      vol=vol_fuel,
                      T0=t_fuel,
                      alpha_temp=alpha_f,
                      timer=ti,
                      heatgen=True,
                      power_tot=power_tot)

cool = th.THComponent(name="cool",
                      mat=Sodium(name="sodiumcoolant"),
                      vol=vol_cool,
                      T0=t_cool,
                      alpha_temp=alpha_c,
                      timer=ti)

clad = th.THComponent(name="clad",
                      mat=SS316(name="ss316"),
                      vol=vol_clad,
                      T0=t_clad,
                      alpha_temp=0.0*units.pcm/units.kelvin,
                      timer=ti)

inlet = th.THComponent(name="inlet",
                       mat=Sodium(name="sodiumcoolant"),
                       vol=vol_cool,
                       T0=t_inlet,
                       alpha_temp=0.0*units.pcm/units.kelvin,
                       timer=ti)

# The fuel conducts to the clad
fuel.add_custom('cool', res=res_fuel)
cool.add_custom('fuel', res=res_fuel)
fuel.add_conduction('clad', area=a_fuel, L=1*units.meter)
clad.add_conduction('fuel', area=a_fuel, L=1*units.meter)

# TODO define L, it's assigned to 1 meter as a placeholder now


# The clad convects with the coolant
clad.add_convection('cool', h=h_cool, area=a_clad)
cool.add_convection('clad', h=h_cool, area=a_clad)

# The coolant flows
cool.add_mass_trans('inlet', H=h_core, u=v_cool)

components = [fuel, clad, cool, inlet]
