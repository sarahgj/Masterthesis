% Reads input data from a xlsx file in form of dates, times, lat, lon and
% emission fluxes. 
% Write release files to be used for FLEXPART
% Check if its over ground or over sea level
% Got it from Alina Fiehn
clear all;
close all;
clc
%run = 5;

%Choose halocarbon
type = 'methyliodide';
%type = 'dibromomethane';
%type = 'bromoform';

%Setting end date
if strcmp(type, 'methyliodide')
    %end_simulation_date = '20130103 000000';
    simulation_days = 10;
    %Set number of simulation
    simulation = 'F10';
elseif strcmp(type, 'bromoform')
    %end_simulation_date = '20130123 000000';
    simulation_days = 92;
    %Set number of simulation
    simulation = 'F92';
elseif strcmp(type, 'dibromomethane')
    %end_simulation_date = '20131031 000000';
    simulation_days = 437; %Til 31 desember 2016
    %Set number of simulation
    simulation = 'F437';
end

%% read variables from file
infile = xlsread('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/ASTRA_fluxes_for_MATLAB');

%reading the fluxes and setting the right molare masse
if strcmp(type, 'methyliodide')
    emissions = infile(:,1); % [pmol/(m²*hr)]
    molm = 0.14194;           % Molare Masse [kg/mol]
elseif strcmp(type, 'dibromomethane')
    emissions = infile(:,2); % [pmol/(m²*hr)]
    molm = 0.17383;           % Molare Masse [kg/mol]    
elseif strcmp(type, 'bromoform')
    emissions = infile(:,3); % [pmol/(m²*hr)]
    molm = 0.25273;           % Molare Masse [kg/mol] 
else
    fprintf('Choose type of halocarbon on line 12-14')
end

%Molar masses from Alina
%molm = 0.2527;   % Molare Masse Bromoform
%molm = 0.14195;  % Molare Masse Methyliodide
%molm  = 0.06214; % Molare Masse DMS [kg/mol]

 
%% SKIP NaNs
ind=find(~isnan(emissions)); % indices of fluxes
len = length(ind);
flux = emissions(ind);   % [pmol/(m²*hr)]

day = infile(ind,4);
hour = infile(ind,5);
lat = infile(ind,6);
lon = infile(ind,7);


%% producing two strings with the date and time window for the release
measuredates = datenum(2015, 10, day, hour, 0, 0);
startdates   = measuredates - 1./48.; %halfanhour
enddates     = measuredates + 1./48.; %halfanhour
end_simulation_dates = measuredates + simulation_days;
measuredates_string = datestr(measuredates,30);
startstring  = datestr(startdates,30);
endstring    = datestr(enddates,30);
end_simulation_string = datestr(end_simulation_dates,30);


% correcting lon for positive values to the West
% lon = -lon;

% producing lat and lon windows for the release
lat1 = lat - 0.0001;
lat2 = lat + 0.0001;
lon1 = lon - 0.0001;
lon2 = lon + 0.0001;


%% print fluxes and measuredates to files
if strcmp(type, 'methyliodide')
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Fluxes/fluxes_Methyliodide_ASTRA_F10.dat',flux, '\t') 
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Fluxes/all_dates_Methyliodide_ASTRA_F10.dat',measuredates_string, '') 
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Fluxes/all_lats_Methyliodide_ASTRA_F10.dat',lat, '\t')
elseif strcmp(type, 'dibromomethane')
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Fluxes/fluxes_Dibromomethane_ASTRA_F437.dat',flux, '\t') 
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Fluxes/all_dates_Dibromomethane_ASTRA_F437.dat',measuredates_string, '')
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Fluxes/all_lats_Dibromomethane_ASTRA_F437.dat',lat, '\t') 
elseif strcmp(type, 'bromoform')
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Fluxes/fluxes_Bromoform_ASTRA_F92.dat',flux, '\t') 
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Fluxes/all_dates_Bromoform_ASTRA_F92.dat',measuredates_string, '') 
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Fluxes/all_lats_Bromoform_ASTRA_F92.dat',lat, '\t')
end

%figure(1)
%plot(measuredates, flux)
%datetick('x','keepticks','keeplimits');
%title(['ASTRA: ', type]);
%xlabel('Date');
%ylabel('Flux');
%saveas(figure(1), ['/uio/hume/student-u17/sarahgj/Master/Figures/VSLS/Fluxes/ASTRA_', type],'eps')


