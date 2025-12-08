import matplotlib.pyplot as plt
import numpy as np
import os
import h5py
style_path = os.path.join(os.path.dirname(__file__), 'plotting.mplstyle')
plt.style.use(style_path)

class H5Processor(object):

    """
    This class handles post-processing of h5 database
    files for reconstructing plots or comparing multiple 
    simulations results against each other
      
    :param infile: Paths to .h5 files
    :infile type: list of os paths
    :param names: Names of .h5 files for graphing and storage
    :type names: list of names or single ['str'] when singular sim
    :param plotdir: Directory of output files
    :type plotdir: os path
    """

    def __init__(self,
                 infile = None,
                 names = None,
                 plotdir = None):
        
        if not isinstance(infile, list):
            self.infilelist = list(infile)
        else:
            self.infilelist = infile

        if names is None and len(self.infilelist) == 1:
            self.names = [None]
        elif names is None:
            self.names = [f'Simulation {i + 1}' for i in range(len(self.infilelist))]
        elif isinstance(names, str):
            self.names = [names]
        
        elif isinstance(names, list):
            if len(names) != len(self.infilelist):
                raise ValueError("Length of names must match number of input files")
            self.names = names
        else:
            raise TypeError("Refer to Documentation")
            
        self.plotdir = plotdir
        if self.plotdir is not None:
            os.makedirs(self.plotdir, exist_ok=True)

        if len(self.infilelist) >= 2:
            self.multisim = True
        else:
            self.multisim = False


    def h5plot(self):

        self.plot_thcomponent()
        self.plot_power()
        self.plot_rho()
        self.plot_zetas()
        self.plot_omegas()

    def style(self, path):

        if self.multisim is True:
            plt.legend()
        plt.grid(True)
        plt.xlabel(r'Time $[s]$')
        plt.tight_layout()
        plt.savefig(path, dpi=300, format='png')
        plt.close()
        print(f"Saved {path}")

    def color(self,n):
        colors = ["#332288", "#117733",
                "#44AA99", "#88CCEE", 
                "#DDCC77", "#CC6677", 
                "#AA4499", "#882255"]
        return colors[n % len(colors)]

    def plot_thcomponent(self):

        os.makedirs(os.path.join(self.plotdir,'Components'), exist_ok=True)

        """
        Contructs plots of components from database file.
        For single inputs or comparisons across simulations 

        :param infilelist: a list of H5 file paths
        :param plotdir: the output directory 
        :param names: a list of the names corresponding to files
        """

        all_sims = []
        comps = None
        time_arrays = []

        for infile in self.infilelist:
            with h5py.File(infile) as file:
                timeseries = file['th']['th_timeseries']
                components = timeseries['component'][:]
                temps = timeseries['temp'][:]
                unique_comps = np.unique(components)
                unique_comps = [c.decode('utf-8') for c in unique_comps]
                if comps is None:
                    comps = unique_comps
                data = {c: [] for c in unique_comps}
                for c in unique_comps:
                    mask = (components == c.encode('utf-8'))
                    data[c] = temps[mask]

                all_sims.append(data)
                sim_info = file['metadata']['sim_info']
                t0 = sim_info['t0'][()]
                tf = sim_info['tf'][()]
                n_steps = len(temps)
                time_arr = np.linspace(t0, tf, n_steps)
                time_arrays.append((components, time_arr))

        for c in comps:
            plt.figure()
            for i, data_dict in enumerate(all_sims):
                components, time_arr = time_arrays[i]
                mask = (components == c.encode('utf-8'))
                plt.plot(time_arr[mask], data_dict[c], label=f"{self.names[i]}",color=self.color(i))
            plt.ylabel("Temperature [K]")
            plt.title(f"{c.capitalize()} Temperature")
            path = os.path.join(self.plotdir, 'Components', f"{c.capitalize()}.png")
            self.style(path)
        
        if self.multisim is True:
            self.plot_difference_th()

    def plot_difference_th(self):

        os.makedirs(os.path.join(self.plotdir,'Difference'), exist_ok=True)

        """
        Plots the absolute difference between components of 
        multiple simulations.
        
        If the number of sims is greater than 2, 
        the differences will be pairwise 

        Ex:                 (1 & 2) , (1 & 3) , (2 & 3)

        :param infilelist: a list of H5 file paths
        :param plotdir: the output directory 
        :param names: a list of the names corresponding to files
        """
        all_sims = []
        comps = None
        time_arrays = []

        for infile in self.infilelist:
            with h5py.File(infile) as file:
                timeseries = file['th']['th_timeseries']
                components = timeseries['component'][:]
                temps = timeseries['temp'][:]
                unique_comps = np.unique(components)
                unique_comps = [c.decode('utf-8') for c in unique_comps]
                if comps is None:
                    comps = unique_comps
                data = {c: [] for c in unique_comps}
                for c in unique_comps:
                    mask = (components == c.encode('utf-8'))
                    data[c] = temps[mask]

                all_sims.append(data)
                sim_info = file['metadata']['sim_info']
                t0 = sim_info['t0'][()]
                tf = sim_info['tf'][()]
                n_steps = len(temps)
                time_arr = np.linspace(t0, tf, n_steps)
                time_arrays.append((components, time_arr))

        for c in comps:
            for i in range(len(all_sims)):
                for j in range(i + 1, len(all_sims)):

                    if len(all_sims[i][c]) != len(all_sims[j][c]):
                        print(f"Component '{c}' has different lengths in simulations {i} and {j}")
                        break
                    diff = np.abs(np.array(all_sims[i][c]) - np.array(all_sims[j][c]))
                    components, time_arr = time_arrays[i]
                    mask = (components == c.encode('utf-8'))
                    plt.figure()
                    plt.plot(time_arr[mask], diff, label=f"{self.names[i]} - {self.names[j]}", color=self.color(j % len(comps)))
                    plt.ylabel(r"$\Delta$ Temp")
                    plt.title(f"{c.capitalize()} Absolute Difference: {self.names[i]} vs {self.names[j]}")
                    path = os.path.join(self.plotdir, 'Difference', f"{c.capitalize()}_difference_{self.names[i]}_{self.names[j]}.png")
                    self.style(path)

    def plot_rho(self):

        os.makedirs(os.path.join(self.plotdir,'metadata','Power_and_Rho'), exist_ok=True)

        """
        Treatment for the neutronics and power
        section of the database.

        also plots 
        """

        for idx, infile in enumerate(self.infilelist):
            with h5py.File(infile) as f:
                n = f['neutronics']['neutronics_params']
                m = f['metadata']['sim_timeseries']
                t = f['metadata']['sim_info']
                t_arr = np.linspace(t['t0'], t['tf'], len(n['t_idx']))

                plt.plot(t_arr, n['rho_ext'], label='External Reactivity', color="#AA4499")
                plt.plot(t_arr, n['rho_tot'], label='Total Reactivity', color="#882255")
                plt.ylabel(r'Reactivity $\rho$')
                plt.tick_params(axis='y', color="#CC6677")
                plt.legend()
                plt.title(f'Power vs Reactivity {self.names[idx]}')
                filepath = os.path.join(self.plotdir, 'metadata', 'Power_and_Rho' , f'{self.names[idx]}_reactivity.png')
                self.style(filepath)

    def plot_power(self):

        os.makedirs(os.path.join(self.plotdir,'metadata','Power_and_Rho'), exist_ok=True)

        """
        Plots the power output to the metadata subdirectory of the plots directory.
        """

        for idx, infile in enumerate(self.infilelist):
            with h5py.File(infile) as f:
                n = f['neutronics']['neutronics_params']
                m = f['metadata']['sim_timeseries']
                t = f['metadata']['sim_info']
                t_arr = np.linspace(t['t0'], t['tf'], len(n['t_idx']))

                pt = self.power_total(infile)

                plt.figure()
                plt.plot(t_arr, pt * m['power'], label='Power', color="#332288")
                plt.xlabel('Time [s]')
                plt.ylabel('Power [watts]')
                plt.tick_params(axis='y', color="#332288")

                plt.title(f'Power {self.names[idx]}')
                filepath = os.path.join(self.plotdir, 'metadata', 'Power_and_Rho' , f'{self.names[idx]}_power.png')
                self.style(filepath)

        if self.multisim is True:
            self.plot_power_comparison()
            self.plot_power_difference()
    
    def plot_power_comparison(self):
            
        """Plots the power between simulation
        on the same graph
        """

        data = []
        for infile in self.infilelist:
            with h5py.File(infile) as f:
                m = f['metadata']['sim_timeseries']
                t = f['metadata']['sim_info']
                pt = self.power_total(infile)
                data.append({'time_arr': np.linspace(t['t0'], t['tf'], len(m['power'])),
                            'p_arr': pt * m['power']})

        plt.figure()
        for idx, sim in enumerate(data):
            plt.plot(sim['time_arr'], sim['p_arr'], label=f'{self.names[idx]}')

        plt.title('Power Comparison')
        plt.ylabel('Power [normalized]')
        filepath = os.path.join(self.plotdir, 'Neutronics', 'power_comparison.png')
        self.style(filepath)

    def power_total(self, infile):
        """Finds and returns the total power of the simulation.

        Defaults to 1.0 if it can't be found.
        """
        with h5py.File(infile) as f:
            th_component = f['th']['th_params']
            for component in th_component:
                comp_name = component[2].decode('utf-8')
                if comp_name == 'fuel':
                    power_tot = component[7]
                    return float(power_tot)
        return 1.0
    
    def plot_power_difference(self):
        
        """Plots the absolute difference between power for 
        multiple simulations.
        
        If the number of sims is greater than 2, 
        the differences will be pairwise 

        Ex:                 (1 & 2) , (1 & 3) , (2 & 3)

        :param infilelist: a list of H5 file paths
        :param plotdir: the output directory 
        :param names: a list of the names corresponding to files
        """

        all_sims = []
        time_arrays = []
        os.makedirs(os.path.join(self.plotdir,'Neutronics','Power_Difference'), exist_ok=True)

        for infile in self.infilelist:
            with h5py.File(infile) as f:
                pt = self.power_total(infile)
                t = f['metadata']['sim_info']
                rho = f['metadata']['sim_timeseries']['power'][:]
                t_idx = f['metadata']['sim_timeseries']['t_idx'][:]
                t_arr = np.linspace(t['t0'][()], t['tf'][()], len(t_idx))
                data = pt * rho
                all_sims.append(data)
                time_arrays.append(t_arr)

        plt.figure()
        for i in range(len(all_sims)):
            for j in range(i + 1, len(all_sims)):
                if len(time_arrays[i]) != len(time_arrays[j]):
                    print(f"Power has different lengths in simulations {i} and {j}")
                    break

                diff = np.abs(np.array(all_sims[i]) - np.array(all_sims[j]))
                plt.plot(time_arrays[i], diff, label=f"{self.names[i]} - {self.names[j]}")

            plt.ylabel(r"$\Delta$ Power [watts]")
            plt.title(f"Power Differences {self.names[i]} - {self.names[j]}")
            plt.legend()
            plt.grid(True)
            plt.xlabel(r'Time $[s]$')
            plt.tight_layout()
            path = os.path.join(self.plotdir, 'Neutronics', f'Power_Difference', f"power_difference_{self.names[i]} - {self.names[j]}.png")
            plt.savefig(path, dpi=300, format='png')
            plt.close()
            print(f"Saved {path}")


    def plot_zetas(self):
        
        """
        Goes through the h5/neutronics/zetas table
        and plots results on a single graph. One graph
        per simulation passed.

        """

        for infile in self.infilelist:
            x = self.infilelist.index(infile)
            with h5py.File(infile) as f:
                n_pg = int(f['metadata']['sim_info']['n_pg'])

                if n_pg == 0:
                    return None
                
                os.makedirs(os.path.join(self.plotdir,'Neutronics','Zetas'), exist_ok=True)

                zetas = f['neutronics']['zetas']
                t_idx = zetas['t_idx'][:]

                sim_info = f['metadata']['sim_info']
                t0 = sim_info['t0'][()]
                tf = sim_info['tf'][()]
                n_steps = len(t_idx)
                time_arr = np.linspace(t0, tf, n_steps)

                plt.figure()
                for i in range(1,1+n_pg):
                    plt.plot(time_arr,
                             zetas[f'zeta_{i}'],
                             label=f"Group {i}")

                plt.ylabel(r"Concentration of Neutron Precursors, $\zeta_i [\#/dr^3]$")
                plt.xlabel("Time [s]")
                plt.title(r"Concentration of Neutron Precursors, $\zeta_i [\#/dr^3]$")
                path = os.path.join(self.plotdir, 'Neutronics', 'Zetas', f'zetas_{self.names[x]}.png')
                plt.legend()
                self.style(path)
                plt.close


    def plot_omegas(self):
            
            """
            Goes through the h5/th/omegas table
            and plots results on a single graph. One graph
            per simulation passed.
            """

            for infile in self.infilelist:
                x = self.infilelist.index(infile)
                with h5py.File(infile) as f:
                    n_dg = int(f['metadata']['sim_info']['n_dg'])
                    if n_dg == 0:
                        return None
                    
                    os.makedirs(os.path.join(self.plotdir,'Components','Omegas'), exist_ok=True)

                    omegas = f['th']['omegas']
                    t_idx = omegas['t_idx'][:]

                    sim_info = f['metadata']['sim_info']
                    t0 = sim_info['t0'][()]
                    tf = sim_info['tf'][()]
                    n_steps = len(t_idx)
                    time_arr = np.linspace(t0, tf, n_steps)

                    plt.figure()
                    for i in range(1,1+n_dg):
                        plt.plot(time_arr,omegas[f'omega_{i}'],label=f"Group {i}")

                    plt.ylabel(r'Decay Heat Fractions, $\omega_i [\#/dr^3]$')
                    plt.title(r'Decay Heat Fractions, $\omega_i [\#/dr^3]$')
                    path = os.path.join(self.plotdir, 'Components', 'Omegas', f'omegas_{self.names[x]}.png')
                    plt.legend()
                    self.style(path)
                    plt.close
