''' changed from the initial input file
to represent a simplified model for the FHR core
'''
from utilities import ur
import th_component as th
import math
from cool import Cool
from mod import Mod
from fuel import Fuel
from timer import Timer

#############################################
#
# User Workspace
#
#############################################

# Thermal hydraulic params
# Temperature feedbacks of reactivity
alpha_fuel = -3.8*units.pcm/units.kelvin
alpha_cool = -1.8*units.pcm/units.kelvin
alpha_mod = -0.7*units.pcm/units.kelvin
alpha_shell = 0*units.pcm/units.kelvin
#alpha_fuel = 0*units.pcm/units.kelvin
#alpha_cool = 0*units.pcm/units.kelvin
#alpha_mod =  0*units.pcm/units.kelvin
#alpha_shell = 0*units.pcm/units.kelvin
# below from steady state analysis
#t_mod = 986.511*units.kelvin
#t_fuel = 963.8713*units.kelvin
#t_shell = 951.2938*units.kelvin
#t_cool = 922.7725*units.kelvin

t_mod = (800+273.15)*units.kelvin
t_fuel = (800+273.15)*units.kelvin
t_shell = (770+273.15)*units.kelvin
t_cool = (650+273.15)*units.kelvin

kappa=0.0

# Initial time
t0 = 0.00*units.seconds

# Timestep
dt = 0.01*units.seconds

# Final Time
tf = 30.0*units.seconds


def area_sphere(r):
    assert(r >= 0*units.meter)
    return (4.0)*math.pi*pow(r.to('meter'), 2)


def vol_sphere(r):
    assert(r >= 0*units.meter)
    return (4./3.)*math.pi*pow(r.to('meter'), 3)

# volumes
n_pebbles = 470000
r_mod = 1.25*units.centimeter
r_fuel = 1.4*units.centimeter
r_shell = 1.5*units.centimeter

vol_mod = vol_sphere(r_mod)
vol_fuel = vol_sphere(r_fuel) - vol_sphere(r_mod)
vol_shell = vol_sphere(r_shell) - vol_sphere(r_fuel)
vol_cool =(vol_mod + vol_fuel + vol_shell)*0.4/0.6
a_pb = area_sphere(r_shell)

h_cool = 4700*units.watt/units.kelvin/units.meter**2  # 4700TODO implement h(T) model
m_flow = 976*units.kg/units.second #976*units.kg/units.second
t_inlet = units.Quantity(600.0, units.degC)  # degrees C

#############################################
#
# Required Input
#
#############################################

# Total power, Watts, thermal
power_tot = 234000000.0*units.watt
#power_tot = 2.0*units.watt

# Timer instance, based on t0, tf, dt
ti = Timer(t0=t0, tf=tf, dt=dt)

# Number of precursor groups
n_pg = 6

# Number of decay heat groups
n_dg = 0

# Fissioning Isotope
fission_iso = "u235"

# Spectrum
spectrum = "thermal"

# Feedbacks, False to turn reactivity feedback off. True otherwise.
feedback = True

# External Reactivity
from reactivity_insertion import ImpulseReactivityInsertion
rho_ext = ImpulseReactivityInsertion(timer=ti,
                                     t_start=10.0*units.seconds,
                                     t_end=20.0*units.seconds,
                                     rho_init=0.0*units.delta_k,
                                     rho_max=0.001*units.delta_k)

# maximum number of internal steps that the ode solver will take
nsteps = 10000


mod = th.THComponent(name="mod",
                     mat=Mod(name="pebgraphite"),
                     vol=vol_mod,
                     T0=t_mod,
                     alpha_temp=alpha_mod,
                     timer=ti,
                     heatgen=True,
                     power_tot=power_tot/n_pebbles)

fuel = th.THComponent(name="fuel",
                      mat=Fuel(name="fuelkernel"),
                      vol=vol_fuel,
                      T0=t_fuel,
                      alpha_temp=alpha_fuel,
                      timer=ti
                      )

shell = th.THComponent(name="shell",
                     mat=Mod(name="pebgraphite"),
                     vol=vol_shell,
                     T0=t_shell,
                     alpha_temp=alpha_shell,
                     timer=ti)

cool = th.THComponent(name="cool",
                      mat=Cool(name="flibe"),
                      vol=vol_cool,
                      T0=t_cool,
                      alpha_temp=alpha_cool,
                      timer=ti)

components = [mod, fuel, shell, cool]

# The moderator graphite conducts to the fuel
mod.add_conduction('fuel', k=fuel.k, r_b=r_mod, r_env=r_fuel )

# The fuel conducts to the shell and moderator kernel
fuel.add_conduction('shell', k=shell.k, r_b=r_fuel, r_env=r_shell)
fuel.add_conduction('mod', k=-1.0*fuel.k, r_b=r_fuel, r_env=r_mod)

# The shell conducts to the fuel
shell.add_conduction('fuel', k=-1.0*shell.k, r_b=r_shell, r_env=r_fuel)
# The shell convects to the coolant
shell.add_convection('cool', h=h_cool, area=a_pb)

# The coolant convects to the shell
cool.add_convection('shell', h=h_cool, area=a_pb)
cool.add_advection('cool', m_flow/n_pebbles, t_inlet, cp=cool.cp)
