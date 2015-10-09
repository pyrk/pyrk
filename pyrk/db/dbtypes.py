# Licensed under a 3-clause BSD style license - see LICENSE
import tables as tb


type_lookup = {bool: tb.BoolCol(),
               int: tb.Int32Col(),
               long: tb.Int64Col(),
               float: tb.Float64Col(),
               str: tb.StringCol(16)
               }


def pytables_type(prim_type):
    if prim_type in type_lookup:
        return type_lookup[prim_type]
    else:
        msg = "The type "
        msg += str(prim_type)
        msg += " is not yet supported in the dbtypes class."
        raise TypeError(msg)
