# Licensed under a 3-clause BSD style license - see LICENSE
import tables as tb


class DBTypes(object):
    """The DBTypes class, which should be treated as pure virtual,
    interrogates a class and generates an appropriate isDescription class from
    it.
    """

    def __init__(self):
        """"""

    def convert_to_pytables_type(self, var):
        """Uses the function dictionary to convert var to a pytables type
        function

        :param var: the variable to convert
        :type var: any
        """
