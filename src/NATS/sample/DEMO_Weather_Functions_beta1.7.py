# NATS sample
#
# Optimal Synthesis Inc.
#
# Oliver Chen
# 09.10.2019
#
# Demo of weather-related functions
#

from NATS_Python_Header import *

clsNATSStandalone = JClass('NATSStandalone')
# Start NATS Standalone environment
natsStandalone = clsNATSStandalone.start()

if (natsStandalone is None) :
    print "Can't start NATS Standalone"
    quit()

simulationInterface = natsStandalone.getSimulationInterface()

entityInterface = natsStandalone.getEntityInterface()
controllerInterface = entityInterface.getControllerInterface()
pilotInterface = entityInterface.getPilotInterface()

environmentInterface = natsStandalone.getEnvironmentInterface()
weatherInterface = environmentInterface.getWeatherInterface()

equipmentInterface = natsStandalone.getEquipmentInterface()
aircraftInterface = equipmentInterface.getAircraftInterface()

safetyMetricsInterface = natsStandalone.getSafetyMetricsInterface()

environmentInterface.load_rap("share/tg/rap")

print ""
print "************************************************"
print "Get wind data"
print "************************************************"
print ""

# Demo of getting wind data -------------------------------
t = 6600
lat_deg = 40.0
lon_deg = -73.0
alt_ft = 20000.0

windResultArray = weatherInterface.getWind(t, lat_deg, lon_deg, alt_ft)
if not(windResultArray is None) :
    print "Wind result(t=", t, ", lat=", lat_deg, ", lon=", lon_deg, ", altitude=", alt_ft, ") = [", windResultArray[0], ", ", windResultArray[1], "]"
# end - Demo of getting wind data -------------------------


print ""
print "********************************************************"
print "Simulate trajectory and get weather polygons when paused"
print "********************************************************"
print ""

# Demo of getting conflicting weather polygon data ----------------------------

# Download weather data files(not the severe traffic-blocking weather definition)
# This function is only needed to be called when new weather files are required
#weatherInterface.downloadWeatherFiles();

aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_KLAX_KSFO.trx", "share/tg/trx/TRX_DEMO_KLAX_KSFO_mfl.trx")

simulationInterface.setupSimulation(11000, 30)

simulationInterface.start(3210)
             
# Use a while loop to constantly check simulation status.  When the simulation finishes, continue to output the trajectory data
while True:
    runtime_sim_status = simulationInterface.get_runtime_sim_status()
    if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
        break
    else:
        time.sleep(1)

# Till here, the simulation paused
# We can work on getting the weather polygon info as follows

ac_id = "ULI-3533A88AE5"

curAircraft = aircraftInterface.select_aircraft(ac_id)
if not(curAircraft is None):
    lat_deg = curAircraft.getLatitude_deg() # Set latitude
        
    lon_deg = curAircraft.getLongitude_deg() # Set longitude
        
    alt_ft = 33000.0 # Set altitude
    nauticalMile_radius = 100.0 # Set nautical mile radius
        
    #controllerInterface.setWeather_pirepFile("") # NATS automatically pick latest file

    #controllerInterface.setWeather_polygonFile("share/rg/polygons/MACS_scenario.dat")
    #controllerInterface.setWeather_polygonFile("") # NATS automatically pick latest file

    controllerInterface.setWeather_sigmetFile("share/tg/weather/demo_20190906_182626.sigmet")
    #controllerInterface.setWeather_sigmetFile("") # NATS automatically pick latest file

    # Get weather polygons
    weatherPolygonArray = weatherInterface.getWeatherPolygons(ac_id, lat_deg, lon_deg, alt_ft, nauticalMile_radius)
    if not(weatherPolygonArray is None) :
        for i in range(0, len(weatherPolygonArray)) :
            curWeatherPolygon = weatherPolygonArray[i]
            if not(curWeatherPolygon is None) and (0 < len(curWeatherPolygon.getX_data())):
                x_data_array = curWeatherPolygon.getX_data()
                y_data_array = curWeatherPolygon.getY_data()
                print "WeatherPolygon", i, ", number of vertices = ", curWeatherPolygon.getNum_vertices()
                
# Print more data
#                 print "    xmin = ", curWeatherPolygon.getXmin(), " xmax = ", curWeatherPolygon.getXmax(), \
#                 ", ymin = ", curWeatherPolygon.getYmin(), " ymax = ", curWeatherPolygon.getYmax(), \
#                 ", x_centroid = ", curWeatherPolygon.getX_centroid(), ", y_centroid = ", curWeatherPolygon.getY_centroid(), \
#                 ", poly_type = ", curWeatherPolygon.getPoly_type(), \
#                 ", start_hr = ", curWeatherPolygon.getStart_hr(), ", end_hr = ", curWeatherPolygon.getEnd_hr()
                
                for j in range(0, len(curWeatherPolygon.getX_data())) :
                    print "    x_data = ", x_data_array[j], ", y_data = ", y_data_array[j]
                
                print ""
    else :
        print "No weather polygon data found"

simulationInterface.resume()

while True:
    runtime_sim_status = simulationInterface.get_runtime_sim_status()
    if (runtime_sim_status == NATS_SIMULATION_STATUS_ENDED) :
        break
    else:
        time.sleep(1)

aircraftInterface.release_aircraft()
# end - Demo of getting conflicting weather polygon data ----------------------


environmentInterface.release_rap()

# Stop NATS Standalone environment
natsStandalone.stop()

shutdownJVM()
