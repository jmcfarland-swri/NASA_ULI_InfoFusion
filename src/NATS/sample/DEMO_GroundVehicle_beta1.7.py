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
groundVehicleInterface = equipmentInterface.getGroundVehicleInterface()

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

    groundVehicleInterface.load_groundVehicle("share/tg/trx/TRX_DEMO_11GroundVehicles.trx")

    # Add external ground vehicle
    #groundVehicleInterface.externalGroundVehicle_create_trajectory_profile('NEW123', 'DWA1897', 'KSFO', 37, -122, 15, 28)
    #print(groundVehicleInterface.getAllGroundVehicleIds())

    '''
    bus = groundVehicleInterface.select_groundVehicle('BUS123')
    print(bus.getGvid())
    print(bus.getAirportId())
    print(bus.getAircraftInService())
    print(bus.getLatitude())
    print(bus.getLongitude())
    print(bus.getAltitude())
    print(bus.getSpeed())
    print(bus.getCourse())
    print(bus.getDeparture_time())
    print(bus.getDrive_plan_length())
    print(bus.getTarget_waypoint_index())
    print(bus.getTarget_waypoint_name())
    print(bus.getDrive_plan_latitude_array())
    print(bus.getDrive_plan_longitude_array())
    print(bus.getDrive_plan_waypoint_name_array())


    bus.setCourse(1.4)

    bus = groundVehicleInterface.select_groundVehicle('BUS123')
    print(bus.getGvid())
    print(bus.getAirportId())
    print(bus.getAircraftInService())
    print(bus.getLatitude())
    print(bus.getLongitude())
    print(bus.getAltitude())
    print(bus.getSpeed())
    print(bus.getCourse())
    print(bus.getDeparture_time())
    print(bus.getDrive_plan_length())
    print(bus.getTarget_waypoint_index())
    print(bus.getTarget_waypoint_name())
    print(bus.getDrive_plan_latitude_array())
    print(bus.getDrive_plan_longitude_array())
    print(bus.getDrive_plan_waypoint_name_array())
    '''
    simulationInterface.setupSimulation(11000, 30) # SFO - PHX

    simulationInterface.start()

    #Set aircraft to be simulated
    aircraftCallsign = 'SWA1897'

    # Use a while loop to constantly check simulation status.  When the simulation finishes, continue to output the trajectory data
    '''
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)

    simulationInterface.resume()
    '''
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_ENDED) :
            break
        else:
            time.sleep(1)

    millis = int(round(time.time() * 1000))
    print "Outputting trajectory data.  Please wait...."
    fileName = os.path.splitext(os.path.basename(__file__))[0] + "_" + str(millis) + ".csv"
    simulationInterface.write_trajectories(fileName)

    groundVehicleInterface.release_groundVehicle()
    aircraftInterface.release_aircraft()
    environmentInterface.release_rap()

# Stop NATS Standalone environment
natsStandalone.stop()

shutdownJVM()