# Licensed under a 3-clause BSD style license - see LICENSE
"""
This subpackage contains ANS standard data for decay heat from fission product
groups.
"""


class DecayData(object):

    """
    The DecayData class contains fission decay heat data.

        It is used to contain decay heat data retrieved from ANS/ANSI standards
        for decay heat from fission products.

        The traits are documented close to their definition by using a special
        comment ``#:`` prefix.

    .. note::

       The ANS/ANSI standards can be found at the ans store:
           http://www.ans.org/store/i_240256
    """

    def __init__(self, nuc, e, n):
        """Initializes the decay group data for the fissioning nuclide (u235,
        pu238, etc.... currently only u235 and sfr are supported).


        :param e: The energy spectrum type. This should be 'thermal' or 'fast'
            to indicate the energy spectrum.
        :type e: str.
        :param n: The number of decay heat groups. Currently, only 11 is
            supported.
        :type n: int.
        :returns: A DecayData object.
        """
        self._lambdas = self._get_lambdas(nuc, e)
        self._kappas = self._get_kappas(nuc, e)
        self._nuc = nuc
        self._e = e
        self._n = n

    def lambdas(self):
        """
        :returns: a list of floats
            the lambdas (decay constants) for each decay heat group
        """
        return self._lambdas

    def kappas(self):
        """
        :returns: a list of floats
            the kappas (decay heat values) for each decay heat group
        """
        return self._kappas

    def _get_lambdas(self, nuc, e):
        """
        :param e: The energy spectrum type. This should be 'thermal' or 'fast'
            to indicate the energy spectrum.
        :type e: str.
        :param nuc: The fissioning nuclide or custom reactor type. Currently
        only u235, sfr, or pu239 are supported
        :type nuc: str.
        :returns: a list of floats
            the lambdas (decay constants) for each decay heat group
        """
        lambda_dict = {}
        lambda_dict["u235"] = {}
        lambda_dict["sfr"] = {}
        lambda_dict["pu239"] = {}

        # ANS/ANSI 5.1-1971 for 235U thermal fission standard, 11 groups
        lambda_dict["u235"]["thermal"] = [2.658*10**0, 4.619*10**(-1),
                                          6.069*10**(-2), 5.593*10**(-3),
                                          6.872*10**(-4), 6.734*10**(-5),
                                          6.413*10**(-6), 6.155*10**(-7),
                                          8.288*10**(-8), 1.923*10**(-8),
                                          1.214*10**(-9)]

        lambda_dict["u235"]["fast"] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        lambda_dict["sfr"]["fast"] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        lambda_dict["pu239"]["thermal"] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        lambda_dict["pu239"]["fast"] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        return lambda_dict[nuc][e]

    def _get_kappas(self, nuc, e):
        """
        :param e: The energy spectrum type. This should be 'thermal' or 'fast'
            to indicate the energy spectrum.
        :type e: str.
        :param nuc: The fissioning nuclide or custom reactor type. Currently
        only u235, sfr, or pu239 are supported
        :type nuc: str.
        :returns: a list of floats
        :returns: a list of floats
            the kappas (decay heat values) for each decay heat group
        """
        kappa_dict = {}
        kappa_dict["sfr"] = {}
        kappa_dict["u235"] = {}
        kappa_dict["pu239"] = {}

        # Decay heat data, ANS/ANSI 5.1-1971 for 235U thermal fission, 11grps
        kappa_dict["u235"]["thermal"] = [6.587*10**0,
                                         1.490*10**(-1),
                                         2.730*10**(-1),
                                         2.173*10**(-2),
                                         1.961*10**(-3),
                                         1.025*10**(-4),
                                         4.923*10**(-6),
                                         2.679*10**(-7),
                                         1.452*10**(-8),
                                         1.893*10**(-9),
                                         1.633*10**(-10)]
        kappa_dict["u235"]["fast"] = [0.0, 0.0, 0.0]
        kappa_dict["sfr"]["fast"] = [0.0, 0.0, 0.0]
        kappa_dict["pu239"]["thermal"] = [0.0, 0.0, 0.0]
        kappa_dict["pu239"]["fast"] = [0.0, 0.0, 0.0]
        return kappa_dict[nuc][e]
