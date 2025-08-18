import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

class mod:
    def __init__(self, temperature=None, resolution=None):
        if temperature == None:
            self.Temp=np.random.uniform(10,350)
        else:
            self.Temp=temperature
        if resolution == None:
            self.ER=np.random.rand()*0.25+0.001
            self.kR=np.random.rand()*0.02+0.005
        else:
            self.ER=resolution["ER"]
            self.kR=resolution["kR"]

class domain:
    def __init__(self, az=None, flake=None):
        # Make it really static when exposing inputs
        #Rotational domain parameters
        self.type=[]
        if az is None:
            az = {"Num": np.random.randint(1,3)}
            az["az"] = np.random.uniform(-30,30,az["Num"])
            az["amp"] = np.random.rand(az["Num"])
        else:
            if "Num" not in az:
                az["Num"] = np.random.randint(1,len(az["az"]))
            if "az" not in az:
                az["az"] = np.random.uniform(-30,30,az["Num"])
        self.az=az
        #Flake offset domain parameters
        if flake is None:
            flake = {"Num": np.random.randint(0,5)}
            flake["th"] = np.deg2rad(np.random.uniform(-5,5, flake["Num"]))
            flake["ph"] = np.deg2rad(np.random.uniform(-5,5, flake["Num"]))
            flake["amp"] = np.random.rand(flake["Num"])
        else:
            if "Num" not in flake:
                flake["Num"] = len(flake["th"])
            if "th" not in flake:
                flake["th"] = np.deg2rad(np.random.uniform(-5,5, flake["Num"]))
            if "ph" not in flake:
                flake["ph"] = np.deg2rad(np.random.uniform(-5,5, flake["Num"]))
            if "amp" not in flake:
                flake["amp"] = np.random.rand(flake["Num"])
        self.flake=flake
    def Make_domain_rot(self, spec):
        bands=spec.bands
        kx = bands.kpath[:, 0]
        ky = bands.kpath[:, 1]
        for i in range(self.az["Num"]):
            krot = np.zeros((len(kx), 2))
            krot[:, 0] = np.cos(np.deg2rad(self.az["az"][i])) * kx - np.sin(np.deg2rad(self.az["az"][i])) * ky
            krot[:, 1] = np.sin(np.deg2rad(self.az["az"][i])) * kx + np.cos(np.deg2rad(self.az["az"][i])) * ky
            Bands_r = griddata(krot, bands.bands[:,0:bands.Nbands], (kx, ky), method='nearest')
            M_r = griddata(krot, spec.matrix_elements, (kx, ky), method='nearest')
            ReS_r = spec.ReS
            ImS_r = spec.ImS
            bands.bands = np.concatenate((bands.bands, Bands_r), axis=1)
            spec.matrix_elements = np.concatenate((spec.matrix_elements, M_r), axis=1)
            spec.ReS = np.concatenate((spec.ReS, ReS_r), axis=1)
            spec.ImS = np.concatenate((spec.ImS, ImS_r), axis=1)
            spec.domain = np.hstack((spec.domain, self.az["amp"][i]* np.ones((1,bands.Nbands))))
            self.type=self.type+['rot']
            spec.domain_info=self
        return(bands, spec)
    
    def Rmv_domain_rot(self, spec):
        bands=spec.bands
        bands.bands=bands.bands[:,0:bands.Nbands]
        spec.bands=bands
        spec.matrix_elements=spec.matrix_elements[:,0:bands.Nbands]
        spec.domain=spec.domain[0,0:bands.Nbands]
        spec.ReS=spec.ReS[0,0:bands.Nbands]
        spec.ImS=spec.ImS[0,0:bands.Nbands]

        del spec.domain_info
        self.type.remove('rot')
        return(bands, spec)
    
    def Make_domain_offset(self, arpes, speed='fast'):
        if speed == 'fast':
            if arpes.dimension != 'sliceEk':
                th = arpes.th
                ph = arpes.ph
                A_offset = np.zeros((arpes.intensity.shape))
                for i in range (self.flake["Num"]):
                    indth = np.where(th >= min(th) + abs(self.flake["th"][i]))[0][0] - 1
                    indph = np.where(ph >= min(ph) + abs(self.flake["ph"][i]))[0][0] - 1
                    A_offset += self.flake["amp"][i]*(np.roll(np.roll(arpes.intensity,\
                            -1*np.sign(self.flake["th"][i]).astype(int)*indth, axis=1), \
                            -1*np.sign(self.flake["ph"][i]).astype(int)*indph, axis=2))
            elif arpes.dimension == 'sliceEk':
                th = arpes.th
                A_offset = np.zeros((arpes.intensity.shape))
                for i in range (self.flake["Num"]):
                    indth = np.where(th >= min(th) + abs(self.flake["th"][i]))[0][0] - 1
                    A_offset += self.flake["amp"][i]*np.roll(arpes.intensity, \
                        -1*np.sign(self.flake["th"][i]).astype(int)*indth, axis=1)
        elif speed == 'slow':       
            if arpes.dimension != 'cube':
                A_offset = np.zeros((arpes.intensity.shape))
                for i in range(self.flake["Num"]):
                    dom={"th0":self.flake["th"][i], "ph0":self.flake["ph"][i]}
                    A_out=arpes.Make_angle_conv(const=arpes.slice_const, domain=dom)
                    A_offset += self.flake["amp"][i]*A_out
            elif arpes.dimension == 'cube':
                A_offset = np.zeros((arpes.intensity.shape))
                for i in range(self.flake["Num"]):
                    dom={"th0":self.flake["th"][i], "ph0":self.flake["ph"][i]}
                    A_out=arpes.Make_angle_conv(domain=dom)
                    A_offset += self.flake["amp"][i]*A_out         
        self.type=self.type+['offset']
        arpes.domain=arpes.intensity +A_offset          
        arpes.domain_info=self  
        print('Domains included:', self.type)
        if 'offset' in self.type:
            print('Number of flakes:', self.flake["Num"])
            print('flake th0:' , np.round(np.degrees(self.flake["th"]),2))
            print('flake ph0:' , np.round(np.degrees(self.flake["ph"]),2))
            print('flake amp:' , np.round(self.flake["amp"],2))
        if 'rot' in self.type:
            print('Number of rotational domains:', self.az["Num"])
            print('rotational angle:' , self.az["az"])     
        return(arpes)
    
    def Rmv_domain_offset(self, arpes):
        if hasattr(arpes, 'domain')==True:
            del arpes.domain
            del arpes.domain_info
            self.type.remove('offset')
        elif hasattr(arpes, 'domain')==False:
            print('Flake domains do not exist')
        return(arpes)

