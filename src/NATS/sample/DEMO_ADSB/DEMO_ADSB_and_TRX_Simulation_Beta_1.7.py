'''
This module is a demonstration to simulate live ADS-B flight data within NATS in real time. Along with this,
it also has a pre-loaded TRX file with virtual flights that are simulated alongside. Please refer to documentation
at sample/DEMO_ADSB/ADS-B Documentation Beta 1.7.pdf for installation and further details.

NOTE: Running this module requires ADS-B live feed via an RTL-SDR dongle connected to an antenna. To receive this hardware 
setup, please contact Optimal Synthesis Inc.
'''

from NATS_Header import *

clsNATSStandalone = JClass('NATSStandalone')
# Start NATS Standalone environment
natsStandalone = clsNATSStandalone.start()

if (natsStandalone is None) :
    print "Can't start NATS Standalone"
    quit()

def getUpdatedFlightData():
    url = 'http://localhost:8080/dump1090/data.json'  # where to get the aircraft.json
    headers = {'Cache-Control':'no-cache', 'Pragma':'no-cache', 'If-Modified-Since':'Sat, 1 Jan 2000 00:00:00 GMT', }
    
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request)

    data = response.read().decode('utf8')
    jsonPlane = json.loads(data)
    updatedFlights = []
    for plane in jsonPlane:
        resultStr = ''
        if (str(plane['flight']) is not '' and 
            float(plane['lat']) is not 0.0 and 
            float(plane['lon']) is not 0.0 and 
            float(plane['altitude']) is not 0.0 and 
            str(plane['vert_rate']) is not '' and 
            float(plane['speed']) is not 0.0 and 
            float(plane['track']) is not 0.0 and
            float(plane['seen']) <= 1):
            if 'flight' in plane:
                resultStr = resultStr + str(plane['flight']).strip() + ','
            else:
                resultStr = resultStr + ','
                
            if 'lat' in plane:
                resultStr = resultStr + str(plane['lat']) + ','
            else:
                resultStr = resultStr + ','
    
            if 'lon' in plane:
                resultStr = resultStr + str(plane['lon']) + ','
            else:
                resultStr = resultStr + ','
    
            if 'altitude' in plane:
                resultStr = resultStr + str(plane['altitude']) + ','
            else:
                resultStr = resultStr + ','
            
            if 'vert_rate' in plane:
                resultStr = resultStr + str(plane['vert_rate']) + ','
            else:
                resultStr = resultStr + ','
    
            if 'speed' in plane:
                resultStr = resultStr + str(plane['speed']) + ','
            else:
                resultStr = resultStr + ','
    
            if 'track' in plane:
                resultStr = resultStr + str(plane['track'])
            else:
                resultStr = resultStr + ','
    
            updatedFlights.append(resultStr)

    return updatedFlights
    
simulationInterface = natsStandalone.getSimulationInterface()

equipmentInterface = natsStandalone.getEquipmentInterface()
aircraftInterface = equipmentInterface.getAircraftInterface()

environmentInterface = natsStandalone.getEnvironmentInterface()
airportInterface = environmentInterface.getAirportInterface()
terminalAreaInterface = environmentInterface.getTerminalAreaInterface()


if simulationInterface is None:
    print "Can't get SimInterface"

else:
    simulationInterface.clear_trajectory()
    environmentInterface.load_rap("share/tg/rap")
    aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_2Aircrafts_SafetyMetrics_test.trx", "share/tg/trx/TRX_DEMO_2Aircrafts_SafetyMetrics_test_mfl.trx")

    traj_start_time = time.time() # UTC
    traj_origin_airport = "KPHX"
    traj_destination_airport = "KSFO"
    traj_cruise_alt = 33000.0
    traj_cruise_tas_knots = 430.0
    traj_origin_airport_elevation_ft = 13.0
    traj_destination_airport_elevation_ft = 1135.0

    time_step = 1  # sec
    cnt_loop = 0
    max_cnt_loop = 15  # Number of loop to be processed
    
    array_index = -1

    
    simulationInterface.startRealTime()
    callsignsInFlight = []
    while(cnt_loop < max_cnt_loop):
        updatedFlights = getUpdatedFlightData()
        
        for flight in updatedFlights:
            flightParams = flight.split(",")
            traj_ac_id = flightParams[0]
            traj_ac_type = "AIRCRAFT_TYPE"
            traj_lat = float(flightParams[1])
            traj_lon = float(flightParams[2])
            traj_alt = float(flightParams[3])
            traj_rocd = float(flightParams[4])
            traj_tas_knots = float(flightParams[5])
            traj_tas_knots_ground = float(flightParams[5])
            traj_course_deg = float(flightParams[6])
            traj_fpa_deg = 0.0
            traj_sector_index = 5
            traj_flight_phase = str(FLIGHT_PHASE_CRUISE) #Placeholder for now, dynamic flight phase from ADS-B would be added to the simulation eventually.

            # Inject real-time trajectory state data
            t = int(round(time.time() * 1000))

            if traj_ac_id not in callsignsInFlight:
                simulationInterface.externalAircraft_create_trajectory_profile(traj_ac_id, traj_ac_type, traj_origin_airport, traj_destination_airport, traj_cruise_alt, traj_cruise_tas_knots, traj_lat, traj_lon, traj_alt, traj_rocd, traj_tas_knots, traj_course_deg, traj_flight_phase)
                callsignsInFlight.append(traj_ac_id)
            else:
                simulationInterface.externalAircraft_inject_trajectory_state_data(traj_ac_id, traj_lat, traj_lon, traj_alt, traj_tas_knots, traj_course_deg, traj_fpa_deg, traj_flight_phase, t)

        cnt_loop = cnt_loop + 1
        time.sleep(time_step)


    # Stop simulation
    simulationInterface.stop()


    millis = int(round(time.time() * 1000))
    print "Outputting trajectory data.  Please wait...."
    simulationInterface.write_trajectories("ADSB_" + os.path.splitext(os.path.basename(__file__))[0] + "_" + str(millis) + ".csv")

    aircraftInterface.release_aircraft()
    environmentInterface.release_rap()


# Stop NATS Standalone environment
natsStandalone.stop()

shutdownJVM()
