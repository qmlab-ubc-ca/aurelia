#%%
#Import libraries
import numpy as np

from aurelia.aurelia_arpes import Bands, Spec, ARPES
from aurelia.aurelia_static_vars import mod, domain, experiment
from aurelia.aurelia_plots import show_spectra as sh
from aurelia import aurelia_hdf5_saving as sv

#%% Define bands
Npts_in=[350, 300]
B=Bands(Npts = Npts_in, edges=1.5, symmetry = "hexagonal")
B.Make_kpath()
B.Make_bands()

#Initialize spec, self energy and matrix elements
spec=Spec(B, dimension='cube', Omega = np.linspace(-0.5, 0.15, 132))
SelfEnergy={"type": 'kink'}
spec.Make_self_energy(SE=SelfEnergy)
ME_in = {"type": ['poly','rot']}
spec.Make_matrix_elements(ME = ME_in)

#Define and add rotational domains
az={"Num": 2, "az": np.array([15, 10]),'amp': np.array([0.35, 0.15])}
d=domain(az = az)
d.Make_domain_rot(spec)

#Define modifier and calculate the spectral intensity
ER_max = 0.2
ER_min = 0.005
res = {"ER": np.random.uniform(ER_min, ER_max), "kR": np.random.rand()*0.05+0.01}
Temp = np.random.uniform(5, 500)
m=mod(resolution= res, temperature=Temp)
spec.Make_specfun(m)
spec.Make_specmod(m)
sh.Make_spec_plot(spec)

#%% Optionally, remove the rotational domains and check the original
#d.Rmv_domain_rot(spec)
#spec.Make_specfun(m)
#spec.Make_specmod(m)
#%% Prepare the experimental parameters object
# Offset angles
exp_offsets={"ph0":np.radians(np.random.uniform(-5,5)),\
                "th0":np.radians(np.random.uniform(-5,5)),\
                "az0":np.radians(np.random.uniform(-5,5)) }  
#Background parameters
bkgd_max = 0.15
bkgd_min = 0.01
bg={"type": ['flat','Shirley','poly'],\
     "polyA": np.random.uniform(bkgd_min, bkgd_max),\
      "flatA": np.random.uniform(bkgd_min, bkgd_max), \
      "ShirA": np.random.uniform(bkgd_min, bkgd_max)}
#Detector parameters
det={"response":'center', "sensitivity": np.random.uniform(0.8,1),\
      "type":'HA', "slit": "vertical", "counting mode":"ADC"}

Ne_max = 10**6
Ne_min = 10**5
exp=experiment(spec, detector=det, bkgd=bg, Ne = np.random.randint(Ne_min, Ne_max), angles = exp_offsets)

# Calculate the ARPES spectra
angle_lim={"th":np.deg2rad([-15,15]),\
      "ph":np.deg2rad([-15,15])}
arpes=ARPES(spec,exp, dimension = "slicekk", ang_lim = angle_lim)
arpes.Make_angle_conv()
sh.Make_arpes_plot(arpes, exp)
#%%
#Optionally, add flake domains (automatically initialized without user specification here)
#arpes=d.Make_domain_offset(arpes)

#Add background, response, and simulate the statistics.
arpes=exp.Make_bkgd(arpes)
arpes=exp.Make_detector_responsivity(arpes)
arpes.Make_statistics(exp)
sh.Make_stats_plot(arpes) #The edges are cropped here

# %%
#Optionally save
#path = os.path.join(".", "data_QS")
#filename='arpes_domains.h5'
#sv.save_class_to_hdf5(arpes,path,filename)
# %%
