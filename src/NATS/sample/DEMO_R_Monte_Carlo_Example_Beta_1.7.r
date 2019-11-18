
# This is a prototype example of an R program to access NATS functions.
# It runs a Monte Carlo Simulation on controller absence time and saves plots of aircraft
# trajectory, speed, altitude, vertical speed with respect to time.

# The graphs are by default saved as a PDF file. If using RStudio, the graph plotting can be enhanced
# with interactive plotting.


# Initialize all variables for standalone NATS
source("sample/NATS_R_Header.r")
clsNATSStandalone <- .jnew('NATSStandalone')

# Start NATS Standalone environment
natsStandalone <- clsNATSStandalone$start()

# Initializing NATS Interfaces and variables
simulationInterface <- natsStandalone$getSimulationInterface()
equipmentInterface <- natsStandalone$getEquipmentInterface()
entityInterface <- natsStandalone$getEntityInterface()
aircraftInterface <- equipmentInterface$getAircraftInterface()
environmentInterface <- natsStandalone$getEnvironmentInterface()
airportInterface <- environmentInterface$getAirportInterface()
terminalAreaInterface <- environmentInterface$getTerminalAreaInterface()
controllerInterface <- entityInterface$getControllerInterface()

if (is.null(natsStandalone)) {
    print("Can't start NATS Standalone")
    quit()
}

# Attributes to perturb, can be any among 'AIRSPEED', 'ALTITUDE', 'WAYPOINT_LATITUDE_AND_LONGITUDE', 'WAYPOINT_LONGITUDE', 'WAYPOINT_LATITUDE', 'CURRENT_LATITUDE', 'CURRENT_LONGITUDE', 'CURRENT_LATITUDE_AND_LONGITUDE'

PERTURB_ATTRIBUTES <- list('ALTITUDE')
time <- c()
speed <- c()
altitude <- c()
rocd <- c()
course <- c()
latitude <- c()
longitude <- c()

#Monte-Carlo Simulation setup for perturbing true air speed (feet) and controller absense time (time steps)
aircraftID <- 'SWA1897'
meanAltitude <- 25000
sampleSize <- 10
meanTimeStep <- 6
timeStepVector = meanTimeStep + matrix(rnorm(sampleSize*1), sampleSize, 1)
altitudeVector = meanAltitude + 1000*matrix(rnorm(sampleSize*1), sampleSize, 1)

#Monte-Carlo Simulation setup for perturbing true air speed (knots)
#Please enter target aircraft callsign here. SWA1897 is an example.
#aircraftID <- 'SWA1897'
#meanAirspeedSpeed <- 450
#sampleSize <- 10
#airspeedVector <- meanAirspeedSpeed + 10*matrix(rnorm(sampleSize*1), sampleSize, 1)

#Monte-Carlo Simulation setup for perturbing geo coordinates (latitude and longitude)
#Please enter target aircraft callsign here. SWA1897 is an example.
#aircraftID <- 'SWA1897'
#meanCourse <- 3.14
#sampleSize <- 10
#courseVector <- meanCourse + 0.1*matrix(rnorm(sampleSize*1), sampleSize, 1)

#Monte-Carlo Simulation setup for perturbing geo coordinates (latitude and longitude)
#Please enter target aircraft callsign here. SWA1897 is an example.
#aircraftID <- 'SWA1897'
#meanRocd <- 25
#sampleSize <- 10
#rocdVector <- meanRocd + matrix(rnorm(sampleSize*1), sampleSize, 1)

#Monte-Carlo Simulation setup for perturbing geo coordinates (latitude and longitude)
#Please enter target aircraft callsign here. SWA1897 is an example.
#aircraftID <- 'SWA1897'
#waypointIndex <- 8
#meanLatitude <- 34.422439
#meanLongitude <- -118.025853
#sampleSize <- 10
#latitudeVector <- meanLatitude + 0.1*matrix(rnorm(sampleSize*1), sampleSize, 1)
#longitudeVector <- meanLongitude + 0.1*matrix(rnorm(sampleSize*1), sampleSize, 1)

#Monte-Carlo Simulation setup that perturbs number of time steps for controller absence
#Please enter target aircraft callsign here. SWA1897 is an example.
#aircraftID <- 'SWA1897'
#meanTimeStep <- 6
#sampleSize <- 10
#timeStepVector <- meanTimeStep + matrix(rnorm(sampleSize*1), sampleSize, 1)

#Monte-Carlo Simulation setup for perturbing geo coordinates (latitude)
#Please enter target aircraft callsign here. SWA1897 is an example.
#aircraftID <- 'PLEASE_ENTER_AIRCRAFT_CALLSIGN_HERE'
#waypointIndex <- 8
#meanLatitude <- 34.422439
#sampleSize <- 10
#latitudeVector <- meanLatitude + 0.1*matrix(rnorm(sampleSize*1), sampleSize, 1)

