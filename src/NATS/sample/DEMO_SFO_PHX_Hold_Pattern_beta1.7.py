# This sample program demonstrates several hold patterns during simulation.
#
# Oliver Chen
# 10.02.2019
#

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

safetyMetricsInterface = natsStandalone.getSafetyMetricsInterface()

environmentInterface = natsStandalone.getEnvironmentInterface()
airportInterface = environmentInterface.getAirportInterface()
terminalAreaInterface = environmentInterface.getTerminalAreaInterface()
terrainInterface = environmentInterface.getTerrainInterface()

entityInterface = natsStandalone.getEntityInterface()
controllerInterface = entityInterface.getControllerInterface()
pilotInterface = entityInterface.getPilotInterface()

planned_dirname = ""
output_filename = ""

if simulationInterface is None:
    print "Can't get SimulationInterface"

else:
    simulationInterface.clear_trajectory()
    environmentInterface.load_rap("share/tg/rap")

    aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_SFO_PHX_GateToGate.trx", "share/tg/trx/TRX_DEMO_SFO_PHX_mfl.trx")
    
    simulationInterface.setupSimulation(20000, 30) # SFO - PHX

    simulationInterface.start(900)
    
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)
    
    # (1) Holding
    # Delay clearance of AIRCRAFT_CLEARANCE_ENTER_ARTC
    # This will cause aircraft stay in FLIGHT_PHASE_HOLD_IN_DEPARTURE_PATTERN
    controllerInterface.setDelayPeriod("SWA1897", AIRCRAFT_CLEARANCE_ENTER_ARTC, 2000)
    
    simulationInterface.resume(7000)
    
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)
    
    # (2) Holding
    # Delay clearance of AIRCRAFT_CLEARANCE_DESCENT_FROM_CRUISE
    # This will cause aircraft stay in FLIGHT_PHASE_HOLD_IN_ENROUTE_PATTERN
    controllerInterface.setDelayPeriod("SWA1897", AIRCRAFT_CLEARANCE_DESCENT_FROM_CRUISE, 1700)
    
    simulationInterface.resume(610)
    
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)
    
    # (3) Holding
    # Delay clearance of AIRCRAFT_CLEARANCE_ENTER_TRACON
    # This will cause aircraft stay in FLIGHT_PHASE_HOLD_IN_ARRIVAL_PATTERN
    controllerInterface.setDelayPeriod("SWA1897", AIRCRAFT_CLEARANCE_ENTER_TRACON, 1700)
    
    simulationInterface.resume(1660)
    
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)
    
    # (4) Holding
    # When entering FINAL_APPROACH phase
    # Delay clearance of AIRCRAFT_CLEARANCE_TOUCHDOWN for certain time which aircraft continues to descent to the altitude close to 500 ft above destination airport elevation
    # This will cause aircraft to GO AROUND
    controllerInterface.setDelayPeriod("SWA1897", AIRCRAFT_CLEARANCE_TOUCHDOWN, 2000)
    
    #Controller function to release hold and go to FFIXA waypoint to a new approach I07L
    #controllerInterface.releaseAircraftHold("SWA1897", "I07L", "FFIXA")
    
    #Controller function to release hold and resume simulation from FFIXA waypoint.
    #controllerInterface.releaseAircraftHold("SWA1897", "", "FFIXA")

    simulationInterface.resume(720)
    
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)
    
    # (5) Holding
    # When aircraft is in GO AROUND phase
    # Delay clearance of AIRCRAFT_CLEARANCE_APPROACH
    # This will cause aircraft to stay in FLIGHT_PHASE_HOLD_IN_ARRIVAL_PATTERN
    controllerInterface.setDelayPeriod("SWA1897", AIRCRAFT_CLEARANCE_APPROACH, 1700)
    
    simulationInterface.resume()
 
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
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

shutdownJVM()
