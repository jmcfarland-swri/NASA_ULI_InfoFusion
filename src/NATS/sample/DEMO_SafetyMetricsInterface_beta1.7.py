from NATS_Python_Header import *

print('This module illustrates the SafetyMetricsInterface functions to model simulation situations. The trajectory is then plotted on Google Maps.')

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

if simulationInterface is None:
    print "Can't get SimInterface"

else:
    simulationInterface.clear_trajectory()
    environmentInterface.load_rap("share/tg/rap")

    aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_2Aircrafts_SafetyMetrics_test.trx", "share/tg/trx/TRX_DEMO_2Aircrafts_SafetyMetrics_test_mfl.trx")

    # Controller to set human error: delay time
    #controllerInterface.setDelayPeriod("SWA1897", AIRCRAFT_CLEARANCE_PUSHBACK, 7)
    #controllerInterface.setDelayPeriod("SWA1897", AIRCRAFT_CLEARANCE_TAKEOFF, 20)

    simulationInterface.setupSimulation(11000, 30) # SFO - PHX

    simulationInterface.start(3090)
    
    #Set aircraft to be simulated
    aircraftCallsign = 'SWA1897'

    # Use a while loop to constantly check simulation status.
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)

    #print(safetyMetricsInterface.getFlightsInRange('SWA1897'))
    #print(safetyMetricsInterface.getDistanceToRunwayThreshold('SWA1897'))
    #print(safetyMetricsInterface.getDistanceToRunwayEnd('SWA1897'))
    #print(safetyMetricsInterface.getVelocityAlignmentWithRunway('SWA1897', 'ARRIVAL'))
    #print(safetyMetricsInterface.getPassengerCount('A306'))
    print(safetyMetricsInterface.getAircraftCost('A306'))

    simulationInterface.resume()

    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_ENDED) :
            break
        else:
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
PathVisualizer.plotOnGoogleMap([aircraftCallsign], fileName)