# Licensed under a 3-clause BSD style license - see LICENSE
import tables as tb


type_lookup = {bool: tb.BoolCol(),
               int: tb.Int32Col(),
               long: tb.Int64Col(),
               float: tb.Float64Col(),
               str: tb.StringCol(16)
               }

def pytables_type(prim_type):
    return type_lookup[prim_type]
