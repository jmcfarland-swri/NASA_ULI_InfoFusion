# NATS sample
#
# Optimal Synthesis Inc.
#
# Oliver Chen
# 10.01.2019
#
# Demo of aircraft-related functions.
#
# Users can learn how to obtain aircraft instance, show related aircraft information, start/pause/resume simulation and output result trajectory file.

from NATS_Python_Header import *

import datetime

clsNATSStandalone = JClass('NATSStandalone')
# Start NATS Standalone environment
natsStandalone = clsNATSStandalone.start()

if (natsStandalone is None) :
    print "Can't start NATS Standalone"
    quit()
    
simulationInterface = natsStandalone.getSimulationInterface()

equipmentInterface = natsStandalone.getEquipmentInterface()
aircraftInterface = equipmentInterface.getAircraftInterface()

environmentInterface = natsStandalone.getEnvironmentInterface()
airportInterface = environmentInterface.getAirportInterface()
terminalAreaInterface = environmentInterface.getTerminalAreaInterface()

planned_dirname = ""
output_filename = ""

if simulationInterface is None:
    print "Can't get SimulationInterface"

else:
    simulationInterface.clear_trajectory()
    
    environmentInterface.load_rap("share/tg/rap")
    aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_100rec_beta1.5.trx", "share/tg/trx/TRX_DEMO_100rec_mfl_beta1.5.trx")
    
    if not(aircraftInterface is None):
        aircraftIdArray_withinZone = aircraftInterface.getAircraftIds(float(30.0), float(35.0), float(-115.0), float(-90.0), float(-1.0), float(-1.0))
        if (not(aircraftIdArray_withinZone is None) and (len(aircraftIdArray_withinZone) > 0)) :
            i = 0
            for i in range(0, len(aircraftIdArray_withinZone)):
                curAcId = aircraftIdArray_withinZone[i]
                print "Aircraft id in selected zone = ", curAcId
        
        print "****************************************"
        
        curAircraft = aircraftInterface.select_aircraft("ULI-3AFSD3DC24")
        if not(curAircraft is None):
            airborne_flight_plan_waypoint_name_array = curAircraft.getFlight_plan_waypoint_name_array()
            for j in range(0, len(airborne_flight_plan_waypoint_name_array)) :
                print "ULI-3AFSD3DC24 airborne flight plan waypoint name = ", airborne_flight_plan_waypoint_name_array[j]
            print ""

        aircraft_3E6A0495F1 = aircraftInterface.select_aircraft("ULI-3E6A0495F1")
        aircraft_3E6A0495F1.delay_departure(100) # Delay the departure time for 100 sec
        
    simulationInterface.setupSimulation(12000, 10)
    
    # Start the simulation for 1000 secs then pause
    simulationInterface.start(1000)

    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        print "Time:", datetime.datetime.now(), ", simulation continuing.... "
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)

    aircraft_3E6A0495F1 = aircraftInterface.select_aircraft("ULI-3E6A0495F1")
    if not(aircraft_3E6A0495F1 is None):
        print "****************************************"
        print "ULI-3E6A0495F1 (pausing at", simulationInterface.get_curr_sim_time(), "sec), latitude = ", aircraft_3E6A0495F1.getLatitude_deg(), ", longitude = ", aircraft_3E6A0495F1.getLongitude_deg(), ", altitude = ", aircraft_3E6A0495F1.getAltitude_ft()
        print "****************************************"
    
    # Resume and continue the simulation
    simulationInterface.resume()
    
    # Use a while loop to constantly check simulation status.  When the simulation finishes, continue to output the trajectory data
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        print "Time:", datetime.datetime.now(), ", simulation continuing.... "
        if (runtime_sim_status == NATS_SIMULATION_STATUS_ENDED) :
            break
        else:
            time.sleep(1)

    millis = int(round(time.time() * 1000))
    print "Outputting trajectory data.  Please wait...."
    
    planned_dirname = os.path.splitext(os.path.basename(__file__))[0] + "_" + str(millis)
    output_filename = planned_dirname + ".csv"
    
    # Output the trajectory result file
    simulationInterface.write_trajectories(output_filename)
    
    aircraftInterface.release_aircraft()
    environmentInterface.release_rap()


# Stop NATS Standalone environment
natsStandalone.stop()

# =========================================================

# The following statements read the result trajectory files and display plotting.

# Create temp directory and copy the result trajectory file into it
planned_dirname = "tmp_" + planned_dirname
os.makedirs("../NATS_Standalone/" + planned_dirname)
copyfile("../NATS_Standalone/" + output_filename, "../NATS_Standalone/" + planned_dirname + "/" + output_filename)

post_process = pp.PostProcessor(file_path = "../NATS_Standalone/" + planned_dirname,
                                ac_name = 'ULI-3AFSD3DC24');
post_process.plotSingleAircraftTrajectory();

# Delete temp directory
print "Deleting directory:", planned_dirname
rmtree("../NATS_Standalone/" + planned_dirname) 

shutdownJVM()