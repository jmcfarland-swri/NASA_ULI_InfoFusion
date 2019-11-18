'''
NATS Interactive Client.

This program can be run using execfile() command in Python shell to start interactive NATS Session.

'''

from NATS_Python_Header import *

print('This module illustrates the interactive NATS operations in real time.')

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

environmentInterface = natsStandalone.getEnvironmentInterface()
airportInterface = environmentInterface.getAirportInterface()
terminalAreaInterface = environmentInterface.getTerminalAreaInterface()
terrainInterface = environmentInterface.getTerrainInterface()

entityInterface = natsStandalone.getEntityInterface()
controllerInterface = entityInterface.getControllerInterface()
pilotInterface = entityInterface.getPilotInterface()

print "Following NATS Interfaces have been initialized:\n\n"
print "simulationInterface"
print "equipmentInterface"
print "aircraftInterface"
print "groundVehicleInterface"
print "safetyMetricsInterface"
print "environmentInterface"
print "airportInterface"
print "entityInterface"
print "controllerInterface"
print "pilotInterface"
print "terrainInterface"
print "groundOperatorInterface\n\n"

print "These interfaces can be used to submit NATS commands.\n\nExample:\nlist(aircraftInterface.getAllAircraftId())\n"
