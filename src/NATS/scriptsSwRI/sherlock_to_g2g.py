'''
            NATIONAL AIRSPACE TRAJECTORY-PREDICTION SYSTEM (NATS)
          Copyright 2018 by Optimal Synthesis Inc. All rights reserved
          
Author: Hari Iyer
Date: 08/03/2019
Update: 2019.06.20

Gate to Gate flight plan generation module. Please refer to documentation under NATS_Client/sample/GateToGateFpReadme.pdf for details.
'''

from NATS_Python_Header import *

import sys
sys.path.insert(0, '/home/edecarlo/dev/nasa-uli/src/')
from PARA_ATM import *
from PARA_ATM.Commands.Helpers import DataStore
from sys import argv
from trx_tools import write_base_trx

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
airportInterface = environmentInterface.getAirportInterface()
terminalAreaInterface = environmentInterface.getTerminalAreaInterface()
weatherInterface = environmentInterface.getWeatherInterface()

equipmentInterface = natsStandalone.getEquipmentInterface()
aircraftInterface = equipmentInterface.getAircraftInterface()

safetyMetricsInterface = natsStandalone.getSafetyMetricsInterface()

# Load environment data
environmentInterface.load_rap("share/tg/rap")

# Get DataStore to paraatm database
db_access = DataStore.Access()
db_access.cursor.execute('SELECT * FROM cs_aal343 LIMIT 0;')
col_names = [desc[0] for desc in db_access.cursor.description]
db_access.cursor.execute("SELECT * FROM cs_aal343;")
results = pd.DataFrame(db_access.cursor.fetchall(),columns=col_names)
results.sort_values(by='time',inplace=True)
results.dropna(axis=0,subset=['rocd','tas'],how='all',inplace=True)

fname = 'trxSwRI/cs_aal343'
write_base_trx(results.iloc[0,:],fname)

#To do: get cs_aal343 and write initial .trx and .mfl files in share/tg/trx, then load them into the aircraftInterface. We only care about the departure airport, the arrival airport can be PHX.

#fname = 'trxSwRI/TRX_DEMO_Combined_GateToGate'
# #Custom TRX can be set here
aircraftInterface.load_aircraft("{}.trx".format(fname), "{}_mfl.trx".format(fname))

# # Get callsigns of all flights in the TRX
callsignList = aircraftInterface.getAllAircraftId()
print('CALLSIGN LIST: ', callsignList)

for callsign in callsignList:
    departureAirport = airportInterface.getDepartureAirport(callsign)
    arrivalAirport = airportInterface.getArrivalAirport(callsign)
    flight = aircraftInterface.select_aircraft(callsign)

    print('departureAirport: ', departureAirport)
    print('arrivalAirport: ', arrivalAirport)

# # Iterate through flights to generate Gate to Gate flight plans and store them in the TRX file.
# for callsign in callsignList:
    
#     print("Augmented flight plan generation for aircraft: " + callsign)
#     print("-----------------------------------------------------------")
    
#     ### To do: Decide what happens for flights that have already departed.
#     flightTakenOff = 'no';
        
#     # Get flight instance for the callsign name
#     flight = aircraftInterface.select_aircraft(callsign)
    
#     # Get arrival and destination airports
#     departureAirport = airportInterface.getDepartureAirport(callsign)
#     arrivalAirport = airportInterface.getArrivalAirport(callsign)

#     # Get arrival and departure airport gates
#     departureGates = []
#     if (flightTakenOff == "no"):
#         departureGates = list(airportInterface.getAllGates(departureAirport))

#     arrivalGates = list(airportInterface.getAllGates(arrivalAirport))
    
#     # Get arrival and departure airport runways
#     departureRunways = {}
#     if (flightTakenOff == "no"):
#         departureRunways = {key.replace(" ", ""): value.replace(" ", "") for (key, value) in  airportInterface.getAllRunways(departureAirport)}
#     arrivalRunways =  {key.replace(" ", ""): value.replace(" ", "") for (key, value) in airportInterface.getAllRunways(arrivalAirport)}
    
#     selectedDepartureGate = ""
#     selectedDepartureRunway = ""

#     departureRunwayID = selectedDepartureRunway
#     arrivalRunwayID = selectedArrivalRunway
    
#     if selectedDepartureRunway:
#         selectedDepartureRunway = departureRunways[selectedDepartureRunway]
        
#     runwayEnds = airportInterface.getRunwayEnds(arrivalAirport, selectedArrivalRunway)
#     if not runwayEnds:
#         runwayEnds = airportInterface.getRunwayEnds(arrivalAirport, selectedArrivalRunway + " ")
#     selectedArrivalRunway = list(runwayEnds)[1]
    
    
#     departureTaxi = []
#     if (flightTakenOff == "no"):
#         departureTaxi = airportInterface.get_taxi_route_from_A_To_B(callsign, departureAirport, selectedDepartureGate, selectedDepartureRunway)

