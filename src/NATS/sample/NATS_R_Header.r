# This is the header file for running R examples

# Java initialization with rJava library, setting up JARs to access NATS functions. rJava can be installed by running install.packages("rJava") in R shell.
library(rJava)
.jinit('.')
.jaddClassPath(paste('dist/nats-client.jar', sep = ""))
.jaddClassPath(paste('dist/nats-shared.jar', sep = ""))
.jaddClassPath(paste('dist/nats-standalone.jar', sep = ""))
.jaddClassPath(paste('dist/commons-logging-1.2.jar', sep = ""))
.jaddClassPath(paste('dist/json.jar', sep = ""))
.jaddClassPath(paste('dist/rmiio-2.1.2.jar', sep = ""))

# Initialize NATS variables
aircraftClearance <- .jnew('com.osi.util.AircraftClearanceReference')
constants <- .jnew('com.osi.util.Constants')


AIRCRAFT_CLEARANCE_PUSHBACK <- aircraftClearance$AIRCRAFT_CLEARANCE_PUSHBACK
AIRCRAFT_CLEARANCE_TAXI_DEPARTING <- aircraftClearance$AIRCRAFT_CLEARANCE_TAXI_DEPARTING
AIRCRAFT_CLEARANCE_TAKEOFF <- aircraftClearance$AIRCRAFT_CLEARANCE_TAKEOFF
AIRCRAFT_CLEARANCE_ENTER_ARTC <- aircraftClearance$AIRCRAFT_CLEARANCE_ENTER_ARTC
AIRCRAFT_CLEARANCE_DESCENT_FROM_CRUISE <- aircraftClearance$AIRCRAFT_CLEARANCE_DESCENT_FROM_CRUISE
AIRCRAFT_CLEARANCE_ENTER_TRACON <- aircraftClearance$AIRCRAFT_CLEARANCE_ENTER_TRACON
AIRCRAFT_CLEARANCE_APPROACH <- aircraftClearance$AIRCRAFT_CLEARANCE_APPROACH
AIRCRAFT_CLEARANCE_TOUCHDOWN <- aircraftClearance$AIRCRAFT_CLEARANCE_TOUCHDOWN
AIRCRAFT_CLEARANCE_TAXI_LANDING <- aircraftClearance$AIRCRAFT_CLEARANCE_TAXI_LANDING
AIRCRAFT_CLEARANCE_RAMP_LANDING <- aircraftClearance$AIRCRAFT_CLEARANCE_RAMP_LANDING


NATS_SIMULATION_STATUS_READY <- constants$NATS_SIMULATION_STATUS_READY
NATS_SIMULATION_STATUS_START <- constants$NATS_SIMULATION_STATUS_START
NATS_SIMULATION_STATUS_PAUSE <- constants$NATS_SIMULATION_STATUS_PAUSE
NATS_SIMULATION_STATUS_RESUME <- constants$NATS_SIMULATION_STATUS_RESUME
NATS_SIMULATION_STATUS_STOP <- constants$NATS_SIMULATION_STATUS_STOP
NATS_SIMULATION_STATUS_ENDED <- constants$NATS_SIMULATION_STATUS_ENDED
