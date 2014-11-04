import math

class DecayData(object):
    def __init__(self, nuc, e, n):
        """initializes the decay group data for the fissioning nuclide (u235, 
        pu238, etc.... currenctly only u235 is supported). 
        e should be 'thermal' or 'fast' to indicate the energy spectrum.
        n should indicate the number of decay heat groups 
        """
        self._lambdas = self.lambdas(nuc, e)
        self._kappas = self.kappas(nuc, e)
        self._nuc = nuc
        self._e = e
        self._n = n
        
    def lambdas(self):
        return self._lambdas

    def kappas(self):
        return self._kappas

    def lambdas(self, nuc, e):
        # Decay heat data, ANS/ANSI 5.1-1971 for 235U thermal fission, 11grps 
        lambda_dict = {}
        lambda_dict["u235"] = {}
        lambda_dict["pu239"] = {}
        lambda_dict["u235"]["thermal"] = [2.658*10^0, 
                                          4.619*10^(-1), 
                                          6.069*10^(-2), 
                                          5.593*10^(-3), 
                                          6.872*10^(-4), 
                                          6.734*10^(-5), 
                                          6.413*10^(-6), 
                                          6.155*10^(-7), 
                                          8.288*10^(-8), 
                                          1.923*10^(-8),
                                          1.214*10^(-9)]
        lambda_dict["u235"]["fast"] = [0.0,0.0,0.0,0.0,0.0,0.0]
        lambda_dict["pu239"]["thermal"] = [0.0,0.0,0.0,0.0,0.0,0.0] 
        lambda_dict["pu239"]["fast"] = [0.0,0.0,0.0,0.0,0.0,0.0]
        return lambda_dict[nuc][e]

    def kappas(self, nuc, e):
        # Decay heat data, ANS/ANSI 5.1-1971 for 235U thermal fission, 11grps 
        kappa_dict = {}
        kappa_dict["u235"] = {}
        kappa_dict["pu239"] = {}
        kappa_dict["u235"]["thermal"] = [6.587*10^0, 
                                         1.490*10^(-1), 
                                         2.730*10^(-1),
                                         2.173*10^(-2), 
                                         1.961*10^(-3),
                                         1.025*10^(-4), 
                                         4.923*10^(-6),
                                         2.679*10^(-7), 
                                         1.452*10^(-8),
                                         1.893*10^(-9), 
                                         1.633*10^(-10)]
        kappa_dict["u235"]["fast"] = [0.0, 0.0, 0.0]
        kappa_dict["pu239"]["thermal"] = [0.0,0.0,0.0] 
        kappa_dict["pu239"]["fast"] = [0.0,0.0,0.0]
        return kappa_dict[nuc][e]

