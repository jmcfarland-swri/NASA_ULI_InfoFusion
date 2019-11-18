# NATS sample
#
# Optimal Synthesis Inc.
#
# Oliver Chen
# 10.03.2019
#
# Samples of airport-related functions

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

environmentInterface = natsStandalone.getEnvironmentInterface()
airportInterface = environmentInterface.getAirportInterface()
terminalAreaInterface = environmentInterface.getTerminalAreaInterface()

if simulationInterface is None:
    print "Can't get SimulationInterface"

else:
    simulationInterface.clear_trajectory()
    
    environmentInterface.load_rap("share/tg/rap")
    aircraftInterface.load_aircraft("share/tg/trx/TRX_DEMO_SFO_PHX_GateToGate.trx", "share/tg/trx/TRX_DEMO_SFO_PHX_mfl.trx")

    airportName = airportInterface.getFullName("KSFO")
    print "KSFO airport full name =", airportName

    print "************************************************"

    # Get all runways
    runways = airportInterface.getAllRunways("KSFO")
    if not(runways is None) :
        for j in range(0, len(runways)) :
            print "Runway in KSFO = ", runways[j][0], ", waypoing id = ", runways[j][1]
    else :
        print "No runway data"

    print "************************************************"
    
    # Get runway exits of the airport
    runwayExits = airportInterface.getRunwayExits("KABQ", "RW26")
    if not(runwayExits is None) :
        for j in range(0, len(runwayExits)) :
            print "Exit point on runway RW26 at airport KABQ = ", runwayExits[j]
    else :
        print "No runway exit data"
    
    print "************************************************"

    # Get all SID procedures of the airport
    allSids = terminalAreaInterface.getAllSids("KSFO")
    if not(allSids is None) :
        for curProc in allSids :
            # Get procedure leg names
            arrayLegNames = terminalAreaInterface.getProcedure_leg_names("SID", curProc, "KSFO")
            if not (arrayLegNames is None) :
                for curLegName in arrayLegNames :
                    # Get waypoints of the leg
                    arrayWaypoints = terminalAreaInterface.getWaypoints_in_procedure_leg("SID", curProc, "KSFO", curLegName)
                    if not (arrayWaypoints is None) :
                        for curWaypoint in arrayWaypoints :
                            print "KSFO --> SID:", curProc, ". leg = ", curLegName, ", wp = ", curWaypoint

    print "************************************************"
    
    # Get all STAR procedures of the airport
    allStars = terminalAreaInterface.getAllStars("KSFO")
    if not(allStars is None) :
        for curProc in allStars :
            # Get procedure leg names
            arrayLegNames = terminalAreaInterface.getProcedure_leg_names("STAR", curProc, "KSFO")
            if not (arrayLegNames is None) :
                for curLegName in arrayLegNames :
                    # Get waypoints of the leg
                    arrayWaypoints = terminalAreaInterface.getWaypoints_in_procedure_leg("STAR", curProc, "KSFO", curLegName)
                    if not (arrayWaypoints is None) :
                        for curWaypoint in arrayWaypoints :
                            print "KSFO --> STAR:", curProc, ". leg = ", curLegName, ", wp = ", curWaypoint
    
    print "************************************************"
    
    allApproaches = terminalAreaInterface.getAllApproaches("KSFO")
    if not(allApproaches is None) :
        for curProc in allApproaches :
            # Get procedure leg names
            arrayLegNames = terminalAreaInterface.getProcedure_leg_names("APPROACH", curProc, "KSFO")
            if not (arrayLegNames is None) :
                for curLegName in arrayLegNames :
                    # Get waypoints of the leg
                    arrayWaypoints = terminalAreaInterface.getWaypoints_in_procedure_leg("APPROACH", curProc, "KSFO", curLegName)
                    if not (arrayWaypoints is None) :
                        for curWaypoint in arrayWaypoints :
                            print "KSFO --> APPROACH:", curProc, ". leg = ", curLegName, ", wp = ", curWaypoint
    
    print "************************************************"
    
    departureRunway = airportInterface.getDepartureRunway("SWA1897")
    print "SWA1897 departureRunway = ", departureRunway
 
    arrivalRunway = airportInterface.getArrivalRunway("SWA1897")
    print "SWA1897 arrivalRunway = ", arrivalRunway

    print "************************************************"
    
    # Calculate a route from point A to B
    # The resulted route is not loaded in NATS.  It only outputs the array of waypoint ids.
    design_taxi_plan_KSFO = airportInterface.get_taxi_route_from_A_To_B("SWA1897", "KSFO", "Gate_F_086", "Rwy_02_002")
    if not(design_taxi_plan_KSFO is None) :
        for i in range(0, len(design_taxi_plan_KSFO)) :
            print "design_taxi_plan_KSFO waypoint id = ", design_taxi_plan_KSFO[i]

    print "************************************************"

    # Calculate a route from point A to B
    # The resulted route is not loaded in NATS.  It only outputs the array of waypoint ids.
    design_taxi_plan_KPHX = airportInterface.get_taxi_route_from_A_To_B("SWA1897", "KPHX", "Rwy_03_009", "Gate_04_C16") 
    if not(design_taxi_plan_KPHX is None) :
        for i in range(0, len(design_taxi_plan_KPHX)) :
            print "design_taxi_plan_KPHX waypoint id = ", design_taxi_plan_KPHX[i]

    print "************************************************"

    # Show airport layout node data
    array_node_data = airportInterface.getLayout_node_data("KABQ")
    if not(array_node_data is None) :
        for i in range(0, len(array_node_data)) :
            print "KABQ node data = ", array_node_data[i][0], ", ", array_node_data[i][2], ", ", array_node_data[i][3], ", ", array_node_data[i][4], ", ", array_node_data[i][5], ", ", array_node_data[i][6]

    aircraftInterface.release_aircraft()
    environmentInterface.release_rap()

# Stop NATS Standalone environment
natsStandalone.stop()

shutdownJVM()