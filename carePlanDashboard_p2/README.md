Care Plan Dashboard
=========

### Creates a Care Plan Dashboard given a folder of patient files.
##### Alyssa Freeman (alyssafreeman@kensatek.com)

### Quick Start

1. Download the application for your platform.
2. Launch the application (no need to install anything).

To create the Care Plan Dashboard:
1. Select the Browse button to select a Source Directory (folder containing the patient '.xlsm' files)
2. Select the Browse button to select an Output Direcotry (folder the dashboard excel file will be created in)
3. Type in a Dashboard File name (no need to include .xlsx)
4. Type in the Start and End Date of the time period you want to analyze
5. Select Create Dashboard button to run the program

To create the Results Base Incentive Program Dashboard:
1. Select the Browse button to select a Source Directory (folder containing the patient '.xlsm' files)
2. Select the Browse button to select an Output Direcotry (folder the dashboard excel file will be created in)
3. Type in an Incentive Dashboard File name (no need to include .xlsx)
4. Type in the Start and End Date of the time period you want to analyze
5. Select Create Incentive Based Dashboard button to run the program

### Running From Source (development purposes only)

Install the following:

* Python 2.7.10
* Clone the repo and run `python2 dashboard.py`.

Detailed instructions are on the [building page](https://cryptully.readthedocs.org/en/latest/building.html) of the documentation.

### Building the app (development purposes only)

CarePlanDasboard builds and runs on Linux, Windows, and OS X.

create spec file:
pyinstaller --windowed --onefile dashboard.py

clean project:  
rm -rf build dist

build:
pyinstaller --windowed --clean --onefile dashboard.spec


### TODO

* Add error logging

### License

Copyright (C) 2015 Alyssa Freeman