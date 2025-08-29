#This function was used to generate the quality score images used to train the ML model in the manuscript
#%%
#Import libraries
import numpy as np
from aurelia.aurelia_arpes import Bands, Spec, ARPES
from aurelia.aurelia_static_vars import mod, domain, experiment
from aurelia.aurelia_plots import show_spectra as sh
from aurelia import aurelia_hdf5_saving as sv
#%% Exposed Parameters for training
#Number of electrons
Ne_max = 10**5
Ne_min = 10**4

#Background parameters
bkgd_max = 0.2
bkgd_min = 0.01

#Sharpness parameters
ER_max = 0.2
ER_min = 0.005

#%%
path = os.path.join(".", "data_QS")
os.makedirs("data_QS", exist_ok=True)
#Define kapath. Here we are calculating dispersion cut, so we want more points in kx, and less in ky.
Npts_in=[500, 220]
#Define matrix elements
ME_in = {"type": ['poly','symm','rot']}
#Define offset angles (primary flake)
exp_offsets={"ph0":np.radians(np.random.uniform(-5,5)),\
                "th0":np.radians(np.random.uniform(-5,5)),\
                "az0":np.radians(np.random.uniform(-5,5)) }  
#Define background
bg={"type": ['flat','Shirley','poly'],\
     "polyA": np.random.uniform(bkgd_min, bkgd_max),\
      "flatA": np.random.uniform(bkgd_min, bkgd_max), \
      "ShirA": np.random.uniform(bkgd_min, bkgd_max)}
#Define detector settings
det={"response":'center', "sensitivity": np.random.uniform(0.8,1),\
      "type":'HA', "slit": "vertical", "counting mode":"ADC"}
#Define score parameters
score_param={"threshold": [0.9, 0.7, 0.5, 0.3, 0.1, 0], \
       "penalty": [1, 2, 3, 5, 8], \
        "weight": [0.6, 1, 0.8]}
#%% Run the simulation
for i in range(5):
      B=Bands(Npts = Npts_in, edges=1.1)
      B.Make_kpath()
      B.Make_bands()
      spec=Spec(B, dimension='sliceEk', Omega = np.linspace(-0.55, 0.15, 532))
      spec.Make_matrix_elements(ME=ME_in, )
      spec.Make_self_energy(SE={"type": 'FL'})
      res = {"ER": np.random.uniform(ER_min, ER_max), "kR": np.random.rand()*0.05+0.01}
      Temp = np.random.uniform(5, 50)
      m=mod(resolution= res, temperature=Temp)
      spec.Make_specfun(m)
      spec.Make_specmod(m)

      exp=experiment(spec, detector=det, bkgd=bg, Ne = int(np.random.uniform(Ne_min, Ne_max)))
      arpes=ARPES(spec, exp, dimension = "sliceEk")
      arpes.Make_angle_conv()
      #sh.Make_arpes_plot(arpes, exp)
      arpes=exp.Make_bkgd(arpes)
      arpes=exp.Make_detector_responsivity(arpes)
      arpes.Make_statistics(exp)
      sh.Make_stats_plot(arpes)

      arpes.Make_quality_score(param = score_param)
      #filename='arpesQS_'+str(i)+'.h5'
      #sv.save_class_to_hdf5(arpes,path,filename)

# %%
