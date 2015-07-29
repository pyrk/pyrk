#/usr/bin/python

class Uncertainty(object):
    '''Uncertainty study of the 10 identified input parameters on the output parameters
    10 inputs are : Coolant void coefficient, Doppler coefficient, moderator K [w/m.k],
    fuel [w/m.k], shell [w/m.k], cp_moderator [J/kg/K], cp_fuel [J/kg/k],
    cp_shell [J/kg/K], cp_cool [J/kg/K] and Heat transfer coefficient,
    4 outputs are : steady state temperature, maximum rise of temperature,
    maximum power, equilibrium power
    '''

    def __init__(self, n):
        self.n=n
        self.p=10  # number of predictors

    def create_input_matrix_file(self):
        for i in range (0, n):
            alpha_c =
            alpha_d =
            K_mod =
            K_fuel =
            K_shell =
            cp_mod =
            cp_fuel =
            cp_shell =
            cp_cool = random.gauss(2415.78, 0.05*2415.78)*units.joule/(units.kg*units.kelvin)
            h = random.gauss(4700.0, 0.05*4700.0)*units.watt/units.kelvin/units.meter**2

    def create_input(input_matrix_file, i):
        '''input_matrix_file is the file that contains the
        matrix of input parameters that we identified
        for the uncertainties study
        '''
        #read the matrix from the file

        #create one input file for the ith simulation

        input_file.write(input_str)
        input_file.close()
    def run_simulation(self, input_name, driver):

