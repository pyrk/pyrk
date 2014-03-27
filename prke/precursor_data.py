class PrecursorData(object):
    def __init__(self, nuc, e):
        """initializes the precursor group data for the fissioning nuclide. e 
        should be 'thermal' or 'fast' to indicate the energy spectrum."""
        self._betas = self.betas(nuc, e)
        self._lambdas = self.lambdas(nuc, e)
        self._omegas = self.omegas(nuc, e)
        self._lifetime = self.mean_lifetimes(nuc, e)
        self._nuc = nuc
        self._e = e
        
    def betas(self):
        return self._betas

    def lambdas(self):
        return self._lambdas

    def omegas(self):
        return self._omegas

    def lifetime(self):
        return self._lifetime

    def betas(self, nuc, e):
        # obtained from http://arxiv.org/pdf/1001.4100.pdf
        beta_dict = {}
        beta_dict["u235"] = {}
        beta_dict["pu239"] = {}
        beta_dict["u235"]["thermal"] = []
        beta_dict["u235"]["fast"] = [0.000266, 0.001491, 0.001316, 0.002849, 0.000896, 0.000182] 
        beta_dict["pu239"]["thermal"] = [] 
        beta_dict["pu239"]["fast"] = [] 
        return beta_dict[nuc][e]

    def lambdas(self, nuc, e):
        # obtained from http://arxiv.org/pdf/1001.4100.pdf
        lambda_dict = {}
        lambda_dict["u235"] = {}
        lambda_dict["pu239"] = {}
        lambda_dict["u235"]["thermal"] = []
        lambda_dict["u235"]["fast"] = [0.0127, 0.0317, 0.155, 0.311, 1.4, 3.87] 
        lambda_dict["pu239"]["thermal"] = [] 
        lambda_dict["pu239"]["fast"] = []
        return lambda_dict[nuc][e]

    def omegas(self, nuc, e):
        # should obtain decay heat values
        omega_dict = {}
        omega_dict["u235"] = {}
        omega_dict["pu239"] = {}
        omega_dict["u235"]["thermal"] = [0, 0, 0, 0, 0, 0]
        omega_dict["u235"]["fast"] = [0, 0, 0, 0, 0, 0]
        omega_dict["pu239"]["thermal"] = [] 
        omega_dict["pu239"]["fast"] = []
        return omega_dict[nuc][e]

    def mean_lifetimes(self, nuc, e):
        lifetime_dict = {}
        lifetime_dict["u235"] = {}
        lifetime_dict["pu239"] = {}
        lifetime_dict["u235"]["thermal"] = 1.08e-5 
        lifetime_dict["u235"]["fast"] = 0
        lifetime_dict["pu239"]["thermal"] = 0 
        lifetime_dict["pu239"]["fast"] = 0
        return lifetime_dict[nuc][e]

