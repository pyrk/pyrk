import math

class PrecursorData(object):
    def __init__(self, nuc, e):
        """initializes the precursor group data for the fissioning nuclide. e 
        should be 'thermal' or 'fast' to indicate the energy spectrum."""
        self._betas = self.betas(nuc, e)
        self._lambdas = self.lambdas(nuc, e)
        self._omegas = self.omegas(nuc, e)
        self._Lambda = self.Lambdas(nuc, e)
        self._nuc = nuc
        self._e = e
        
    def beta(self):
        return sum(self._betas)

    def betas(self):
        return self._betas

    def lambdas(self):
        return self._lambdas

    def omegas(self):
        return self._omegas

    def Lambda(self):
        return self._Lambda

    def v_d(self, nuc, e):
        if nuc == "u235" and e == "thermal":
            return 0.01668

    def betas(self, nuc, e):
        # obtained from http://arxiv.org/pdf/1001.4100.pdf
        beta_dict = {}
        beta_dict["u235"] = {}
        beta_dict["pu239"] = {}
        beta_dict["u235"]["thermal"] = [0.00247, 0.0013845, 0.001222, 0.0026455, 0.000832, 0.000169]
        beta_dict["u235"]["fast"] = [0.000266, 0.001491, 0.001316, 0.002849, 0.000896, 0.000182] 
        beta_dict["pu239"]["thermal"] = [0.0,0.0,0.0,0.0,0.0,0.0] 
        beta_dict["pu239"]["fast"] = [0.0,0.0,0.0,0.0,0.0,0.0] 
        return beta_dict[nuc][e]

    def lambdas(self, nuc, e):
        # obtained from http://arxiv.org/pdf/1001.4100.pdf
        lambda_dict = {}
        lambda_dict["u235"] = {}
        lambda_dict["pu239"] = {}
        lambda_dict["u235"]["thermal"] = [math.log(2)/x for x in \
                [54.51, 21.84, 6.00, 2.23, 0.496, 0.179]]
        lambda_dict["u235"]["fast"] = [0.0127, 0.0317, 0.155, 0.311, 1.4, 3.87] 
        lambda_dict["pu239"]["thermal"] = [0.0,0.0,0.0,0.0,0.0,0.0] 
        lambda_dict["pu239"]["fast"] = [0.0,0.0,0.0,0.0,0.0,0.0]
        return lambda_dict[nuc][e]

    def omegas(self, nuc, e):
        # should obtain decay heat values
        omega_dict = {}
        omega_dict["u235"] = {}
        omega_dict["pu239"] = {}
        omega_dict["u235"]["thermal"] = [0.0, 0.0, 0.0]
        omega_dict["u235"]["fast"] = [0.0, 0.0, 0.0]
        omega_dict["pu239"]["thermal"] = [0.0,0.0,0.0] 
        omega_dict["pu239"]["fast"] = [0.0,0.0,0.0]
        return omega_dict[nuc][e]

    def Lambdas(self, nuc, e):
        Lambda_dict = {}
        Lambda_dict["u235"] = {}
        Lambda_dict["pu239"] = {}
        Lambda_dict["u235"]["thermal"] = 1.08e-5 
        Lambda_dict["u235"]["fast"] = 0
        Lambda_dict["pu239"]["thermal"] = 0 
        Lambda_dict["pu239"]["fast"] = 0
        return Lambda_dict[nuc][e]