%% Calculating emitted masses M

%constants to be used
pico = 1e-12;
micro = 1e-6;
dlat = 22.18; %distance for 0.0002 degrees in latitude [m]
Na = 6.0221415e23; %Avogadros constant, number of particles in one mol 

area = NaN(len,1);
particles = NaN(len,1);
partrelease = NaN(len,1);
mass = NaN(len,1);
for i = 1:len
    cp = cos(lat(i)*3.1415926/180.);
    sp = sin(lat(i)*3.1415926/180.);
    a = 6378137.0; %equatorial earth radii
    b = 6356752.3; %polar earth radii
    % dlondeg is the distance for 1 degree in longitude [m]
    % dlon is the distance for 0.0002 degrees in longitude [m]
    dlondeg = 3.1415926/180. * cp * sqrt( (a^4 * cp^2 + b^4 * sp^2) / ((a*cp)^2 + (b*sp)^2) );
    dlon = dlondeg*2./10000.;
    area(i) = dlat * dlon; % release windows: 0.0002 lat * 0.0002 lon [m2]
    % at entspricht der Anzahl von Teilchen emittiert über der Fläche A in einer Stunde als Funktion des Flusses F
    %particles(i) = round(flux(i) * area(i) * pico * Na); %[particles/hr]*1hr = total number of particles released
    %partrelease(i) = round(particles(i)*1e-13); % why *1e-13?
    %if (partrelease(i) < 0) 
    %   partrelease(i) = 0;
    %end
    mass(i) = flux(i) * area(i) * pico * molm; % [kg/hr]*1hr = total mass released
        % partikelanzahl wird auf konstante Werte gesetzt
    partrelease(i) = 10000;
end

positive_index = find(mass>=0);
%open file to write released mass [micro mol] 
if strcmp(type, 'methyliodide')
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Released/released_Methyliodide_ASTRA_F10.dat',mass(positive_index), '\t') 
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Released/dates_Methyliodide_ASTRA_F10.dat',measuredates_string(positive_index,:), '') 
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Released/lats_Methyliodide_ASTRA_F10.dat',lat(positive_index), '\t') 
elseif strcmp(type, 'dibromomethane')
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Released/released_Dibromomethane_ASTRA_F437.dat',mass(positive_index), '\t') 
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Released/dates_Dibromomethane_ASTRA_F437.dat',measuredates_string(positive_index,:), '') 
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Released/lats_Dibromomethane_ASTRA_F437.dat',lat(positive_index), '\t')
elseif strcmp(type, 'bromoform')
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Released/released_Bromoform_ASTRA_F92.dat',mass(positive_index), '\t') 
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Released/dates_Bromoform_ASTRA_F92.dat',measuredates_string(positive_index,:), '') 
   dlmwrite('/uio/hume/student-u17/sarahgj/Master/Data/VSLS_measurements/Released/lats_Bromoform_ASTRA_F92.dat',lat(positive_index), '\t') 
end

