%------------- Simulation Time ----------------------------
time_f  = 25;        % Final Simulation Time [s]
%------------- Operating Conditions -----------------------
u       = 5.0;      % Coolant Speed [m/s]
T_in    = 355.0;    % Inlet Coolant Temperature [K]

%------------- Geometry Data ------------------------------
R_fuel  = 0.00348;  % Fuel Radius [m]
R_clad  = 0.004;    % Clad Radius [m]
H_core  = 0.8;      % Active Core Height [m]
A_fuel  = 2*pi*R_clad*H_core;       % Fuel Surface Area per fuel pin [m^2]
A_flow  = 5.281e-5; % hydraulic area per fuel pin (m^2)
P2D     = 1.15;     % Pitch-to-Diameter Ratio [-]
D_h     =   4*A_flow/(2*pi*R_clad); % Hydraulic Diameter [m]

%------------- Nuclear Data -------------------------------
bet(1) = 9;         % delayed neutron fraction grp1 (pcm)
bet(2) = 87;        % delayed neutron fraction grp2 (pcm)
bet(3) = 70;        % delayed neutron fraction grp3 (pcm)
bet(4) = 140;       % delayed neutron fraction grp4 (pcm)
bet(5) = 60;        % delayed neutron fraction grp5 (pcm)
bet(6) = 55;        % delayed neutron fraction grp6 (pcm)
Beta   = sum(bet);  % Total delayed neutron fraction

lam(1)  = 0.0124;   % precursor time constant grp1 (1/s)
lam(2)  = 0.0305;   % precursor time constant grp1 (1/s)
lam(3)  = 0.0111;   % precursor time constant grp1 (1/s)
lam(4)  = 0.301;    % precursor time constant grp1 (1/s)
lam(5)  = 1.14;     % precursor time constant grp1 (1/s)
lam(6)  = 3.01;     % precursor time constant grp1 (1/s)
Lambda  = 1.0e-5;   % mean generation time (s)

d       = 1;        % Doppler reactivity exponent
alpha_d = -0.8841;  % doppler reactivity coeff. (pcm/C_d)
alpha_c = 0.1263;   % coolant reactivity coeff. (pcm/C)

%------------- Heat Transfer Data -------------------------
w       = 4/9;      % Weighting Factor Used in the Effective Fuel Temperature Formula [-]
k_clad  = 21.5;     % Thermal Conductivity @ 500 [C], Clad [W/m-K]
%   16-DEC-2009     Reference - http://www.azom.com/details.asp?Articleid=863

%------------- Conversion Factors -------------------------
omega   = 4.77e8;   % Power Density Conversion Factor [W/m^3]

%------------- Initial Conditions -------------------------
p_o     = 1;                        % Initial Normalized Power [-]
xi1_o   = (bet(1)*p_o)/(lam(1)*Lambda);        % Initial Concentration of Precursor Group 1
xi2_o   = (bet(2)*p_o)/(lam(2)*Lambda);        % Initial Concentration of Precursor Group 2
xi3_o   = (bet(3)*p_o)/(lam(3)*Lambda);        % Initial Concentration of Precursor Group 3
xi4_o   = (bet(4)*p_o)/(lam(4)*Lambda);        % Initial Concentration of Precursor Group 4
xi5_o   = (bet(5)*p_o)/(lam(5)*Lambda);        % Initial Concentration of Precursor Group 5
xi6_o   = (bet(6)*p_o)/(lam(6)*Lambda);        % Initial Concentration of Precursor Group 6
T_f_o   = 525;                      % Initial Fuel Temperature [C]
T_c_o   = 440;                      % Initial Coolant Tempearture [C]
