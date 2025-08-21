#%%
import os
import sys
import numpy as np
sys.path.insert(0, os.path.abspath("..") + "\\aurelia")
from aurelia_arpes import Bands, Spec, ARPES
from aurelia_static_vars import mod, domain, experiment
#from init_static import save_h5 as save
from aurelia_plots import show_spectra as sh
import aurelia_hdf5_saving as sv
#%% Exposed Parameters
#Number of electrons
Ne_max = 10**5
Ne_min = 10**4

#Background parameters
bkgd_max = 0.15
bkgd_min = 0.01

#Sharpness parameters
ER_max = 0.2
ER_min = 0.005
#%%
Npts_in=[550, 200]
ME_in = {"type": ['poly','symm','rot']}
#ang_in={"th":np.deg2rad([-15,15]),"ph":np.deg2rad([-30,20])}
exp_offsets={"ph0":np.radians(np.random.uniform(-5,5)),\
                "th0":np.radians(np.random.uniform(-5,5)),\
                "az0":np.radians(np.random.uniform(-5,5)) }  

bg={"type": ['flat','Shirley','poly'],\
     "polyA": np.random.uniform(bkgd_min, bkgd_max),\
      "flatA": np.random.uniform(bkgd_min, bkgd_max), \
      "ShirA": np.random.uniform(bkgd_min, bkgd_max)}
det={"response":'center', "sensitivity": np.random.uniform(0.8,1),\
      "type":'HA', "slit": "vertical", "counting mode":"ADC"}

flake={"Num": 2}
flake["th"] = np.random.choice([-1,1], size=flake["Num"])*np.deg2rad(np.random.uniform(2,8, flake["Num"]))

d=domain(flake=flake)

SE={"type": 'FL'}
B=Bands(Npts = Npts_in, edges=1.5)
B.Make_kpath()
B.Make_bands()
spec=Spec(B, ME=ME_in, dimension='sliceEk', Omega = np.linspace(-0.55, 0.15, 532))
spec.Make_matrix_elements()
spec.Make_self_energy(SE)
res = {"ER": np.random.uniform(ER_min, ER_max), "kR": np.random.rand()*0.05+0.01}
Temp = np.random.uniform(5, 50)
m=mod(resolution= res, temperature=Temp)
B, spec = d.Make_domain_rot(spec)
spec.Make_specfun(m)
spec.Make_specmod(m)
sh.Make_spec_plot(spec)

#%%
exp=experiment(spec, detector=det, bkgd=bg, Ne = int(np.random.uniform(Ne_min, Ne_max)))
arpes=ARPES(spec,exp, dimension = "sliceEk")
arpes.Make_angle_conv(const=0)
arpes=d.Make_domain_offset(arpes)
arpes=exp.Make_bkgd(arpes)
arpes=exp.Make_detector_responsivity(arpes)
arpes.Make_statistics(exp)
sh.Make_stats_plot(arpes)
# %%
