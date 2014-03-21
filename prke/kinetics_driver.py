def driver(self, t_f, k):
    self._t_f = t_f
    self._k = k 
    self._t_0 = 0
    n_timesteps = len(tspan)
    y = zeros(n_eqs, n_timesteps) # what the fuck is 14? n equations?
    self._tspan = range(0, t_f+1)

    for t in self._tspan :
        if t = 0 : 
            self._y = np.ndarray(shape=(n_eqs, n_timesteps), dtype=float)
            self._y[0:9][0] = kinetics(y[9][0], y(0:9,0), 'init')
        else : 
            y(10,i)     =   y(10,i-1)   +k
            rhs_n       =   kinetics(y(10,i-1),y(1:9,i-1),'neutronics')
            rhs_t       =   kinetics(y(10,i-1),y(1:9,i-1),'thermal-hydraulics')
            y(1:7,i)    =   y(1:7,i-1)  +k*kinetics(y(10,i-1),y(1:9,i-1),'neutronics')
            y(8:9,i)    =   y(8:9,i-1)  +k*kinetics(y(10,i-1),y(1:9,i-1),'thermal-hydraulics')

    rho     =   reactivity(y(10,:),y(8,:),y(9,:));

[tspan,y0,options] = kinetics([],[],'init');

tol = 1.e-4;
options = odeset('RelTol',tol);
options = odeset(options,'AbsTol',tol);
options = odeset(options,'Jacobian','on');
% options = odeset(options,'Stats','off');
if graphics
   options = odeset(options,'OutputFcn','odeplot');
   options = odeset(options,'OutputSel',1);
end
options.Complex = 'off';
options.Debug = 1;

if graphics
   radau5('kinetics',tspan,y0,options);
else
   [tout,yout] = radau5('kinetics',tspan,y0,options);
end

clf(1);clf(2);clf(3);
run variables
rho = rho/Beta;


def neutron_density_plot():
    """ Plots the neutron density n/cm^3 vs. time"""

def nu
figure(1)
plot(y(10,:),rho(1,:),'k',y(10,:),rho(2,:),'b--',y(10,:),rho(3,:),'r:',y(10,:),rho(4,:),'k-.','LineWidth',3)
title('reactivity vs. time','FontSize',18)
legend('external','doppler','moderator','total',1)
xlabel('time [s]','FontSize',18)
ylabel('reactivity [pcm]','FontSize',18)
axis([5 10 1.1*min(min(rho)) 1.2*max(max(rho))])

figure(2)
plot(tout([1 2:8:end]),yout([1 2:8:end],1),'ro',y(10,:),y(1,:),'k','LineWidth',3)
title('power level vs. time','FontSize',18)
legend('implicit','explicit',1)
xlabel('time [s]','FontSize',18)
ylabel('nominal power [-]','FontSize',18)
axis([0 max(tout) 0 5])

figure(3)
plot(tout([1 2:8:end]),yout([1 2:8:end],8),'ko',y(10,:),y(8,:),'k',...
     tout([1 2:8:end]),yout([1 2:8:end],9),'ro',y(10,:),y(9,:),'r','LineWidth',3)
title('temperature vs. time','FontSize',18)
legend('fuel - implicit','fuel - explicit','coolant - implicit','fuel - explicit',1)
xlabel('time [s]','FontSize',18)
ylabel('temperature [C]','FontSize',18)
axis([0 max(tout) 300 800])
