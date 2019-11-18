National Airspace Trajectory-Prediction System(NATS)

Version beta 1.7

Standalone (Desktop) NATS Program Module

This program module is responsible for all the computations related to the aircraft trajectory propagation and data manipulation.  This module runs on local machine only.


Contents of the zip file NATS-Standalone.zip
============================================
<dependency_library>    Dir    Dependency library
<dist>                  Dir    NATS binary files
<lib_precomp>           Dir    Precompiled dependency library.  You can use them if you are experiencing difficulties during compilation.
<log>                   Dir    Log file directory
<sample>                Dir    Sample files
<share>                 Dir    Background data
<utility>               Dir    Utility program
README.txt
README_Utility.txt
run
TestRun.sh
What_is_New.txt


Hardware Requirements
=====================
1. Intel/AMD 64bit CPU 1Ghz and up
2. RAM capacity at least 1GB
   Strategic weather avoidance places high demand on memory.  We suggest at least 12GB RAM for better system performance. 


Operating System/Software Environment Requirements
=================================================
1. Linux 64bit
   This software has been tested on:
   # Ubuntu v12.04, v16.04 with gcc 5.5
   # CentOS 6.9 with gcc 4.4
   # CentOS 7 with gcc 4.8
2. Java 1.7 and later
3. Python 2.7
4. Linux dependency library
   4.1 libcurl4-gnutls-dev
   4.2 libicu
   4.3 libxml2-dev
5. Jpype(For Python codes)
   Tested on v0.6.3
   
   Please do not use newer version of Jpype.  Current version of NATS is developed in Java 1.7 and it only works with Jpype 0.6.3.
   
   To install Jpype 0.6.3
   Go to https://github.com/originell/jpype
   Download jpype-0.6.3.tar.gz
   Unzip it, enter the directory and execute commands.
       sudo python setup.py install
6. MATLAB(if applicable)
   Tested on MATLAB R2014b, R2015b, R2019a
7. R
   Tested on version 3.4


Configuration
=============
1. Set system environment variable NATS_HOME with correct absolute path on your machine.

2. Change file permission to executable mode.
   chmod +x ./run
   chmod +x ./TestRun.sh
   chmod +x utility/run_nodejs.sh
   chmod +x utility/node-v8.11.1-linux-x64/bin/node
   chmod +x utility/stopStandalone.sh
3. Execute the testing script in command-line terminal.  Example: ./TestRun.sh
   (It is suggested that you call the run script from the current directory path.)


Test Run
========
NATS_Standalone/TestRun.sh is a a simple testing program to ensure NATS is starting and stopping well.
Two steps to use TestRun program are:
1. Change permission of TestRun.sh file
       chmod +x TestRun.sh
2. Execute TestRun program
       ./TestRun.sh
You should be able to see NATS Standalone running, loading databases and stopping.  It shows that your installation is in good shape.

Using NATS Pre-compiled Dependency Libraries(Optional. Only do this if NATS Standalone is not running.)
============================================
Notice: Users do not have to do this unless NATS is unable to run on the built-in libraries which came with the distribution.

There are several pre-compiled dependency library zip files in the NATS_Standalone/lib_precomp directory.
Users can use them for running NATS Standalone if they encounter any obstacles while building dependency libraries on Linux systems.

Example
We can use NATS pre-compiled hdf5 library.
# In NATS_Standalone/lib_precomp directory, unzip hdf5.zip
# Edit NATS_Standalone/run file
# Append hdf5 pre-compiled lib folder to LD_LIBRARY_PATH environment variable.
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$NATS_HOME/dist:$NATS_HOME/lib_precomp/Ubuntu_16.04/hdf5/lib

Troubleshooting
===============
1. libstdc++.so.6: version `GLIBCXX_3.4.22' not found
   This means that NATS is unable to find libstdc++.so.6 file during runtime.  This may happen when you run your program(Python, MATLAB, ... etc) or TestRun.sh
   Solution. Find the location of libstdc++.so.6
             In Terminal console window
                 sudo find /usr/ -name libstdc++.so.6
             You will see libstdc++.so.6 existing in some folders.
             We suggest to pick the file which is located in /usr/lib64.  Write down the actual path on your computer.
             Then we can add it to the Linux environment variable so the library file can be found.
             In Terminal console window
                 export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64

