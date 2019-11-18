from NATS_Python_Header import *

print('This module illustrates the CNSInterface functions to model simulation situations. The trajectory is then plotted on Google Maps.')


clsNATSStandalone = JClass('NATSStandalone')
# Start NATS Standalone environment
natsStandalone = clsNATSStandalone.start()

if (natsStandalone is None) :
    print "Can't start NATS Standalone"
    quit()
    
simulationInterface = natsStandalone.getSimulationInterface()

equipmentInterface = natsStandalone.getEquipmentInterface()
aircraftInterface = equipmentInterface.getAircraftInterface()
cnsInterface = equipmentInterface.getCNSInterface()

environmentInterface = natsStandalone.getEnvironmentInterface()
airportInterface = environmentInterface.getAirportInterface()
terminalAreaInterface = environmentInterface.getTerminalAreaInterface()

entityInterface = natsStandalone.getEntityInterface()
controllerInterface = entityInterface.getControllerInterface()
pilotInterface = entityInterface.getPilotInterface()

safetyMetricsInterface = natsStandalone.getSafetyMetricsInterface()

if simulationInterface is None:
    print "Can't get SimInterface"

else:
    simulationInterface.clear_trajectory()
    environmentInterface.load_rap("share/tg/rap")

    aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_2Aircrafts_SafetyMetrics_test.trx", "share/tg/trx/TRX_DEMO_2Aircrafts_SafetyMetrics_test_mfl.trx")

    simulationInterface.setupSimulation(11000, 30)

    simulationInterface.start(120)

    #Set aircraft to be simulated
    aircraftCallsign = 'SWA1897'

    # Use a while loop to constantly check simulation status.  When the simulation finishes, continue to output the trajectory data
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)

    # CNS Functions usage
    print cnsInterface.getLineOfSight(33.440903, -111.992862, 1135, 33.274183, -112.147879, 1500)
    cnsInterface.setNavigationLocationError("SWA1897", "LATITUDE", 0.00005, 0.00000001, 0.9, 0.2, 1)
    cnsInterface.setNavigationLocationError("SWA1897", "LONGITUDE", 0.00005, 0.00000001, 0.9, 0.2, 1)
    cnsInterface.setNavigationAltitudeError("SWA1897", .00005, 0.2, 0)
    cnsInterface.setRadarError('KSFO', 'RANGE', 25, 0.0000005, 0.2, 1)
    cnsInterface.setRadarError('KSFO', 'AZIMUTH', 30, 0.0000005, 0.2, 1)
    cnsInterface.setRadarError('KSFO', 'ELEVATION', 2500, 0.0000005, 0.2, 1)

    simulationInterface.resume()

    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_ENDED) :
            break
        else:
            aircraft = aircraftInterface.select_aircraft('SWA1897')
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
#PathVisualizer.plotOnGoogleMap([aircraftCallsign], fileName)
