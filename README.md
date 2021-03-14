# openCM2

## Non-UC2 Dependencies 
- numpy
- pygame 

## Installation
Do everything below in UC2 env if you use that.

### for controller connection
```
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install libusb-dev

wget http://www.pabr.org/sixlinux/sixpair.c
gcc -o sixpair.c -lusb
gcc -o sixpair sixpair.c -lusb

reboot

sudo ./sixpair
    
sudo bluetoothctl
    power on
    default-agent
    scan on
    pair <controller adress, eg.00:00:00:00:00>
    trust <controller adress, eg.00:00:00:00:00>    
 
```

### pygame
For python 3.6 (no idea why)
- install dependencies:
 
```
sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev   libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev
 ```

- install pygame:
     
```
python -m pip install pygame 
 
```

