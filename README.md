# openCM2
This is the software part of the openCM2 project, the hardware part can be found under https://github.com/bjks/openCM2_hardware.

## Non-UC2 Dependencies 
- numpy
- pygame 

## Installation
If you are using the UC2 virtual environment, we recommend to do the installation in this environment as well.
The installation includes:
- connecting the controller to the Raspberry Pi
- install pygame
- install paho-mqtt

### Connecting the controller
```
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install libusb-dev

wget http://www.pabr.org/sixlinux/sixpair.c
gcc -o sixpair sixpair.c -lusb

reboot
```
Now, you need to plug you controller into the Raspberry Pi.
```
sudo ./sixpair
```
You need to unplug your controller and press the PS button to turn on the controller. Now we need to establish the bluetooth connection. Once you run `scan on` you should see your controller show up the device list. You need to take its MAC adress (which has the form `00:00:00:00:00`) and run the commands `pair`, `trust`, and `connect`.
```
sudo bluetoothctl
    power on
    default-agent
    scan on
    pair <controller adress, eg.00:00:00:00:00>
    trust <controller adress, eg.00:00:00:00:00>    
    connect <controller adress, eg.00:00:00:00:00>    
```
Now your controller is connected. You can find more information [here](https://approxeng.github.io/approxeng.input/api/dualshock3.html).

### Install pygame and paho-mqtt
To install pygame, we first install all dependencies:
```
sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev   libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev
```
and then we can install pygame by running
```
python -m pip install pygame
```
Lastly, we need to install paho-mqtt with
```
pip install paho-mqtt
```

## Usage
To run the script you need to run 
```
python controller2motor.py
```
The message in the terminal explains the botton settings. Once everything is setup a window will show up, as long as this window is you active window the program reacts to the controller input. To avoid that, bring the window of the program to the background. 