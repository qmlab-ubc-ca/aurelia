
#This is a quick start example to the uses of aurelia!
#%% 
import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath("..") + "\\aurelia")
from aurelia_arpes import Bands, Spec, ARPES
from aurelia_static_vars import mod, experiment
from aurelia_plots import show_spectra as sh
#%%
#Define bands
B=Bands(Npts = [200, 250]) #Number of points in for theta, phi
B.Make_kpath()
B.Make_bands()
B.print_variables()
#Calculate spectra (in Eb and k)
spec=Spec(B, dimension='sliceEk')
spec.Make_matrix_elements()
spec.Make_self_energy(SE = {"type": 'FL'})
m=mod()
spec.Make_specfun(m)
spec.Make_specmod(m)
spec.print_variables()
sh.Make_spec_plot(spec)

#Calculate experimental arpes spectra
ang_in={"th":np.deg2rad([-15,15]),\
        "ph":np.deg2rad([-10,10])}

det={"response":'center', "sensitivity": np.random.uniform(0.5,1),\
      "type":'HA', "slit": "horizontal", "counting mode":"ADC"}

bg={"type": ('flat','poly')}
exp=experiment(spec, detector=det, bkgd=bg, Ne=10**6)
arpes=ARPES(spec, exp, ang_lim=ang_in)
arpes.Make_angle_conv()
sh.Make_arpes_plot(arpes,exp)

#Add experimental artifacts
arpes=exp.Make_bkgd(arpes)
arpes=exp.Make_detector_responsivity(arpes)
arpes.Make_statistics(exp)
sh.Make_stats_plot(arpes)
arpes.print_variables()

# %%
