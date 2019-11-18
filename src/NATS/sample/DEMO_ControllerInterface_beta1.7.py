from NATS_Python_Header import *

print('This module illustrates the ControllerInterface functions to model simulation situations. The trajectory is then plotted on Google Maps.')

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
pilotInterface = entityInterface.getPilotInterface()

if simulationInterface is None:
    print "Can't get SimInterface"

else:
    simulationInterface.clear_trajectory()
    environmentInterface.load_rap("share/tg/rap")

    aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_2Aircrafts_SafetyMetrics_test.trx", "share/tg/trx/TRX_DEMO_2Aircrafts_SafetyMetrics_test_mfl.trx")

    simulationInterface.setupSimulation(12000, 30) # SFO - PHX

    simulationInterface.start(600)

    #Set aircraft to be simulated
    aircraftCallsign = 'SWA1897'

    # Use a while loop to constantly check simulation status
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)

    # Set controller functions
    # Some function may stop the aircraft from continuing moving forward.  If it happens, the plotting of the result trajectory will show nothing.
    controllerInterface.setDelayPeriod("SWA1897", AIRCRAFT_CLEARANCE_TAKEOFF, 20)
    #controllerInterface.skipFlightPhase('SWA1897', 'FLIGHT_PHASE_CLIMB_TO_CRUISE_ALTITUDE')
    #controllerInterface.setActionRepeat('SWA1897', "VERTICAL_SPEED")
    #controllerInterface.setWrongAction('SWA1897', "AIRSPEED", "FLIGHT_LEVEL")
    #controllerInterface.setActionReversal('SWA1897', 'VERTICAL_SPEED')
    #controllerInterface.setPartialAction('SWA1897', 'COURSE', 200, 50)
    #controllerInterface.skipChangeAction('SWA1897', 'COURSE')
    #controllerInterface.setActionLag('SWA1897', 'COURSE', 90, 0.05, -110)
    #controllerInterface.setControllerAbsence(aircraftCallsign, 6)

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