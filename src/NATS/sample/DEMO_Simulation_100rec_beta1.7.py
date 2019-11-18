# NATS sample
#
# Optimal Synthesis Inc.
#
# Oliver Chen
# 10.02.2019
#
# Demo of trajectory simulation on 100 flights for 86400 sec(1 day)

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

    aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_100rec_beta1.5.trx", "share/tg/trx/TRX_DEMO_100rec_mfl_beta1.5.trx")

    simulationInterface.setupSimulation(86400, 30)

    simulationInterface.start()
             
    # Use a while loop to constantly check simulation status.  When the simulation finishes, continue to output the trajectory data
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
PathVisualizer.plotOnGoogleMap(['ULI-3AFSD3DC24', 'ULI-3E6A0495F1', 'ULI-FEA47106EB', 'ULI-3AFAB4BC27', 'ULI-707397319B'], fileName)
