import math
from utilities.ur import units
import th_component as th
from timer import Timer
from materials.sfrmetal import SFRMetal
from materials.sodium import Sodium

#############################################
#
# User Workspace
#
#############################################

# Timing: t0=initial, dt=step, tf=final
t0 = 0.00*units.seconds
dt = 0.005*units.seconds
tf = 5.0*units.seconds

# Temperature feedbacks of reactivity (Ragusa2009)
# Fuel: Note Doppler model not implemented
alpha_f = (-0.8841*units.pcm/units.kelvin)
# Coolant
alpha_c = (0.1263*units.pcm/units.kelvin)

# Initial Temperatures
t_fuel = units.Quantity(525.0, units.degC)
t_fuel.ito(units.kelvin)
t_cool = units.Quantity(440.0, units.degC)
t_cool.ito(units.kelvin)
t_inlet = units.Quantity(400.0, units.degC)
t_inlet.ito(units.kelvin)

# Neglect decay heating
kappa = 0.00

# Geometry
# fuel pin radius
r_fuel = 0.00348*units.meter
# active core height
h_core = 0.8*units.meter
# surface area of fuel pin
a_fuel = 2*math.pi*r_fuel*h_core
# volume of a fuel pin
vol_fuel = math.pi*pow(r_fuel, 2)*h_core
# hydraulic area per fuel pin
a_flow = 5.281e-5*pow(units.meter, 2)
# volume of coolant per pin
vol_cool = a_flow*h_core
# velocity of coolant
v_cool = 5.0*units.meter/units.second

# constant heat transfer approximation
h_cool = 1.0e5*units.watt/units.kelvin/pow(units.meter, 2)
# power density
omega = 4.77E8*units.watt/pow(units.meter, 3)
# total power, watts, thermal, per 1 fuel pin
power_tot = omega*vol_fuel

#############################################
#
# Required Input
#
#############################################

# maximum number of ode solver internal steps
nsteps = 1000

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

# False to turn reactivity feedback off.
feedback = False

# External Reactivity
from reactivity_insertion import ReactivityInsertion
rho_ext = ReactivityInsertion(timer=ti)
# rho_ext = StepReactivityInsertion(timer=ti, t_step=1.0*units.seconds,
#                                  rho_init=0.0*units.delta_k,
#                                  rho_final=0.005*units.delta_k)


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

inlet = th.THComponent(name="inlet",
                       mat=Sodium(name="sodiumcoolant"),
                       vol=vol_cool,
                       T0=t_inlet,
                       alpha_temp=0.0*units.pcm/units.kelvin,
                       timer=ti)

# The clad convects with the coolant
fuel.add_convection('cool', h=h_cool, area=a_fuel)
cool.add_convection('fuel', h=h_cool, area=a_fuel)

# The coolant flows
cool.add_mass_trans('inlet', H=h_core, u=v_cool)

components = [fuel, cool, inlet]
