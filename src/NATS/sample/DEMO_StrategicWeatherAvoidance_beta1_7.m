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
    
    % Set polygon file for Strategic Weather Avoidance
    % Detail path and filename are required if you would like to use a specific file.  Example: share/rg/polygons/YYYYMMDD_HHMMSS.dat
    %
    % If inputing '', NATS engine will look for the latest file with name format YYYYMMDD_HHMMSS.dat
    %
    % Notice!!!!
    % If Sigmet file is used, polygon file will be ignored
    controllerInterface.setWeather_polygonFile('share/rg/polygons/MACS_scenario.dat');
    %controllerInterface.setWeather_polygonFile('') % NATS automatically pick latest file
    %controllerInterface.setWeather_polygonFile('NONE') % Disable file
    
    % Set sigmet file for Strategic Weather Avoidance
    % Detail path and filename are required if you would like to use a specific file.  Example: share/rg/polygons/YYYYMMDD_HHMMSS.dat
    %
    % If inputing '', NATS engine will look for the latest file with name format YYYYMMDD_HHMMSS.sigmet
    %
    % Notice!!!!
    % If Sigmet file is used, polygon file will be ignored
    %controllerInterface.setWeather_sigmetFile('') % NATS automatically pick latest file
    %controllerInterface.setWeather_sigmetFile('NONE') % Disable file
    
    % Enable strategic weather avoidance capability
    % This function must be called before setting up simulation so NATS can load required database files.
    controllerInterface.enableStrategicWeatherAvoidance(true);
    
    simulationInterface.start();

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