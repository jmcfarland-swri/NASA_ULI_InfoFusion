# NATS sample
#
# Optimal Synthesis Inc.
#
# Oliver Chen
# 10.01.2019
#
# Demo of changing aircraft state
#
# This program starts the simulation for a period of time then NATS pause automatically.
# When the simulation is at pause status, we change the aircraft state.
# When the simulation resumes, it continues to run the rest of the simulation until it finishes.
#
# Users can compare the trajectory data to see the change of aircraft state.

from NATS_Python_Header import *

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

entityInterface = natsStandalone.getEntityInterface()
controllerInterface = entityInterface.getControllerInterface()

if simulationInterface is None:
    print "Can't get SimulationInterface"

else:
    simulationInterface.clear_trajectory()
    environmentInterface.load_rap("share/tg/rap")
    
    aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_SFO_PHX_GateToGate.trx", "share/tg/trx/TRX_DEMO_SFO_PHX_mfl.trx")
    
    simulationInterface.setupSimulation(11000, 30)

    simulationInterface.start(1020)
    
    # Check simulation status.  Continue to next code when it is at PAUSE status
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)
    
    # =====================================================
    
    # Required
    # Every time at pause, get the latest aircraft data
    curAircraft = aircraftInterface.select_aircraft("SWA1897")
    if not (curAircraft is None):
        print "Setting new state to aircraft SWA1897"
        
        # Set new state value
        #curAircraft.setCruise_tas_knots(450)
        #curAircraft.setCruise_alt_ft(35000)
    
        curAircraft.setLatitude_deg(36.0)
        curAircraft.setLongitude_deg(-120.0)
    
    # =====================================================
    
    simulationInterface.resume(7110) # Resume and continue the simulation
    
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)
    
    # =====================================================
    
    # Required
    # Every time at pause, get the latest aircraft data
    curAircraft = aircraftInterface.select_aircraft("SWA1897")
    
    # Set new state value
    #curAircraft.setCruise_tas_knots(450)
    #curAircraft.setCruise_alt_ft(35000)
    
    curAircraft.setLatitude_deg(36.0)
    curAircraft.setLongitude_deg(-120.0)
    curAircraft.setAltitude_ft(32000.0)
    curAircraft.setTas_knots(400.0)
    curAircraft.setCourse_rad(110.0 * 3.1415926 / 180)
    curAircraft.setRocd_fps(50.0)
    
    # =====================================================
    
    simulationInterface.resume()
    
    # Use a while loop to constantly check simulation status.  When the simulation finishes, continue to output the trajectory data
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_ENDED) :
            break
        else:
            time.sleep(1)

    millis = int(round(time.time() * 1000))
    print "Outputting trajectory data.  Please wait...."
    # Output the trajectory result file
    simulationInterface.write_trajectories(os.path.splitext(os.path.basename(__file__))[0] + "_trajectory_" + str(millis) + ".csv")

    aircraftInterface.release_aircraft()
    environmentInterface.release_rap()


# Stop NATS Standalone environment
natsStandalone.stop()

shutdownJVM()
