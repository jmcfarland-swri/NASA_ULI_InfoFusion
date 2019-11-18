% NATS sample
%
% Optimal Synthesis Inc.
%
% Oliver Chen
% 10.01.2019
%
% Samples of airport-related functions

% Run header module
run('NATS_MATLAB_Header.m');

natsStandalone = NATSStandalone.start();
if isempty(natsStandalone)
    printf('Can''t start NATS Standalone\n');
    return;
end

simulationInterface = natsStandalone.getSimulationInterface();

environmentInterface = natsStandalone.getEnvironmentInterface();
airportInterface = environmentInterface.getAirportInterface();
terminalAreaInterface = environmentInterface.getTerminalAreaInterface();

equipmentInterface = natsStandalone.getEquipmentInterface();
aircraftInterface = equipmentInterface.getAircraftInterface();

entityInterface = natsStandalone.getEntityInterface();
controllerInterface = entityInterface.getControllerInterface();
pilotInterface = entityInterface.getPilotInterface();

if not(isempty(simulationInterface))
    simulationInterface.clear_trajectory();
    
    environmentInterface.load_rap('share/tg/rap');
    
    aircraftInterface.load_aircraft('share/tg/trx/TRX_DEMO_SFO_PHX_GateToGate.trx', 'share/tg/trx/TRX_DEMO_SFO_PHX_mfl.trx');

    airportName = airportInterface.getFullName('KSFO');
    fprintf('KSFO airport full name = %s\n', char(airportName));

    disp('************************************************');

    runways = airportInterface.getAllRunways('KSFO');
    if ~isempty(runways)
        for j = 1 : size(runways)
            fprintf('KSFO --> Runway = %s, waypoing id = %s\n', runways(j, 1), runways(j, 2));
        end
    else
        disp('No runway data');
    end

    disp('************************************************');

    % Get all SID procedures of the airport
    allSids = terminalAreaInterface.getAllSids('KSFO');
    if ~isempty(allSids)
        for idx_proc = 1 : size(allSids)
            curProc = char(allSids(idx_proc, 1));
            % Get procedure leg names
            arrayLegNames = terminalAreaInterface.getProcedure_leg_names('SID', curProc, 'KSFO');
            if ~isempty(arrayLegNames)
                for idx_leg = 1 : size(arrayLegNames)
                    curLegName = char(arrayLegNames(idx_leg, 1));
                    % Get waypoints of the leg
                    arrayWaypoints = terminalAreaInterface.getWaypoints_in_procedure_leg('SID', curProc, 'KSFO', curLegName);
                    if ~isempty(arrayWaypoints)
                        for idx_wp = 1 : size(arrayWaypoints)
                            curWaypoint = char(arrayWaypoints(idx_wp, 1));
                            fprintf('KSFO --> SID: %s, leg = %s, waypoint = %s\n', curProc, curLegName, curWaypoint);
                        end
                    end
                end
            end
        end
    end
    
    disp('************************************************');
    
    % Get all STAR procedures of the airport
    allStars = terminalAreaInterface.getAllStars('KSFO');
    if ~isempty(allStars)
        for idx_proc = 1 : size(allStars)
            curProc = char(allStars(idx_proc, 1));
            % Get procedure leg names
            arrayLegNames = terminalAreaInterface.getProcedure_leg_names('STAR', curProc, 'KSFO');
            if ~isempty(arrayLegNames)
                for idx_leg = 1 : size(arrayLegNames)
                    curLegName = char(arrayLegNames(idx_leg, 1));
                    % Get waypoints of the leg
                    arrayWaypoints = terminalAreaInterface.getWaypoints_in_procedure_leg('STAR', curProc, 'KSFO', curLegName);
                    if ~isempty(arrayWaypoints)
                        for idx_wp = 1 : size(arrayWaypoints)
                            curWaypoint = char(arrayWaypoints(idx_wp, 1));
                            fprintf('KSFO --> STAR: %s, leg = %s, waypoint = %s\n', curProc, curLegName, curWaypoint);
                        end
                    end
                end
            end
        end
    end
    
    disp('************************************************');
    
    % Get all APPROACH procedures of the airport
    allApproaches = terminalAreaInterface.getAllApproaches('KSFO');
    if ~isempty(allApproaches)
        for idx_proc = 1 : size(allApproaches)
            curProc = char(allApproaches(idx_proc, 1));
            % Get procedure leg names
            arrayLegNames = terminalAreaInterface.getProcedure_leg_names('APPROACH', curProc, 'KSFO');
            if ~isempty(arrayLegNames)
                for idx_leg = 1 : size(arrayLegNames)
                    curLegName = char(arrayLegNames(idx_leg, 1));
                    % Get waypoints of the leg
                    arrayWaypoints = terminalAreaInterface.getWaypoints_in_procedure_leg('APPROACH', curProc, 'KSFO', curLegName);
                    if ~isempty(arrayWaypoints)
                        for idx_wp = 1 : size(arrayWaypoints)
                            curWaypoint = char(arrayWaypoints(idx_wp, 1));
                            fprintf('KSFO --> APPROACH: %s, leg = %s, waypoint = %s\n', curProc, curLegName, curWaypoint);
                        end
                    end
                end
            end
        end
    end
    
    disp('************************************************');
    
    departureRunway = airportInterface.getDepartureRunway('SWA1897');
    fprintf('SWA1897 departureRunway = %s\n', char(departureRunway));
 
    arrivalRunway = airportInterface.getArrivalRunway('SWA1897');
    fprintf('SWA1897 arrivalRunway = %s\n', char(arrivalRunway));

    disp('************************************************');
    
    % Calculate a route from point A to B
    % The resulted route is not loaded in NATS.  It only outputs the array of waypoint ids.
    design_taxi_plan_KSFO = airportInterface.get_taxi_route_from_A_To_B('SWA1897', 'KSFO', 'Gate_F_086', 'Rwy_02_002');
    if ~isempty(design_taxi_plan_KSFO)
        for i = 1 : size(design_taxi_plan_KSFO)
            fprintf('design_taxi_plan_KSFO waypoint id = %s\n', char(design_taxi_plan_KSFO(i, 1)));
        end
    end
    
    disp('************************************************');

    % Calculate a route from point A to B
    % The resulted route is not loaded in NATS.  It only outputs the array of waypoint ids.
    design_taxi_plan_KPHX = airportInterface.get_taxi_route_from_A_To_B('SWA1897', 'KPHX', 'Rwy_03_009', 'Gate_04_C16');
    if ~isempty(design_taxi_plan_KSFO)
        for i = 1 : size(design_taxi_plan_KPHX)
            fprintf('design_taxi_plan_KPHX waypoint id = %s\n', char(design_taxi_plan_KPHX(i, 1)));
        end
    end

    disp('************************************************');
    
    % Show airport layout node data
    array_node_data = airportInterface.getLayout_node_data('KABQ');
    if ~isempty(array_node_data)
        for i = 1 : size(array_node_data)
            fprintf('KABQ node data = %d, %f, %f, %s, %s, %s, %s\n', array_node_data(i, 1), array_node_data(i, 2), array_node_data(i, 3), array_node_data(i, 4), array_node_data(i, 5), array_node_data(i, 6), array_node_data(i, 7));
        end
    end
    
    aircraftInterface.release_aircraft();
    environmentInterface.release_rap();
end


% Stop NATS Standalone environment
natsStandalone.stop();
