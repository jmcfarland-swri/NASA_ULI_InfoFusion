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

equipmentInterface = natsStandalone.getEquipmentInterface()
aircraftInterface = equipmentInterface.getAircraftInterface()

if simulationInterface is None:
    print "Can't get SimulationInterface"

else:
    simulationInterface.clear_trajectory()

    environmentInterface.load_rap("share/tg/rap")

    aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_SFO_PHX_GateToGate.trx", "share/tg/trx/TRX_DEMO_SFO_PHX_mfl.trx")
  
#     # Controller to set human error: delay time
#     # Users can try the following setting and see the difference in trajectory
    #controllerInterface.setDelayPeriod("SWA1897", AIRCRAFT_CLEARANCE_PUSHBACK, 7)
    #controllerInterface.setDelayPeriod("SWA1897", AIRCRAFT_CLEARANCE_TAKEOFF, 20)

    simulationInterface.setupSimulation(12000, 30) # SFO - PHX

    simulationInterface.start(660)
               
    # Use a while loop to constantly check simulation status.  When the simulation finishes, continue to output the trajectory data
    while True:
        runtime_sim_status = simulationInterface.get_runtime_sim_status()
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE) :
            break
        else:
            time.sleep(1)
     
    # Pilot to set error scenarios
    # Users can try the following setting and see the difference in trajectory
    #pilotInterface.skipFlightPhase('SWA1897', 'FLIGHT_PHASE_CLIMB_TO_CRUISE_ALTITUDE')
    #pilotInterface.setActionRepeat('SWA1897', "VERTICAL_SPEED")
    #pilotInterface.setWrongAction('SWA1897', "AIRSPEED", "FLIGHT_LEVEL")
    #pilotInterface.setActionReversal('SWA1897', 'VERTICAL_SPEED')
    #pilotInterface.setPartialAction('SWA1897', 'COURSE', 200, 50)
    #pilotInterface.skipChangeAction('SWA1897', 'COURSE')
    #pilotInterface.setActionLag('SWA1897', 'COURSE', 10, 0.05, 60)

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

# =========================================================
 
# The following statements read the result trajectory files and display plotting.
  
# Create temp directory and copy the result trajectory file into it
planned_dirname = "tmp_" + planned_dirname
os.makedirs(planned_dirname)
   
local_trajectory_filename = output_filename
   
copyfile(local_trajectory_filename, planned_dirname + "/" + local_trajectory_filename)
   
post_process = pp.PostProcessor(file_path = planned_dirname,
                                ac_name = 'SWA1897');
                                   
post_process.plotSingleAircraftTrajectory();
   
# Delete temp directory
print "Deleting directory:", planned_dirname
rmtree(planned_dirname)

# Stop NATS Standalone environment
natsStandalone.stop()

shutdownJVM()
