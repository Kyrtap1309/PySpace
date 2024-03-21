#import spiceypy to astronomy calculations
import spiceypy

#import datetime to work with date data
import datetime 

#spicepy needs a kernels loaded to work properly
spiceypy.furnsh('./kernels/lsk/naif0012.tls.txt')
spiceypy.furnsh('./kernels/spk/de440s.bsp')

#get a today date
today = datetime.datetime.today()

#convert today to string and set midnight
today = today.strftime('%Y-%M-%dT00:00:00')

#convert UTC to ET
et_today = spiceypy.utc2et(today)


#Calculating an earth state vector and time of light's travel between
#the earth and the sun
#Using spkgeo function with parametres:
#targ = 399 - NAIF ID of the planet (The Earth in this case) that state vector is pointing
#et = et_todat - Reference time of calculations
#ref = 'ECLIPJ2000' - An Ecliptic Plane used in calculations
#obs = 10 - NAIF ID of the object (The Sun in this case) which is the beggining of state vector
earth_state_vector, earth_sun_light_time = spiceypy.spkgeo(targ=399,
    et = et_today, ref='ECLIPJ2000', obs = 10)

#print(earth_state_vector)
print(earth_sun_light_time)