class experiment:      
    def __init__(self, spec, angles=None, hv=None, bkgd=None, Ne=None, detector=None):       
        ## parameters for k to angle conversion
        self.workfun=4+np.random.rand()
        if angles==None:
            if spec.dimension == 'sliceEk':
                self.az0=0
                self.ph0=0
                self.th0=np.radians(np.random.uniform(-10,10))
            elif spec.dimension != 'sliceEk':
                self.az0=np.radians(np.random.uniform(0,360))
                self.th0=np.radians(np.random.uniform(-10,10))
                self.ph0=np.radians(np.random.uniform(-10,10))
        elif angles=='zero':
            self.az0=0
            self.th0=0
            self.ph0=0
        else:
            if "az0" in angles:
                self.az0=angles["az0"]
            else:
                self.az0=0
            if "th0" in angles:
                self.th0=angles["th0"]
            else:
                self.th0=0
            if "ph0" in angles:
                self.ph0=angles["ph0"]
            else:
                self.ph0=0
        if hv == None:
            self.hv=7.634*spec.bands.klim.max()**2-min(spec.Omega)+self.workfun\
            +5*np.random.rand()+5
        else: 
            self.hv=hv
        if bkgd == None:
            bkgd={"type": ['flat','Shirley']}
            if spec.dimension == 'slicekk':      
                bkgd["flatA"]=np.random.rand()*0.2+0.01
                bkgd["shirA"]=0      
            elif spec.dimension == 'sliceEk':
                bkgd["flatA"]=np.random.rand()*0.2+0.01
                bkgd["shirA"]=np.random.rand()*0.1+0.01
            elif spec.dimension == 'cube':
                bkgd["flatA"]=np.random.rand()*0.1+0.01
                bkgd["shirA"]=np.random.rand()*0.05+0.01
        elif bkgd == 'zero':
            bkgd["type"]='zero'
            bkgd["flatA"]=0
            bkgd["shirA"]=0
        else:
            if "flat" in bkgd["type"]:
                if "flatA" not in bkgd: 
                    bkgd["flatA"]=np.random.rand()*0.2+0.01
            if "Shirley" in bkgd["type"]:
                if "shirA" not in bkgd:
                    bkgd["shirA"]=np.random.rand()*0.1+0.01
            if "poly" in bkgd["type"]:
                if "polyOrder" not in bkgd:
                    bkgd["polyOrder"]=np.random.randint(5)
                if "polyA" not in bkgd:
                    bkgd["polyA"]=np.random.rand()*0.1+0.01
        self.bkgd=bkgd
        self.bkgd["type"]=bkgd["type"]

        if detector is None:
            detector={"response": 'flat', "slit": 'horizontal', "counting mode": "PC"}
        self.detector=detector

        if Ne is None:
            if spec.dimension == 'slicekk':      
                self.Ne=round(10**(4+np.random.rand()*2))            
            elif spec.dimension == 'sliceEk':
                self.Ne=round(10**(4+np.random.rand()*3))
            elif spec.dimension == 'cube':
                self.Ne=round(10**(5+np.random.rand()*3))
        else:
            self.Ne=Ne

    def Make_bkgd(self, arpes):
        Amp = np.max(arpes.intensity)
        bkgd=np.zeros(arpes.intensity.shape)
        if 'flat' in self.bkgd["type"]:
            bkgd = bkgd + self.bkgd["flatA"] * Amp * np.ones(arpes.intensity.shape) 
        if 'Shirley' in self.bkgd["type"]:
            if arpes.dimension == 'slicekk':
                print('Shirley background requires energy axis, does not work for slicekk, setting to zero')
                Shir = np.zeros(arpes.intensity.shape)
            else:
                A=arpes.intensity          
                A=np.reshape(A, (A.shape[0], int(np.prod(A.shape)/A.shape[0])))
                Shir = np.zeros(A.shape)
                for i in range(len(arpes.Ek)-1):
                    Shir[i, :] = np.sum(A[i:-1,:], axis=0)
                Shir = self.bkgd["shirA"] * Amp * Shir /np.max(Shir)
                Shir = np.reshape(Shir, arpes.intensity.shape)                                
            bkgd = bkgd + Shir
        if 'poly' in self.bkgd["type"]:
            coeffs = np.random.randn(self.bkgd["polyOrder"]+1,self.bkgd["polyOrder"]+1) # generate random coefficients
            if arpes.dimension == 'slicekk':
                x, y = np.meshgrid(arpes.ph, arpes.th)
            elif arpes.dimension == 'sliceEk':
                x, y = np.meshgrid(arpes.th, arpes.Ek)
            elif arpes.dimension == 'cube':
                x, y = np.meshgrid(arpes.ph, arpes.th)
            Poly =  np.polynomial.polynomial.polyval2d(x, y, coeffs)
            Poly = self.bkgd["polyA"] * Amp * (Poly-np.min(Poly))/np.abs(np.max(Poly))
            if arpes.dimension =='cube':
                Poly=np.stack([Poly]*arpes.Ek.shape[0], axis=1)
            bkgd = bkgd + Poly
        arpes.bkgd=bkgd
        return(arpes)
    
    def Make_detector_responsivity(self, arpes):
        if self.detector["response"] == 'flat':
            response= np.ones(arpes.intensity.shape)
        elif self.detector["response"] == 'center':
            r_diff = self.detector["sensitivity"]
            y = -(arpes.th-np.mean(arpes.th))**2
            y = (y-np.min(y))/max(abs(y))*r_diff+(1-r_diff)
            y = np.reshape(y,(-1,1)).T
            if self.detector["type"] =='HA':
                if arpes.dimension == 'slicekk':
                    y2=np.reshape(np.ones(arpes.ph.shape),(-1,1))
                    response= np.stack([np.matmul(y2, y).T]*1, axis=0)                    
                elif arpes.dimension != 'slicekk':
                    y2=-(arpes.Ek-np.mean(arpes.Ek))**2
                    y2=(y2-np.min(y2))/max(abs(y2))*r_diff+(1-r_diff)
                    y2=np.reshape(y2,(-1,1))
                    if arpes.dimension == 'sliceEk':
                        response= np.matmul(y2, y)
                    if arpes.dimension == 'cube':
                        dummy=np.matmul(y2,y)
                        response=np.stack([dummy]*arpes.ph.shape[0], axis=2)
            if self.detector["type"]=='TOF':
                if arpes.dimension == 'sliceEk':
                    y2=np.reshape(np.ones(arpes.Ek.shape),(-1,1))
                    response= np.matmul(y2, y)
                elif arpes.dimension != 'sliceEk':
                    y2=-(arpes.ph-np.mean(arpes.ph))**2
                    y2=(y2-np.min(y))/max(abs(y))*r_diff+(1-r_diff)
                    y2=np.reshape(y2,(-1,1))
                    if arpes.dimension == 'slicekk':
                        response = np.stack([np.matmul(y2, y).T]*1, axis=0)
                    if arpes.dimension == 'cube':
                        response = np.stack([np.matmul(y2, y).T]*arpes.Ek.shape[0], axis=0)           
        arpes.response=response
        return(arpes)
    
        
        


