# openCM2

## Non-UC2 Dependencies 
- numpy
- pygame 

## Motor Interaction
```python
if np.abs(l3_axis[0])>0.1:
    uc2.devices['Motor_x'].send(l3_axis[0])
if np.abs(l3_axis[1])>0.1:
    uc2.devices['Motor_y'].send(l3_axis[1])                
if np.abs(r3_axis[1])>0.1:
    uc2.devices['Motor_z'].send(r3_axis[1])
```

with 
```python
uc2.mqtt_register_devices(device_name='Motor_z',device_ID='MOT01')
uc2.mqtt_register_devices(device_name='Motor_x',device_ID='MOT02')
uc2.mqtt_register_devices(device_name='Motor_y',device_ID='MOT02')
```


## Installation
Do everything below in UC2 env if you use that.

### for controller connection
```
wget http://www.pabr.org/sixlinux/sixpair.c
gcc -o sixpair.c -lusb
gcc -o sixpair sixpair.c -lusb

reboot

sudo ./sixpair
    
sudo bluetoothctl
    power on
    default-agent
    scan on
    pair < controller adress, eg.00:00:00:00:00>
    trust < controller adress, eg.00:00:00:00:00>    
 
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

