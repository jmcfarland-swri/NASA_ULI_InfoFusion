'''
This module illustrates the function under SafetyMetricsInterface to model wake vortex. The trajectory is then plotted on Google Maps.
Details for the function usage can be found in the API documentation.
NATS_Client/sample/WakeVortexEnvelope.png has an illustration for the same.
'''

from NATS_Python_Header import *

print('This module illustrates the function under SafetyMetricsInterface to model wake vortex. The trajectory is then plotted on Google Maps.')

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

if simulationInterface is None:
    print "Can't get SimInterface"

else:
    simulationInterface.clear_trajectory()
    environmentInterface.load_rap("share/tg/rap")

    aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_2Aircrafts_WakeVortex_test.trx", "share/tg/trx/TRX_DEMO_2Aircrafts_WakeVortex_test_mfl.trx")

    simulationInterface.setupSimulation(11000, 30)

    simulationInterface.start(5000)

    # Set aircraft to be simulated
    aircraftCallsign = 'SWA1897'
    aircraftInstance = aircraftInterface.select_aircraft(aircraftCallsign)

    # Use a while loop to constantly check simulation status.  When the simulation finishes, continue to output the trajectory data
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)

    # Wake Vortex function, refer API documentation for details
    # Function usage: getFlightsInWakeVortexRange(String refAircraftId, float envelopeStartLength, float envelopeStartBreadth, float envelopeEndLength, float envelopeEndBreadth, float envelopeRangeLength, float envelopeDecline)
    aircraftInterface.select_aircraft("SWA1898").setLatitude_deg(aircraftInterface.select_aircraft("SWA1897").getLatitude_deg() - 0.0001)
    aircraftInterface.select_aircraft("SWA1898").setLongitude_deg(aircraftInterface.select_aircraft("SWA1897").getLongitude_deg() - 0.0001)
    aircraftInterface.select_aircraft("SWA1898").setCourse_rad(aircraftInterface.select_aircraft("SWA1897").getCourse_rad())

    print(safetyMetricsInterface.getFlightsInWakeVortexRange('SWA1897', 5000, 2000, 400, 350, 5, 0))

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
