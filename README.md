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
