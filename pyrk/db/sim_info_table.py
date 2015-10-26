"""
This module creates a table to store information about simulation itself.
"""

from __future__ import print_function

import tables as tb


def add_entry_from_sim_info(table, si):
    add_entry(table, si.record())

def add_entry(table, rec):
    for k, v in rec.iteritems():
        table.row[k] = v
    table.row.append()
    table.flush()

def add_simulation_from_sim_info(table, si):
    add_entry(table, si.metadata())