#Monte-Carlo Simulation setup for perturbing geo coordinates (longitude)
#Please enter target aircraft callsign here. SWA1897 is an example.
#aircraftID <- 'PLEASE_ENTER_AIRCRAFT_CALLSIGN_HERE'
#waypointIndex <- 8
#meanLongitude <- -118.025853
#sampleSize <- 10
#longitudeVector <- meanLongitude + 0.1*matrix(rnorm(sampleSize*1), sampleSize, 1)


# Simulation begins
for (count in 1:sampleSize) {
	simulationInterface$clear_trajectory()
	environmentInterface$load_rap('share/tg/rap')
	aircraftInterface$load_aircraft('share/tg/trx/TRX_DEMO_SFO_PHX_GateToGate.trx', 'share/tg/trx/TRX_DEMO_SFO_PHX_mfl.trx')
	simulationInterface$setupSimulation(as.integer(12000), as.integer(30))
	simulationInterface$start(.jlong(1000))

	while (1) {
            serverStatus = simulationInterface$get_runtime_sim_status()
	    if (serverStatus != NATS_SIMULATION_STATUS_PAUSE) {
               Sys.sleep(1)
	    }
            else {
                break
            }
        }


        aircraft = aircraftInterface$select_aircraft(aircraftID)

	if ("AIRSPEED" %in% PERTURB_ATTRIBUTES) {
	    aircraft$setTas_knots(.jfloat(airspeedVector[[count]]))
	}

        if ("ALTITUDE" %in% PERTURB_ATTRIBUTES) {
            aircraft$setAltitude_ft(.jfloat(altitudeVector[[count]]))
	}
     

	controllerInterface$setControllerAbsence('SWA1897', as.integer(4))

	simulationInterface$resume()

        while (1) {
            serverStatus = simulationInterface$get_runtime_sim_status();
            if (serverStatus != NATS_SIMULATION_STATUS_ENDED) {
               Sys.sleep(1)
	    }
            else {
                break
            }
        }

	trajectoryFile = sprintf("R-%s-Monte-Carlo-Sim-Trajectory_%s.csv", aircraftID, toString(count))
        simulationInterface$write_trajectories(paste('share/mcSimulation/', trajectoryFile, sep = ""))

        while(1) {
            if (file.exists(paste('share/mcSimulation/', trajectoryFile, sep = "")))
                break
            else
                Sys.sleep(1)
	}
        aircraftInterface$release_aircraft()
        Sys.sleep(1.5)
        environmentInterface$release_rap()
        Sys.sleep(1.5)

}

# Read output CSV file and plot
processFile = function(filepath) {
  count = 0
  con = file(filepath, "r")
  while ( TRUE ) {
    line = readLines(con, n = 1)
    if (count > 10) {
    if ( length(line) == 0 ) {
      break
    }
    rowValue = strsplit(line, "\\,")

    time <- c(time, as.numeric(rowValue[[1]][1]))
    speed <- c(speed, as.numeric(rowValue[[1]][6]))
    altitude <- c(altitude, as.numeric(rowValue[[1]][4]))
    rocd <- c(rocd, rowValue[[1]][5])
    course <- c(course, rowValue[[1]][8])
    latitude <- c(latitude, as.numeric(rowValue[[1]][2]))
    longitude <- c(longitude, as.numeric(rowValue[[1]][3]))
    }
    count = count + 1
  }
  close(con)

  csvName = strsplit(filepath, "\\/")
  plot.default(latitude, longitude, type="l", main=csvName[[1]][length(csvName[[1]])], xlab="Latitude (Degrees)", ylab="Longitude (Degrees)")
  plot(time, altitude, type="l", main=csvName[[1]][length(csvName[[1]])], xlab="Time (Seconds)", ylab="Altitude (Feet)")
  plot(time, speed, type="l", main=csvName[[1]][length(csvName[[1]])], xlab="Time (Seconds)", ylab="Speed (Knots)")
  plot(time, rocd, type="l", main=csvName[[1]][length(csvName[[1]])], xlab="Time (Seconds)", ylab="Rate of Climb/Descent (Feet per Second)")
  plot(time, course, type="l", main=csvName[[1]][length(csvName[[1]])], xlab="Time (Seconds)", ylab="Course (Degrees)")
}

# Loop through all the files written during simulation for graph plotting
for (i in 1:sampleSize) {
  processFile(paste("share/mcSimulation/R-", aircraftID, "-Monte-Carlo-Sim-Trajectory_", i, ".csv", sep = ""))
}

natsStandalone$stop()
