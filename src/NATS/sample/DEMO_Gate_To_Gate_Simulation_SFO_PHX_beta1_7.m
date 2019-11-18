% NATS sample
%
% Optimal Synthesis Inc.
%
% Oliver Chen
% 10.01.2019
%
% Demo of gate-to-gate trajectory simulation.
%
% The aircraft starts from the origin gate, goes through departing taxi plan, takes off, goes through different flight phases to the destination airport, and finally reaches the destination gate.

% Run header module
run('NATS_MATLAB_Header.m');

natsStandalone = NATSStandalone.start();
if isempty(natsStandalone)
    printf('Can''t start NATS Standalone\n');
    return;
end

simulationInterface = natsStandalone.getSimulationInterface();

environmentInterface = natsStandalone.getEnvironmentInterface();

equipmentInterface = natsStandalone.getEquipmentInterface();
aircraftInterface = equipmentInterface.getAircraftInterface();

entityInterface = natsStandalone.getEntityInterface();
controllerInterface = entityInterface.getControllerInterface();
pilotInterface = entityInterface.getPilotInterface();

if not(isempty(simulationInterface))
    simulationInterface.clear_trajectory();
    
    environmentInterface.load_rap('share/tg/rap');
    
    aircraftInterface.load_aircraft('trxSwRI/TRX_DEMO_Combined_GateToGate.trx', 'trxSwRI/TRX_DEMO_Combined_Gate_to_Gate__mfl.trx');
    
    % Controller to set human error: delay time
    % controllerInterface.setDelayPeriod("SWA1897", AIRCRAFT_CLEARANCE_PUSHBACK, 7);
    % controllerInterface.setDelayPeriod("SWA1897", AIRCRAFT_CLEARANCE_TAKEOFF, 20);

    simulationInterface.setupSimulation(11000, 30);
    
    simulationInterface.start(600);

    while true
        runtime_sim_status = simulationInterface.get_runtime_sim_status();
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE)
            break;
        else
            pause(1);
        end
    end
    
    % pilotInterface.skipFlightPhase('SWA1897', 'FLIGHT_PHASE_CLIMB_TO_CRUISE_ALTITUDE');
    % pilotInterface.setActionRepeat('SWA1897', "VERTICAL_SPEED");
    % pilotInterface.setWrongAction('SWA1897', "AIRSPEED", "FLIGHT_LEVEL");
    % pilotInterface.setActionReversal('SWA1897', 'VERTICAL_SPEED');
    % pilotInterface.setPartialAction('SWA1897', 'COURSE', 200, 50);
    % pilotInterface.skipChangeAction('SWA1897', 'COURSE');
    %pilotInterface.setActionLag('SWA1897', 'COURSE', 10, 0.05, 60);

	simulationInterface.resume();

    % Use a while loop to constantly check simulation status.  When the simulation finishes, continue to output the trajectory data
    while true
        runtime_sim_status = simulationInterface.get_runtime_sim_status();
        if (runtime_sim_status == NATS_SIMULATION_STATUS_ENDED)
            break;
        else
            pause(1);
        end
    end

    % Format epoch time string
    millis = datestr(now, 'yyyymmdd HHMMSS');
    InputDate = datenum(millis, 'yyyymmdd HHMMSS');
    UnixOrigin = datenum('19700101 000000', 'yyyymmdd HHMMSS');
    EpochSecond = round((InputDate-UnixOrigin)*86400000);

	S = dbstack();
    cur_filename = char(S(1).file);
    strIndexArray = strfind(cur_filename, '.m');

    disp('Outputting trajectory data.  Please wait....');
    fileName = sprintf('%s_%s.csv', cur_filename(1: strIndexArray(1)-1), num2str(EpochSecond));
    % Output the trajectory result file
    simulationInterface.write_trajectories(fileName);
    
    aircraftInterface.release_aircraft();
    environmentInterface.release_rap();
end

% Stop NATS Standalone environment
natsStandalone.stop();