%% Writing RELEASE files
j = 0;
for i = 1:len
    if (mass(i) > 0)     
        j = j+1;    
        istr = int2str(j); 
        
        %open file to write
        if strcmp(type, 'methyliodide')
           fid = fopen(['/uio/hume/student-u17/sarahgj/Master/Data/Flexpart_files/ASTRA/Methyliodide/RELEASES-' istr], 'wt');
        elseif strcmp(type, 'dibromomethane')
           fid = fopen(['/uio/hume/student-u17/sarahgj/Master/Data/Flexpart_files/ASTRA/Dibromomethane/RELEASES-' istr], 'wt');
        elseif strcmp(type, 'bromoform')
           fid = fopen(['/uio/hume/student-u17/sarahgj/Master/Data/Flexpart_files/ASTRA/Bromoform/RELEASES-' istr], 'wt');
        else
            fprintf('Thats wierd :O')
        end
        
        %WRITE RELEASES
        fprintf(fid, '*************************************************************************\n');
        fprintf(fid, '*                                                                       *\n');
        fprintf(fid, '*                                                                       *\n');
        fprintf(fid, '*                                                                       *\n');
        fprintf(fid, '*   Input file for the Lagrangian particle dispersion model FLEXPART    *\n');
        fprintf(fid, '*                        Please select your options                     *\n');
        fprintf(fid, '*                                                                       *\n');
        fprintf(fid, '*                                                                       *\n');
        fprintf(fid, '*                                                                       *\n');
        fprintf(fid, '*************************************************************************\n');
        fprintf(fid, '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n');
        fprintf(fid, '  1                                                                      \n');      
        fprintf(fid, '___                        i3    Total number of species emitted        \n'); 
        fprintf(fid, '                                                                         \n');
        if strcmp(type, 'methyliodide')
            fprintf(fid, '  7                                                                      \n');      
        elseif strcmp(type, 'dibromomethane')
            fprintf(fid, '  1                                                                      \n');      
        elseif strcmp(type, 'bromoform')
            fprintf(fid, '  2                                                                      \n');      
        end    
        fprintf(fid, '___                        i3    Index of species in file SPECIES        \n'); 
        fprintf(fid, '                                                                         \n');
        fprintf(fid, '=========================================================================\n');
        fprintf(fid, '%s %s                  \n', startstring(i,1:8), startstring(i,10:15));
        fprintf(fid, '________ ______           i8,1x,i6 Beginning date and time of release \n');
        fprintf(fid, '                                                                         \n');  
        fprintf(fid, '%s %s                  \n', endstring(i,1:8), endstring(i,10:15));
        fprintf(fid, '________ ______           i8,1x,i6 Ending date and time of release    \n');
        fprintf(fid, '                                                                         \n'); 
        fprintf(fid, '%9.4f                       \n', lon1(i));
        fprintf(fid, '____.____                 f9.4  Longitude [DEG] of lower left corner     \n');
        fprintf(fid, '                                                                         \n');  
        fprintf(fid, '%9.4f                       \n', lat1(i));
        fprintf(fid, '____.____                 f9.4  Latitude [DEG] of lower left corner      \n');
        fprintf(fid, '                                                                         \n'); 
        fprintf(fid, '%9.4f                      \n', lon2(i));
        fprintf(fid, '____.____                 f9.4  Longitude [DEG] of lower left corner     \n');
        fprintf(fid, '                                                                         \n'); 
        fprintf(fid, '%9.4f                      \n', lat2(i));
        fprintf(fid, '____.____                 f9.4  Latitude [DEG] of upper right corner     \n');
        fprintf(fid, '                                                                         \n');       
        fprintf(fid, '        1                                                                \n');
        fprintf(fid, '_________                 i9    1 for m above ground, 2 for m above sea level  \n');
        fprintf(fid, '                                                                         \n');    
        fprintf(fid, '    0.000                                                                \n');
        fprintf(fid, '_____.___                 f10.3 Lower z-level (in m agl or m asl)        \n'); 
        fprintf(fid, '                                                                         \n');     
        fprintf(fid, '    0.000                                                                \n');
        fprintf(fid, '_____.___                 f10.3 Upper z-level (in m agl or m asl)        \n');
        fprintf(fid, '                                                                         \n'); 
        fprintf(fid, '%9i                        \n', partrelease(i));
        fprintf(fid, '_________                 i9    Total number of particles to be released \n');
        fprintf(fid, '                                                                         \n');
        fprintf(fid, '%9.4e                                        \n', mass(i));
        fprintf(fid, '_.____E__                e9.4  Total mass emitted                        \n');
        fprintf(fid, '                                                                         \n');
        %   fprintf(fid, '%9.4e                  e9.4  Total mass emitted                      \n', null);
        %   fprintf(fid, '                                                                         \n');
        %   fprintf(fid, '                                                                         \n'); 
        fprintf(fid, 'ASTRAcruice_05-21_Oct_V%2i                                                 \n', i);
        fprintf(fid, '____________________________________   character*40 comment              \n');
        fprintf(fid, '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n');  
        fprintf(fid, '\n');
        fclose(fid);
        
        %WRITE pathnames
        if strcmp(type, 'methyliodide')
            fid_1 = fopen(['/uio/hume/student-u17/sarahgj/Master/Data/Flexpart_files/ASTRA/Methyliodide/pathnames-' istr], 'wt');
            fprintf(fid_1, '/usit/abel/u1/sarahgj/Flexpart/Runs/ASTRA/Methyliodide_%s/options/options-%i/\n', simulation, j);        
            fprintf(fid_1, './outputs-%i/\n', j);        
            fprintf(fid_1, '\n');        
            fprintf(fid_1, '/usit/abel/u1/sarahgj/Flexpart/Runs/ASTRA/Methyliodide_%s/AVAILABLE\n', simulation);        
            fprintf(fid_1, '============================================\n'); 
            fprintf(fid_1, '\n');
            fclose(fid_1);
        
        elseif strcmp(type, 'dibromomethane')
            fid_1 = fopen(['/uio/hume/student-u17/sarahgj/Master/Data/Flexpart_files/ASTRA/Dibromomethane/pathnames-' istr], 'wt');
            fprintf(fid_1, '/usit/abel/u1/sarahgj/Flexpart/Runs/ASTRA/Dibromomethane_%s/options/options-%i/\n', simulation, j);        
            fprintf(fid_1, './outputs-%i/\n', j);        
            fprintf(fid_1, '\n');        
            fprintf(fid_1, '/usit/abel/u1/sarahgj/Flexpart/Runs/ASTRA/Dibromomethane_%s/AVAILABLE\n', simulation);        
            fprintf(fid_1, '============================================\n'); 
            fprintf(fid_1, '\n');
            fclose(fid_1);
        elseif strcmp(type, 'bromoform')
            fid_1 = fopen(['/uio/hume/student-u17/sarahgj/Master/Data/Flexpart_files/ASTRA/Bromoform/pathnames-' istr], 'wt');
            fprintf(fid_1, '/usit/abel/u1/sarahgj/Flexpart/Runs/ASTRA/Bromoform_%s/options/options-%i/\n', simulation, j);        
            fprintf(fid_1, './outputs-%i/\n', j);        
            fprintf(fid_1, '\n');        
            fprintf(fid_1, '/usit/abel/u1/sarahgj/Flexpart/Runs/ASTRA/Bromoform_%s/AVAILABLE\n', simulation);        
            fprintf(fid_1, '============================================\n'); 
            fprintf(fid_1, '\n');            
            fclose(fid_1);                                               
        else
            fprintf('Thats wierd :O')
        end
        
        %WRITE COMMAND
        if strcmp(type, 'methyliodide')
           fid_2 = fopen(['/uio/hume/student-u17/sarahgj/Master/Data/Flexpart_files/ASTRA/Methyliodide/COMMAND-' istr], 'wt');
        elseif strcmp(type, 'dibromomethane')
           fid_2 = fopen(['/uio/hume/student-u17/sarahgj/Master/Data/Flexpart_files/ASTRA/Dibromomethane/COMMAND-' istr], 'wt');
        elseif strcmp(type, 'bromoform')
           fid_2 = fopen(['/uio/hume/student-u17/sarahgj/Master/Data/Flexpart_files/ASTRA/Bromoform/COMMAND-' istr], 'wt');
        else
            fprintf('Thats wierd :O')
        end

        %write to files
        fprintf(fid_2, '********************************************************************************\n');
        fprintf(fid_2, '*                                                                              *\n');
        fprintf(fid_2, '*      Input file for the Lagrangian particle dispersion model FLEXPART        *\n');
        fprintf(fid_2, '*                           Please select your options                         *\n');
        fprintf(fid_2, '*                                                                              *\n');
        fprintf(fid_2, '********************************************************************************\n');
        fprintf(fid_2, '\n');
        fprintf(fid_2, '1               LDIRECT           1 FOR FORWARD SIMULATION, -1 FOR BACKWARD SIMULATION\n');      
        fprintf(fid_2, '%s %s YYYYMMDD HHMISS   BEGINNING DATE OF SIMULATION\n', startstring(i,1:8), startstring(i,10:15)); 
        fprintf(fid_2, '%s %s YYYYMMDD HHMISS   ENDING DATE OF SIMULATION\n', end_simulation_string(i,1:8), end_simulation_string(i,10:15)); 
        fprintf(fid_2, '10800           SSSSS             OUTPUT EVERY SSSSS SECONDS \n');
        if strcmp(type, 'methyliodide')
            fprintf(fid_2, '1800            SSSSS             TIME AVERAGE OF OUTPUT (IN SSSSS SECONDS) \n');
            fprintf(fid_2, '900             SSSSS             SAMPLING RATE OF OUTPUT (IN SSSSS SECONDS) \n');
            fprintf(fid_2, '999999999       SSSSSSS           TIME CONSTANT FOR PARTICLE SPLITTING (IN SECONDS) \n');
            fprintf(fid_2, '900             SSSSS             SYNCHRONISATION INTERVAL OF FLEXPART (IN SECONDS) \n');
        elseif strcmp(type, 'bromoform')
            fprintf(fid_2, '3600            SSSSS             TIME AVERAGE OF OUTPUT (IN SSSSS SECONDS) \n');
            fprintf(fid_2, '1800            SSSSS             SAMPLING RATE OF OUTPUT (IN SSSSS SECONDS) \n');
            fprintf(fid_2, '999999999       SSSSSSS           TIME CONSTANT FOR PARTICLE SPLITTING (IN SECONDS) \n');
            fprintf(fid_2, '1800            SSSSS             SYNCHRONISATION INTERVAL OF FLEXPART (IN SECONDS) \n');
        elseif strcmp(type, 'dibromomethane')
            fprintf(fid_2, '7200            SSSSS             TIME AVERAGE OF OUTPUT (IN SSSSS SECONDS) \n');
            fprintf(fid_2, '1800            SSSSS             SAMPLING RATE OF OUTPUT (IN SSSSS SECONDS) \n');
            fprintf(fid_2, '999999999       SSSSSSS           TIME CONSTANT FOR PARTICLE SPLITTING (IN SECONDS) \n');
            fprintf(fid_2, '1800            SSSSS             SYNCHRONISATION INTERVAL OF FLEXPART (IN SECONDS) \n');
        end  
        fprintf(fid_2, '-5.0            CTL               FACTOR, BY WHICH TIME STEP MUST BE SMALLER THAN TL \n');
        fprintf(fid_2, '4               IFINE             DECREASE OF TIME STEP FOR VERTICAL MOTION BY FACTOR IFINE \n');
        fprintf(fid_2, '1               IOUT              1 CONC. (RESID. TIME FOR BACKWARD RUNS) OUTPUT,2 MIX. RATIO OUTPUT,3 BOTH,4 PLUME TRAJECT.,5=1+4 \n');
        fprintf(fid_2, '1               IPOUT             PARTICLE DUMP: 0 NO, 1 EVERY OUTPUT INTERVAL, 2 ONLY AT END \n');
        fprintf(fid_2, '1               LSUBGRID          SUBGRID TERRAIN EFFECT PARAMETERIZATION: 1 YES, 0 NO \n');
        fprintf(fid_2, '1               LCONVECTION       CONVECTION: 1 YES, 0 NO \n');
        fprintf(fid_2, '0               LAGESPECTRA       AGE SPECTRA: 1 YES, 0 NO \n');
        fprintf(fid_2, '0               IPIN              CONTINUE SIMULATION WITH DUMPED PARTICLE DATA: 1 YES, 0 NO \n');
        fprintf(fid_2, '0               IOUTPUTFOREACHREL CREATE AN OUPUT FILE FOR EACH RELEASE LOCATION: 1 YES, 0 NO \n');
        fprintf(fid_2, '0               IFLUX             CALCULATE FLUXES: 1 YES, 0 NO \n');
        fprintf(fid_2, '0               MDOMAINFILL       DOMAIN-FILLING TRAJECTORY OPTION: 1 YES, 0 NO \n');
        fprintf(fid_2, '1               IND_SOURCE        1=MASS UNIT , 2=MASS MIXING RATIO UNIT \n');
        fprintf(fid_2, '1               IND_RECEPTOR      1=MASS UNIT , 2=MASS MIXING RATIO UNIT \n');
        fprintf(fid_2, '0               MQUASILAG         QUASILAGRANGIAN MODE TO TRACK INDIVIDUAL PARTICLES: 1 YES, 0 NO \n');
        fprintf(fid_2, '0               NESTED_OUTPUT     SHALL NESTED OUTPUT BE USED? YES, 0 NO \n');
        fprintf(fid_2, '2               LINIT_COND        INITIAL COND. FOR BW RUNS: 0=NO,1=MASS UNIT,2=MASS MIXING RATIO UNIT\n');
        fprintf(fid_2, '0               SURF_ONLY         IF THIS IS SET TO 1, OUTPUT IS WRITTEN ONLY OUT FOR LOWEST LAYER                                                                         \n');
        fclose(fid_2);        
    end
end



