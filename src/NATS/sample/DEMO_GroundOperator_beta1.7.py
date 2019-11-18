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
cnsInterface = equipmentInterface.getCNSInterface()
groundVehicleInterface = equipmentInterface.getGroundVehicleInterface()

environmentInterface = natsStandalone.getEnvironmentInterface()
airportInterface = environmentInterface.getAirportInterface()
terminalAreaInterface = environmentInterface.getTerminalAreaInterface()

entityInterface = natsStandalone.getEntityInterface()
controllerInterface = entityInterface.getControllerInterface()
pilotInterface = entityInterface.getPilotInterface()
groundOperatorInterface = entityInterface.getGroundOperatorInterface()

if simulationInterface is None:
    print "Can't get SimInterface"

else:
    simulationInterface.clear_trajectory()
    
    environmentInterface.load_rap("share/tg/rap")

    groundVehicleInterface.load_groundVehicle("share/tg/trx/TRX_DEMO_11GroundVehicles.trx")
    #groundVehicleInterface.externalGroundVehicle_create_trajectory_profile('NEW123', 'DWA1897', 'KSFO', 37, -122, 15, 28)

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

    # Ground Operator function
    #groundOperatorInterface.setActionRepeat('BUS123', 'COURSE')
    #groundOperatorInterface.setVehicleContact('BUS123')
    groundOperatorInterface.setWrongAction('BUS123', 'SPEED', 'COURSE')
    #groundOperatorInterface.setActionReversal('BUS123', 'COURSE')
    #groundOperatorInterface.setPartialAction('BUS123', 'SPEED', 10, 50)
    #groundOperatorInterface.setGroundOperatorAbsence('BUS123', 4)
    #groundOperatorInterface.setActionLag('BUS123', 'SPEED', 10, 0.5, 30)

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

    groundVehicleInterface.release_groundVehicle()
    aircraftInterface.release_aircraft()
    environmentInterface.release_rap()

# Stop NATS Standalone environment
natsStandalone.stop()

shutdownJVM()