#     arrivalTaxi = airportInterface.get_taxi_route_from_A_To_B(callsign, arrivalAirport, selectedArrivalRunway, selectedArrivalGate)
    
#     sidProcedures = []
#     selectedSidProcedure = []
#     if (flightTakenOff == "no"):
        
#         # Get all SID procedures for departure airport
#         sidProcedures = terminalAreaInterface.getAllSids(departureAirport)
#         if not sidProcedures:
#             print(departureAirport + " has no SID procedures.\n")
#             selectedSidProcedure = ""
            
#         else:
#             while 1:
#                 selectedSidProcedure = raw_input("Please choose a SID procedure for departure from " + departureAirport + " among [" + ",".join(sidProcedures) + "]: ")
#                 if selectedSidProcedure not in sidProcedures:
#                     print("\nInvalid SID procedure selected, please try again.\n")
#                 else: 
#                     print("\n")
#                     break


#     # Get Enroute waypoints in flight plan
#     enrouteWaypoints = raw_input("Please enter enroute waypoints in flight plan separated by ',' (Eg. BOILE,LOSHN,BLH): ")
    
#     # Get all STAR procedures for arrival airport
#     starProcedures = terminalAreaInterface.getAllStars(arrivalAirport)
#     while 1:
#         selectedStarProcedure = raw_input("\nPlease choose a STAR procedure for arrival into " + arrivalAirport + " among [" + ",".join(starProcedures) + "]: ")
#         if selectedStarProcedure not in starProcedures:
#             print("\nInvalid STAR procedure selected, please try again.\n")
#         else: 
#             print("\n")
#             break

#     # Get all APPROACH procedures for arrival airport
#     approachProcedures = terminalAreaInterface.getAllApproaches(arrivalAirport)
#     while 1:
#         selectedApproachProcedure = raw_input("Please choose an Approach procedure for arrival into " + arrivalAirport + " among [" + ",".join(approachProcedures) + "]: ")
#         if selectedApproachProcedure not in approachProcedures:
#             print("\nInvalid Approach procedure selected, please try again.\n")
#         else: 
#             print("\n")
#             break

    
#     # Flight plan string generation
#     if (not departureTaxi and flightTakenOff == "no"):
#         print("No default departure taxi route available, please refer to functions getLayout_node_map(String airport_code) and getLayout_node_data(String airport_code) in API Documentation for airport ground nodes to build a taxi plan.\n")
#         departureTaxi = []
#     if (not arrivalTaxi):
#         print("No default arrival taxi route available, please refer to functions getLayout_node_map(String airport_code) and getLayout_node_data(String airport_code) in API Documentation for airport ground nodes to build a taxi plan.\n")
#         arrivalTaxi = []
    
#     if (flightTakenOff == "no") :
#         augmentedFlightPlan = departureAirport + ".<"
#     else :
#         augmentedFlightPlan = departureAirport + "./"
    
#     for airportGroundNode in departureTaxi:
#         augmentedFlightPlan = augmentedFlightPlan + "{\"id\": \"" + airportGroundNode + "\"}, "
        
#     if (len(departureTaxi) > 0 and selectedSidProcedure is not ""):
#         augmentedFlightPlan = augmentedFlightPlan[:-2]
#         augmentedFlightPlan += ">." + departureRunwayID + "." + selectedSidProcedure + "." + enrouteWaypoints.replace(",", "..") + "." + selectedStarProcedure + "." + selectedApproachProcedure + "." + arrivalRunwayID + ".<"
    
#     elif (len(departureTaxi) > 0 and selectedSidProcedure is ""):
#         augmentedFlightPlan = augmentedFlightPlan[:-2]
#         augmentedFlightPlan += ">." + departureRunwayID + "." + enrouteWaypoints.replace(",", "..") + "." + selectedStarProcedure + "." + selectedApproachProcedure + "." + arrivalRunwayID + ".<"
#     else:
#         augmentedFlightPlan += "." + enrouteWaypoints.replace(",", "..") + "." + selectedStarProcedure + "." + selectedApproachProcedure + "." + arrivalRunwayID + ".<"

#     for airportGroundNode in arrivalTaxi:
#         augmentedFlightPlan = augmentedFlightPlan + "{\"id\": \"" + airportGroundNode + "\"}, "
    
#     if(len(arrivalTaxi) > 0):
#         augmentedFlightPlan = augmentedFlightPlan[:-2]
#     augmentedFlightPlan += ">." + arrivalAirport
    
#     print("The augmented flight plan for flight " + callsign + " is as follows. FP_ROUTE value in the original TRX can be replaced by this flight plan.")
#     print(augmentedFlightPlan)
#     print("\n\n")
        
# aircraftInterface.release_aircraft()
environmentInterface.release_rap()

# Stop NATS Standalone environment
natsStandalone.stop()

shutdownJVM()
