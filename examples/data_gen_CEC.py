
#This function generates constant-energy cut ARPES spectra from random bandstructures and epxerimental parameters.
#The number of spectra generated is given by N_runs.
#%%
import numpy as np
from aurelia_arpes import Bands, Spec, ARPES
from aurelia_static_vars import mod, domain, experiment
import matplotlib.pyplot as plt
import aurelia_hdf5_saving as sv
from aurelia_plots import show_spectra as sh
import os
# %%
path = os.path.join(".", "data_QS")
os.makedirs("data_QS", exist_ok=True)
N_runs=1
#Detector settings
det={"response":'center', "sensitivity": np.random.uniform(0.5,1),\
      "type":'HA', "slit": "horizontal", "counting mode":"ADC"}
#Number of points in for theta, phi
Npts_in=[500, 150]
#Input matrix elements
ME_in = {"type": ['poly','symm','rot']}
#Experimental offset angles
exp_offsets={"ph0":np.radians(np.random.uniform(-10,10)),\
                "th0":np.radians(np.random.uniform(-10,10)),\
                "az0":np.radians(np.random.uniform(-5,5)) } 
#Self energy 
SE={"type": 'FL'}
#Background
bg={"type": ('flat','poly')}
for i in range(N_runs):
    #Define bands
    B=Bands(Npts = Npts_in, edges=1.25)
    B.Make_kpath()
    B.Make_bands()
    B.print_variables()
    #Calculate spectra (in Eb and k)
    spec=Spec(B, ME=ME_in, dimension='slicekk')
    spec.Make_matrix_elements()
    spec.Make_self_energy(SE)
    m=mod()
    spec.Make_specfun(m)
    spec.Make_specmod(m)
    spec.print_variables()
    #sh.Make_spec_plot(spec)

    #Calculate experimental arpes spectra
    ang_in={"th":np.deg2rad([-15,15]),\
            "ph":np.deg2rad([-10-np.random.randint(10),10+np.random.randint(10)])}
    exp=experiment(spec, detector=det, bkgd=bg, Ne=10**6)
    arpes=ARPES(spec, exp, ang_lim=ang_in)
    arpes.Make_angle_conv()
    #sh.Make_arpes_plot(arpes,exp)

    #Add experimental artifacts
    arpes=exp.Make_bkgd(arpes)
    arpes=exp.Make_detector_responsivity(arpes)
    arpes.Make_statistics(exp)
    sh.Make_stats_plot(arpes)
   # arpes.print_variables()
    
    #Optional saving
    #print(i)
    #filename='arpesFS_'+str(i)+'.h5'
    #sv.save_class_to_hdf5(arpes,path,filename)
