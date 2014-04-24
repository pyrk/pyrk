from pyne import material
from pyne import data

# load the data into a dictionary
def get_isodict(loc='bu8_tot.eq', valtype="mass"):
    isodict = {}
    for line in file(loc):
        zaid, atoms = line.split()
        if valtype == "mass":  
            isodict[int(zaid)] = data.atomic_mass(int(zaid))*float(atoms)
        elif valtype == "mol":
            isodict[int(zaid)] = float(atoms)
    return isodict


moldict=get_isodict(loc='bu8_tot.eq', valtype="mol")
massdict=get_isodict(loc='bu8_tot.eq', valtype="mass")

mat = material.Material(massdict)



# Now, activity 
import nucname
import operator

from scipy import constants
    
def get_activity_Ci(isodict=moldict, valtype="mol"):
    activity_Ci={}
    ci_dec_per_sec = 3.7E10 # conversion factor 1 curie = 3.7E10 decays/sec 
    if valtype=="mol":
        for iso, mols in isodict.iteritems():
            dec_per_sec = mols*constants.N_A*data.decay_const(nucname.id(iso))
            activity_Ci[nucname.name(iso)]= dec_per_sec/ci_dec_per_sec
    elif valtype=="mass":
        for iso, mass in isodict.iteritems():
            dec_per_sec = mass*data.atomic_mass(nucname.id(iso))*constants.N_A*data.decay_const(nucname.id(iso))
            activity_Ci[nucname.name(iso)]= dec_per_sec/ci_dec_per_sec
    sorted_a = sorted(activity_Ci.iteritems(), key=operator.itemgetter(0))
    print sorted_a
    return activity_Ci

activity_Ci=get_activity_Ci(moldict, valtype="mol")
print activity_Ci
#activity_Ci=get_activity_Ci(massdict, valtype="mass")
#print activity_Ci
