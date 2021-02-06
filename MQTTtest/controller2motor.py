import numpy as np
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
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

def print_help():
    print("\tPress LEFT and RIGHT to move in X-direction")
    print("\tPress DOWN and UP to move in Y-direction")
    print("\tPress W and S to move in Z-direction")
    print("\tPress D to increase sensitivity by 20% and A to do the opposite")
    print("\tPress Q to quit")



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

    sensitivity = 10
    sensitivity_scaling = 1.2
    messages_per_sec = 20

    # init class and auto-connect to server
    uc2 = MQTTtest(setup_name=setup_name,device_ID=device_ID,device_MQTT_name=device_MQTT_name,mqtt_broker_ip=mqtt_broker_ip,mqtt_client_name=mqtt_client_name,mqtt_client_pass=mqtt_client_pass,mqtt_port=mqtt_port,mqtt_keepalive=mqtt_keepalive,mqtt_uselogin=mqtt_uselogin)

    # add the motors
    uc2.mqtt_register_devices(device_name='Motor_z',device_ID='OCM21')
    uc2.mqtt_register_devices(device_name='Motor_x',device_ID='OCM21')
    uc2.mqtt_register_devices(device_name='Motor_y',device_ID='OCM21')
 
    pygame.init()

    front_screen = pygame.font.SysFont('Comic Sans MS', 30)


    clock = pygame.time.Clock() # Used to manage how fast the screen updates.

    joystick_count = pygame.joystick.get_count()
    if not joystick_count:
        print('No joystick connected, use keyboard')
        use_controller = False
    else:
        use_controller = True
        print("Number of joysticks: {}".format(joystick_count))
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    done =False
    
    print_help()

    if not use_controller:
        screen = pygame.display.set_mode((400,300))
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT or event.key == pygame.K_q:
                        done = True
                    if event.key == pygame.K_a:
                            sensitivity/=sensitivity_scaling
                    if event.key == pygame.K_d:
                            sensitivity*=sensitivity_scaling

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                uc2.devices['Motor_x'].send("MM_X",-sensitivity)
            if keys[pygame.K_RIGHT]:
                uc2.devices['Motor_x'].send("MM_X",sensitivity)
            if keys[pygame.K_UP]:
                uc2.devices['Motor_x'].send("MM_Y",sensitivity)
            if keys[pygame.K_DOWN]:
                uc2.devices['Motor_y'].send("MM_Y",-sensitivity)
            if keys[pygame.K_w]:
                uc2.devices['Motor_z'].send("MM_Z",sensitivity)
            if keys[pygame.K_s]:
                uc2.devices['Motor_z'].send("MM_Z",-sensitivity)

            # for event in pygame.event.get():
            #     if event.type == pygame.KEYDOWN:
            #         if event.type == pygame.QUIT or event.key == pygame.K_q:
            #             done = True
            #         if event.key == pygame.K_LEFT:
            #             uc2.devices['Motor_x'].send("MM_X",-1)
            #         if event.key == pygame.K_RIGHT:
            #             uc2.devices['Motor_x'].send("MM_X",1)
            #         if event.key == pygame.K_UP:
            #             uc2.devices['Motor_y'].send("MM_Y",1)
            #         if event.key == pygame.K_DOWN:
            #             uc2.devices['Motor_y'].send("MM_Y",-1)
            #         if event.key == pygame.K_w:
            #             uc2.devices['Motor_z'].send("MM_Z",1)
            #         if event.key == pygame.K_s:
            #             uc2.devices['Motor_z'].send("MM_Z",-1)

            textsurface = front_screen.render('Sensitivity {:.2f}:'.format(sensitivity), False, (255, 255, 255))
            screen.blit(textsurface,(0,0))
            clock.tick(messages_per_sec)            
                        
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
            clock.tick(messages_per_sec)
            
    pygame.quit()

if __name__ == "__main__":
    main()

