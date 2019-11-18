# NATS sample
#
# Optimal Synthesis Inc.
#
# Oliver Chen
# 10.03.2019
#
# This sample demonstrates how to use accident incident sequence functionality to simulate accidents.
# US1549 aircraft incident is simulated to show the whole event and the aircraft finally landed on Hudson river at the border of New Jersey and New York states.
#
# Notice
# Current CIFP data doesn't contain the appropriate SID procedure to represent US1549 path.
# In order to demo the accident, we use temporary SID and have manual work changing waypoints after loading aircraft. 

from NATS_Python_Header import *

print('This module illustrates the simulation of Hudson River accident of US1549 flight.')

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

safetyMetricsInterface = natsStandalone.getSafetyMetricsInterface()


simulationInterface.clear_trajectory()

environmentInterface.load_rap("share/tg/rap")

aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_HudsonMiracle_beta1.6.trx", "share/tg/trx/TRX_DEMO_HudsonMiracle_mfl_beta1.6.trx")

# Customization of waypoints
# Notice
#     This is to fix the missing of SID procedure LGA5 in KLGA airport
#     The followings are not required operations for simulation of accident sequence
# ==================================================================================
controllerInterface.deleteAirborneWaypoint("US1549", 0)
controllerInterface.deleteAirborneWaypoint("US1549", 0)
controllerInterface.deleteAirborneWaypoint("US1549", 0)

controllerInterface.insertAirborneWaypoint("US1549", \
        0, \
        "SID", \
        "RW04-KLGA", \
        40.76928, \
        -73.884028, \
        21, \
        -10000, \
        "")

controllerInterface.insertAirborneWaypoint("US1549", \
        1, \
        "SID", \
        "HEADING OR COURSE_TO_INTERCEPT_RW04-KLGA_LGA", \
        40.826961, \
        -73.836284, \
        1200, \
        -10000, \
        "")

controllerInterface.setTargetWaypoint("US1549", 1)
# end - Customization of waypoints

safetyMetricsInterface.load_FlightPhaseSequence("share/tg/ifs/US1549AccidentFlightSequence.ifs")

simulationInterface.setupSimulation(600, 30)

simulationInterface.start()

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

safetyMetricsInterface.clear_FlightPhaseSequence();

# Stop NATS Standalone environment
natsStandalone.stop()

shutdownJVM()
