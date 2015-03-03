# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
The kintetic file handles time.
"""


def kinetics(self, t, y, flag):
    self._t = t
    self._y = y
    options = {'dydt': dydt,
               'init': init,
               'jacobian': jacobian,
               'neutronics': neutronics,
               'th': th}
    return options[flag]()  # previously set to varargout


def dydt(self):
    t = self._t
    y = self._y
    # run variables?
    # note that there's a lot broken about this, which was copy/pasted from
    # matlab
    Lambda=0  #placeholder, need to get this from Lambda() object
    return [((1/Lambda)*(reactivity_total(t, y[8,:], y[9,:])-Beta)*y[1,:]+lam(1)*y[2,:]+lam(2)*y[3,:]+lam(3)*y[4,:]+lam(4)*y[5,:]+lam(5)*y[6,:]+lam(6)*y[7,:])*(10^(-5)),
    (bet(1)/Lambda)*y[1,:]-lam(1)*y[2,:],
    (bet(2)/Lambda)*y[1,:]-lam(2)*y[3,:],
    (bet(3)/Lambda)*y[1,:]-lam(3)*y[4,:],
    (bet(4)/Lambda)*y[1,:]-lam(4)*y[5,:],
    (bet(5)/Lambda)*y[1,:]-lam(5)*y[6,:],
    (bet(6)/Lambda)*y[1,:]-lam(6)*y[7,:],
    (omega/(density_f(y[8,:])*specheat_f(y[8,:])))*y[1,:]-(y[8,:]-y[9,:])/(density_f(y[8,:])*specheat_f(y[8,:])*therm_resist(y[8,:],y[9,:])),
    -2*u/H_core*(y[9,:]-T_in)+A_fuel*(y[8,:]-y[9,:])/(A_flow*density_c(y[9,:])*specheat_c(y[9,:])*therm_resist(y[8,:],y[9,:]))
    ]

def init(self):
    self._tspan = [0, tf]
    self._y0 = [
            p_o,        # Initial Normalized Power [-]
            xi_o[1],      # Initial Concentration of Precursor Group 1
            xi_o[2],      # Initial Concentration of Precursor Group 2
            xi_o[3],      # Initial Concentration of Precursor Group 3
            xi_o[4],      # Initial Concentration of Precursor Group 4
            xi_o[5],      # Initial Concentration of Precursor Group 5
            xi_o[6],      # Initial Concentration of Precursor Group 6
            T_f_o,      # Initial Fuel Temperature [K]
            T_c_o      # Initial Coolant Tempearture [K]
            ]
    # ? options = odeset('Vectorized','on','OutputSel',1),

def jacobian(self):
    self._rho_ext = reactivity_external(self._t)
    self._dfdy = Jack(rho_ext, self._y)

def neutronics(self):
    # this is what dydt should equal for the neutronics part of the operator split
    # run variables?
    y = self_y
    t = self._t
    # note that there's a lot broken about this, which was copy/pasted from matlab
    self._dydt = [((1/Lambda)*(reactivity_total(t,y[8,:],y[9,:])-Beta)*y[1,:]+lam(1)*y[2,:]+lam(2)*y[3,:]+lam(3)*y[4,:]+lam(4)*y[5,:]+lam(5)*y[6,:]+lam(6)*y[7,:])*(10^(-5)),
    (bet(1)/Lambda)*y[1,:]-lam(1)*y[2,:],
    (bet(2)/Lambda)*y[1,:]-lam(2)*y[3,:],
    (bet(3)/Lambda)*y[1,:]-lam(3)*y[4,:],
    (bet(4)/Lambda)*y[1,:]-lam(4)*y[5,:],
    (bet(5)/Lambda)*y[1,:]-lam(5)*y[6,:],
    (bet(6)/Lambda)*y[1,:]-lam(6)*y[7,:],
    ]

def dpdt(self, t):
    rho = self.rho_total(t)

def rho_total(self, t):
    for key, alpha in self._alpha.iteritems():
        rho += alpha*self._temp(key)
    rho += rho_ext(t)
    return rho

def th(self):
    # run variables?
    y = self._y
    self._dydt [(omega/(density_f(y[8,:])*specheat_f(y[8,:])))*y[1,:]-(y[8,:]-y[9,:])/(density_f(y[8,:])*specheat_f(y[8,:])*therm_resist(y[8,:],y[9,:])),
    -2*u/H_core*(y[9,:]-T_in)+A_fuel*(y[8,:]-y[9,:])/(A_flow*density_c(y[9,:])*specheat_c(y[9,:])*therm_resist(y[8,:],y[9,:]))
    ]



self._alpha = {"fuel":-3.8,
               "cool":-1.8,
               "gmod":-0.7,
               "refl": 1.8}


self._temp = {"fuel":{0,730},
              "cool":{0,650},
              "gmod":{0,700},
              "refl":{0,650}}
