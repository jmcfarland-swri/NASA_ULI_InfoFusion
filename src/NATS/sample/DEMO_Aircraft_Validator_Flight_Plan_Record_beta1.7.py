# NATS sample
#
# Optimal Synthesis Inc.
#
# Oliver Chen
# 10.03.2019
#
# Demo of flight plan validator

from NATS_Python_Header import *

clsNATSStandalone = JClass('NATSStandalone')
# Start NATS Standalone environment
natsStandalone = clsNATSStandalone.start()

if (natsStandalone is None) :
    print "Can't start NATS Standalone"
    quit()
    
equipmentInterface = natsStandalone.getEquipmentInterface()
aircraftInterface = equipmentInterface.getAircraftInterface()


if aircraftInterface is None :
    print "Can't get AircraftInterface"
else :
    result = aircraftInterface.validate_flight_plan_record("TRACK SWA1897 B733 373628.6 1222248.0 0 0.13 280 ZOA ZOA46", "FP_ROUTE KSFO./.RW01R.SSTIK4.LOSHN..BOILE..BLH.HYDRR1.I07R.RW07R.<>.KPHX", 37000)
    print "Result of validation of flight plan = ", result

# Stop NATS Standalone environment
natsStandalone.stop()

shutdownJVM()