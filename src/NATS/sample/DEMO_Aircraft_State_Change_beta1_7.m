% NATS sample
%
% Optimal Synthesis Inc.
%
% Oliver Chen
% 10.01.2019
%
% Demo of changing aircraft state
%
% This program starts the simulation for a period of time then NATS pause automatically.
% When the simulation is at pause status, we change the aircraft state.
% When the simulation resumes, it continues to run the rest of the simulation until it finishes.
%
% Users can compare the trajectory data to see the change of aircraft state.

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
    
    aircraftInterface.load_aircraft('share/tg/trx/TRX_DEMO_SFO_PHX_GateToGate.trx', 'share/tg/trx/TRX_DEMO_SFO_PHX_mfl.trx');

    simulationInterface.setupSimulation(11000, 30);
    
    simulationInterface.start(1020);

    % Check simulation status.  Continue to next code when it is at PAUSE status
    while true
        runtime_sim_status = simulationInterface.get_runtime_sim_status();
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE)
            break;
        else
            pause(1);
        end
    end
    
    curAircraft = aircraftInterface.select_aircraft('SWA1897');
    if ~isempty(curAircraft)
        % Set new state value
        % curAircraft.setCruise_tas_knots(450);
        % curAircraft.setCruise_alt(35000);
    
        curAircraft.setLatitude_deg(36.0);
        curAircraft.setLongitude_deg(-120.0);
    end

	simulationInterface.resume(7110);

    while true
        runtime_sim_status = simulationInterface.get_runtime_sim_status();
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE)
            break;
        else
            pause(1);
        end
    end
    
    curAircraft = aircraftInterface.select_aircraft('SWA1897');
    if ~isempty(curAircraft)
        % Set new state value
        % curAircraft.setCruise_tas_knots(450);
        % curAircraft.setCruise_alt(35000);
    
        curAircraft.setLatitude_deg(36.0);
        curAircraft.setLongitude_deg(-120.0);
        curAircraft.setAltitude_ft(32000.0);
        curAircraft.setTas_knots(400.0);
        curAircraft.setCourse_rad(110.0 * pi / 180);
        curAircraft.setRocd_fps(35.0);
    end
    
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