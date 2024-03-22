#import spiceypy to astronomy calculations
import spiceypy
from kernel_manager import kernels_load

#import datetime to work with date data
import datetime

#import math to use math functions
import math

class Earth:
    def __init__(self):
        AU_TO_KM = 149_597_871
        self.kernels_path = ['./kernels/lsk/naif0012.tls.txt',
                './kernels/pck/gm_de431.tpc.txt',
                './kernels/spk/de440s.bsp']
        kernels_load(self.kernels_path)
        #get a today date
        today = datetime.datetime.today()

        #convert today to string and set midnight
        self.today = today.strftime('%Y-%m-%dT00:00:00')

        #convert UTC to ET
        self.et_today = spiceypy.utc2et(self.today)

        #Calculating an earth state vector and time of light's travel between
        #the earth and the sun
        #Using spkgeo function with parametres:
        #targ = 399 - NAIF ID of the planet (The Earth in this case) that state vector is pointing
        #et = et_todat - Reference time of calculations
        #ref = 'ECLIPJ2000' - An Ecliptic Plane used in calculations
        #obs = 10 - NAIF ID of the object (The Sun in this case) which is the beggining of state vector
        self.earth_state_vector, self.earth_sun_light_time = spiceypy.spkgeo(targ=399,
            et = self.et_today, ref='ECLIPJ2000', obs = 10)

        #Calculate earth - sun distance (km)
        self.earth_sun_distace = math.sqrt(self.earth_state_vector[0]**2 + 
                                      self.earth_state_vector[1]**2 +
                                      self.earth_state_vector[2]**2)
        #Convert a distance to AU
        self.au_earth_sun_distance = self.earth_sun_distace/AU_TO_KM

        #Calculate the orbital speed of the Earth around the Sun (km/s)
        self.earth_sun_speed = math.sqrt(self.earth_state_vector[3]**2 + 
                                         self.earth_state_vector[4]**2 +
                                         self.earth_state_vector[5]**2)

        #Calculate theorical orbital speed of the Earth around the Sun (km/s)
        _, self.gm_sun = spiceypy.bodvcd(bodyid=10, item='GM', maxn=1) #GM parameter
        self.earth_sun_speed_theory = math.sqrt(self.gm_sun[0]/self.earth_sun_distace)

    #Print an information about the Earth
    def __str__(self):
        info = f"""\n\tEarth location in relation to Sun for {self.today}: {self.earth_state_vector} km\n
        Earth distace from Sum equals for {self.today}: {self.au_earth_sun_distance} AU\n
        The Earth orbital speed around the Sun equals for: {self.earth_sun_speed}" km/s\n
        The theoretical Earth orbital speed around the Sun equals for: {self.earth_sun_speed_theory} km/s)\n"""
        return info

if __name__ == '__main__':
    earth = Earth()
    print(earth)
                
        