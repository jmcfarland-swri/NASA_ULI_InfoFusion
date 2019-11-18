from NATS_Python_Header import *

import math

# Toggle to enable/disable aircraft data subscription during simulation.
SUBSCRIBE_TO_FLIGHTS = True

# Data structure for aircraft list and their states that would be updated with every time if subscription option is enabled.
AIRCRAFT_STATES = []
AIRCRAFT_LIST = []

print('This module illustrates the subscription feature to get updated flight data as simulation takes place. The trajectory is then plotted on Google Maps.')

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

equipmentInterface = natsStandalone.getEquipmentInterface()
aircraftInterface = equipmentInterface.getAircraftInterface()

# Function to get updated states of subscribed aircraft
def update_states():
    
    # Iterate through each aircraft.
    for aircraftCallsign in AIRCRAFT_LIST:
        # Get instance of the aircraft and updated states for key flight parameters.
        aircraftInstance = aircraftInterface.select_aircraft(aircraftCallsign)
        newLat = aircraftInstance.getLatitude_deg()
        newLon = aircraftInstance.getLongitude_deg()
        newAlt = aircraftInstance.getAltitude_ft()
        newRocd = aircraftInstance.getRocd_fps()
        newCourse = aircraftInstance.getCourse_rad()
        newSpeed = aircraftInstance.getTas_knots()
        
        # Add updated flight data to the aircraft state
        # Index of an aircraft maps consistently to the state variable. (For each aircraft, AIRCRAFT_LIST[i] <-----> AIRCRAFT_STATES[i])
        AIRCRAFT_STATES[AIRCRAFT_LIST.index(aircraftCallsign)] = [newLat, newLon, newAlt, newRocd, newCourse, newSpeed]
        
        # Print out debug log
        print("States for subscribed aircraft " + aircraftCallsign + " updated to:")
        print("Latitude: " + str(newLat) + " degrees")
        print("Longitude: " + str(newLon) + " degrees")
        print("Altitude: " + str(newAlt) + " feet")
        print("Rate of Climb/Descent: " + str(newRocd) + " feet/second")
        print("Course: " + str(newCourse * 180 / math.pi) + " degrees")
        print("True Airspeed: " + str(newSpeed) + " knots")
        print("\n")
    print("--------------------------------------------") 
  
if simulationInterface is None:
    print "Can't get SimInterface"

else:
    simulationInterface.clear_trajectory()
    environmentInterface.load_rap("share/tg/rap")

    aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_3Aircrafts_MergeSpace_test.trx", "share/tg/trx/TRX_DEMO_3Aircrafts_MergeSpace_test_mfl.trx")

    simulationInterface.setupSimulation(11000, 30)

    simulationInterface.start(600)

    #Set list of flights under simulation that are owned by this client to the flight list data structure.
    AIRCRAFT_LIST = list(aircraftInterface.getAllAircraftId())
    AIRCRAFT_STATES = [[] for x in AIRCRAFT_LIST]
    
    # Use a while loop to constantly check simulation status.  When the simulation finishes, continue to output the trajectory data
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            # Get flight data if subscription has been enabled
            if SUBSCRIBE_TO_FLIGHTS:
                update_states()
            time.sleep(1)

    simulationInterface.resume()

    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_ENDED) :
            break
        else:
            # Get flight data if subscription has been enabled
            if SUBSCRIBE_TO_FLIGHTS:
                update_states()
            time.sleep(1)

    millis = int(round(time.time() * 1000))
    print "Outputting trajectory data.  Please wait...."
    fileName = os.path.splitext(os.path.basename(__file__))[0] + "_" + str(millis) + ".csv"
    # Output the trajectory result file
    simulationInterface.write_trajectories(fileName)


    aircraftInterface.release_aircraft()
    environmentInterface.release_rap()

# Stop NATS Standalone environment
natsStandalone.stop()

shutdownJVM()

#Plot trajectory on Google Maps
PathVisualizer.plotOnGoogleMap(['SWA1897', 'SWA1898', 'SWA1899'], fileName)
