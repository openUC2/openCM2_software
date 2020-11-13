import numpy as np
import sys
import os
import pygame

from MQTTDevice import MQTTDevice
import paho.mqtt.client as mqtt
from random import randint
from time import time, sleep

from ps3_controller_config import *
from cmdInterface import MQTTtest
    
# ============================================================================ #
# ============================================================================ #
# ============================================================================ #
# ============================================================================ #
# ============================================================================ #

def main():
    import pygame
    # set parameters
    setup_name          = "S001"
    device_ID           = "RAS01"
    device_MQTT_name    = "RASPI_" + str(randint(0, 100000))
    mqtt_broker_ip      = "localhost"
    mqtt_client_name    = "raspi1" # not necessary
    mqtt_client_pass    = "1ipsar" # not necessary
    mqtt_port           = 1883
    mqtt_keepalive      = 60
    mqtt_uselogin       = False

    # init class and auto-connect to server
    uc2 = MQTTtest(setup_name=setup_name,device_ID=device_ID,device_MQTT_name=device_MQTT_name,mqtt_broker_ip=mqtt_broker_ip,mqtt_client_name=mqtt_client_name,mqtt_client_pass=mqtt_client_pass,mqtt_port=mqtt_port,mqtt_keepalive=mqtt_keepalive,mqtt_uselogin=mqtt_uselogin)

    # add a motor
    uc2.mqtt_register_devices(device_name='Motor_z',device_ID='MOT01')
    uc2.mqtt_register_devices(device_name='Motor_x',device_ID='MOT02')
    uc2.mqtt_register_devices(device_name='Motor_y',device_ID='MOT02')
 
    fps = 20
    pygame.init()

    clock = pygame.time.Clock() # Used to manage how fast the screen updates.

    #joystick_count = pygame.joystick.get_count()
    #if not joystick_count:
    if True:
        print('No joystick connected, use keyboard')
        use_controller = False
    else:
        use_controller = True
        print("Number of joysticks: {}".format(joystick_count))
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    done =False
    
    if not use_controller:
        screen = pygame.display.set_mode((400,300))
        while not done:
#            print(pygame.key.get_pressed())
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT or event.key == pygame.K_q:
                        done = True
                    if event.key == pygame.K_LEFT:
                        uc2.devices['Motor_x'].send(-1)
                    if event.key == pygame.K_RIGHT:
                        uc2.devices['Motor_x'].send(1)
                    if event.key == pygame.K_UP:
                        uc2.devices['Motor_y'].send(1)
                    if event.key == pygame.K_DOWN:
                        uc2.devices['Motor_y'].send(-1)
                    if event.key == pygame.K_w:
                        uc2.devices['Motor_z'].send(1)
                    if event.key == pygame.K_s:
                        uc2.devices['Motor_z'].send(-1)
            clock.tick(fps)            
                        
    else:                    
        while not done:
            for event in pygame.event.get():                
                if joystick.get_button(Buttons.select):
                        done = True
            l3_axis = [joystick.get_axis(i) for i in [Axis.l3_x,Axis.l3_y]] # [0,1]
            r3_axis = [joystick.get_axis(i) for i in [Axis.r3_x,Axis.r3_y]]
            
            if np.abs(l3_axis[0])>0.1:
                uc2.devices['Motor_x'].send(l3_axis[0])
            if np.abs(l3_axis[1])>0.1:
                uc2.devices['Motor_y'].send(l3_axis[1])                
            if np.abs(r3_axis[1])>0.1:
                uc2.devices['Motor_z'].send(r3_axis[1])
            clock.tick(fps)
            
    pygame.quit()

if __name__ == "__main__":
    main()

