# NATS sample
#
# Optimal Synthesis Inc.
#
# Oliver Chen
# 09.27.2019
#
# Demo of gate-to-gate trajectory simulation.
#
# The aircraft starts from the origin gate, goes through departing taxi plan, takes off, goes through different flight phases to the destination airport, and finally reaches the destination gate.

from NATS_Python_Header import *
print('Imported NATS')
clsNATSStandalone = JClass('NATSStandalone')

# Start NATS Standalone environment
natsStandalone = clsNATSStandalone.start()

if (natsStandalone is None) :
    print("Can't start NATS Standalone")
    quit()

simulationInterface = natsStandalone.getSimulationInterface()

entityInterface = natsStandalone.getEntityInterface()
controllerInterface = entityInterface.getControllerInterface()
pilotInterface = entityInterface.getPilotInterface()

environmentInterface = natsStandalone.getEnvironmentInterface()

equipmentInterface = natsStandalone.getEquipmentInterface()
aircraftInterface = equipmentInterface.getAircraftInterface()

safetyMetricsInterface = natsStandalone.getSafetyMetricsInterface()

if simulationInterface is None:
    print("Can't get SimulationInterface")

else:
    simulationInterface.clear_trajectory()

    #environmentInterface.load_rap("share/tg/rap")

    aircraftInterface.load_aircraft("trxSwRI/TRX_DEMO_Combined_GateToGate.trx", "trxSwRI/TRX_DEMO_Combined_GateToGate_mfl.trx")
  
#     # Controller to set human error: delay time
#     # Users can try the following setting and see the difference in trajectory

    for ac in aircraftInterface.getAllAircraftId():
        print('Changing controllerInterface parameters for {}'.format(ac))
        controllerInterface.setDelayPeriod(ac, AIRCRAFT_CLEARANCE_PUSHBACK, 20.1)
        controllerInterface.setDelayPeriod(ac, AIRCRAFT_CLEARANCE_TAXI_DEPARTING, 20)
        controllerInterface.setDelayPeriod(ac, AIRCRAFT_CLEARANCE_TAKEOFF, 20)
        controllerInterface.setDelayPeriod(ac, AIRCRAFT_CLEARANCE_ENTER_ARTC, 20)
        controllerInterface.setDelayPeriod(ac, AIRCRAFT_CLEARANCE_DESCENT_FROM_CRUISE, 20)
        controllerInterface.setDelayPeriod(ac, AIRCRAFT_CLEARANCE_ENTER_TRACON, 20)
        controllerInterface.setDelayPeriod(ac, AIRCRAFT_CLEARANCE_APPROACH, 20)
        controllerInterface.setDelayPeriod(ac, AIRCRAFT_CLEARANCE_TOUCHDOWN, 20)
        controllerInterface.setDelayPeriod(ac, AIRCRAFT_CLEARANCE_TAXI_LANDING, 20)
        controllerInterface.setDelayPeriod(ac, AIRCRAFT_CLEARANCE_RAMP_LANDING, 20)
        currAircraft = aircraftInterface.select_aircraft(ac)
        currAircraft.delay_departure(100)
    

    simulationInterface.setupSimulation(12000, 1,1,1) # SFO - PHX

    simulationInterface.start()
               
    # Use a while loop to constantly check simulation status.  When the simulation finishes, continue to output the trajectory data
    # while True:
    #     runtime_sim_status = simulationInterface.get_runtime_sim_status()
    #     print('1st Status: ', simulationInterface.get_runtime_sim_status(), 'Time: ',simulationInterface.get_curr_sim_time())
    #     if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
    #         print('Paused at: ', simulationInterface.get_curr_sim_time())
    #         break
    #     else:
    #         time.sleep(1)
     
    # # Pilot to set error scenarios
    # # Users can try the following setting and see the difference in trajectory
    # for ac in aircraftInterface.getAllAircraftId():
    #     print('Changing pilotInterface parameters for {}'.format(ac))
    #     #pilotInterface.setActionLag(ac, 'COURSE', 10, 0.0, 60)
    #     #pilotInterface.setActionLag(ac, 'ALTITUDE', 10, 0.0, 60)
    #     #pilotInterface.setActionLag(ac, 'VERTICAL_SPEED', 10, 0.0, 60)

    # print('Status before resume: ', simulationInterface.get_runtime_sim_status(), 'Time: ',simulationInterface.get_curr_sim_time())
    # simulationInterface.resume()
    # print('Status after resume: ', simulationInterface.get_runtime_sim_status(), 'Time: ',simulationInterface.get_curr_sim_time())
  
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        print('2st Status: ', simulationInterface.get_runtime_sim_status(), 'Time: ',simulationInterface.get_curr_sim_time())
        if (runtime_sim_status == NATS_SIMULATION_STATUS_ENDED) :
            print('Ended at: ', simulationInterface.get_curr_sim_time())
            break
        else:
            time.sleep(1)
  
    millis = int(round(time.time() * 1000))
    print("Outputting trajectory data.  Please wait....")
  
    planned_dirname = os.path.splitext(os.path.basename(__file__))[0] + "_" + str(millis)
    output_filename = planned_dirname + ".csv"
      
    # Output the trajectory result file
    simulationInterface.write_trajectories(output_filename)
      
    aircraftInterface.release_aircraft()
    environmentInterface.release_rap()

# =========================================================
 
# The following statements read the result trajectory files and display plotting.
  
# Create temp directory and copy the result trajectory file into it
planned_dirname = "tmp_" + planned_dirname
os.makedirs(planned_dirname)
   
local_trajectory_filename = output_filename
   
copyfile(local_trajectory_filename, planned_dirname + "/" + local_trajectory_filename)

#post_process = pp.PostProcessor(file_path = planned_dirname,
#                                ac_name = 'SWA1897');
                                   
#post_process.plotSingleAircraftTrajectory();
   
# Delete temp directory
print("Deleting directory:", planned_dirname)
rmtree(planned_dirname)

# Stop NATS Standalone environment
natsStandalone.stop()

shutdownJVM()
