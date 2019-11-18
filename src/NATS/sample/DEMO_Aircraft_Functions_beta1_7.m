% NATS sample
%
% Optimal Synthesis Inc.
%
% Oliver Chen
% 09.16.2019
%
% Demo of aircraft-related functions.
%
% Users can learn how to obtain aircraft instance, show related aircraft information, start/pause/resume simulation and output result trajectory file.

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

% entityInterface = natsStandalone.getEntityInterface();
% controllerInterface = entityInterface.getControllerInterface();
% pilotInterface = entityInterface.getPilotInterface();

if not(isempty(simulationInterface))
    simulationInterface.clear_trajectory();

    environmentInterface.load_rap('share/tg/rap');
    
    aircraftInterface.load_aircraft('share/tg/trx/TRX_DEMO_100rec_beta1.5.trx', 'share/tg/trx/TRX_DEMO_100rec_mfl_beta1.5.trx');
    
    aircraftIdArray_withinZone = aircraftInterface.getAircraftIds(30.0, 35.0, -115.0, -90.0, -1.0, -1.0);
    if ((~isempty(aircraftIdArray_withinZone)) & (size(aircraftIdArray_withinZone) > 0))
        for i = 1: size(aircraftIdArray_withinZone)
            curAcId = aircraftIdArray_withinZone(i);

            fprintf('Aircraft id in selected zone = %s, time = %ld\n', char(curAcId), round(tic * 1000));
        end
    end
    
    disp('****************************************');

    curAircraft = aircraftInterface.select_aircraft('ULI-3AFSD3DC24');
    if ~isempty(curAircraft)
        airborne_flight_plan_waypoint_name_array = curAircraft.getFlight_plan_waypoint_name_array();

        for i = 1: (size(airborne_flight_plan_waypoint_name_array))
            fprintf('ULI-3AFSD3DC24 airborne flight plan waypoint name = %s\n', char(airborne_flight_plan_waypoint_name_array(i, 1)));
        end
    else
        fprintf('Aircraft ULI-3AFSD3DC24 not found');
    end
    
    aircraft_3E6A0495F1 = aircraftInterface.select_aircraft('ULI-3E6A0495F1');
    aircraft_3E6A0495F1.delay_departure(100); % Delay the departure time for 100 sec

    simulationInterface.setupSimulation(10000, 10);

    simulationInterface.start(1000);

    while true
        runtime_sim_status = simulationInterface.get_runtime_sim_status();
        if (runtime_sim_status == NATS_SIMULATION_STATUS_PAUSE)
            break;
        else
            pause(1);
        end
    end
    
    aircraft_3E6A0495F1 = aircraftInterface.select_aircraft('ULI-3E6A0495F1');
    if not(isempty(aircraft_3E6A0495F1))
        disp('****************************************');
        fprintf('ULI-3E6A0495F1 (pausing at %f', simulationInterface.get_curr_sim_time());
        fprintf(' sec, latitude = %f', aircraft_3E6A0495F1.getLatitude_deg());
        fprintf(', longitude = %f', aircraft_3E6A0495F1.getLongitude_deg());
        fprintf(', altitude = %f\n', aircraft_3E6A0495F1.getAltitude_ft());
        disp('****************************************');
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
