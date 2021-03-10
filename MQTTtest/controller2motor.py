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


class Motor:
    def __init__(self, sensitivity=1, speed0 = 50, n_bins=10, setup_name=None, device_ID=None, mqtt_client=None, motor_name=None):
        self.dx = 0
        self.mqtt = MQTTDevice(setup=setup_name, device=device_ID, mqtt_client=mqtt_client)
        self.sensitivity = sensitivity
        self.bins = np.linspace(0, 1.01, n_bins)
        self.motor_name = motor_name
        self.speed = speed0

    def get_new_dx(self, defl):
        return np.sign(defl) * self.speed * np.power(self.bins[np.digitize(np.abs(defl), self.bins)], self.sensitivity)

    def send(self, current_dx):
        new_dx = self.get_new_dx(current_dx)
        if self.dx != new_dx:
            self.mqtt.send(self.motor_name, new_dx)
            self.dx = new_dx
        else:
            pass


def main():
    import pygame
    # ============== set sever parameters ==============
    setup_name          = "S001"
    device_ID           = "RAS01"
    device_MQTT_name    = "RASPI_" + str(randint(0, 100000))
    mqtt_broker_ip      = "localhost"
    
    mqtt_client_name    = "raspi1" # not necessary
    mqtt_client_pass    = "1ipsar" # not necessary

    mqtt_port           = 1883
    mqtt_keepalive      = 60
    mqtt_uselogin       = False

    # ============== set joystick parameters ==============
    messages_per_sec = 50

    # using dx -> speed * binned(dx)^sensitivity
    speed = 50
    n_bins = 10
    sensitivity = 1.4
    speed_increase = 1.2

    # init class and auto-connect to server
    uc2 = MQTTtest( setup_name=setup_name,
                    device_ID=device_ID,
                    device_MQTT_name=device_MQTT_name,
                    mqtt_broker_ip=mqtt_broker_ip,
                    mqtt_client_name=mqtt_client_name,
                    mqtt_client_pass=mqtt_client_pass,
                    mqtt_port=mqtt_port,
                    mqtt_keepalive=mqtt_keepalive,
                    mqtt_uselogin=mqtt_uselogin)

    # add the motors
    motor_x = Motor(    sensitivity=sensitivity, 
                        speed0=speed, 
                        n_bins=n_bins, 
                        setup_name=setup_name, 
                        device_ID="OCM21", 
                        motor_name="MM_X", 
                        mqtt_client = uc2.mqtt_client)

    motor_y = Motor(    sensitivity=sensitivity, 
                        speed0=speed, 
                        n_bins=n_bins, 
                        setup_name=setup_name, 
                        device_ID="OCM21", 
                        motor_name="MM_Y",
                        mqtt_client = uc2.mqtt_client)


    motor_z = Motor(    sensitivity=sensitivity, 
                        speed0=speed, 
                        n_bins=n_bins, 
                        setup_name=setup_name, 
                        device_ID="OCM21", 
                        motor_name="MM_Z",
                        mqtt_client = uc2.mqtt_client)
                     

    
    # ============== initialize the joystick ==============
    pygame.init()
    # front_screen = pygame.font.SysFont('Comic Sans MS', 30)
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
    
    done = False
    print_help()

    if not use_controller:
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT or event.key == pygame.K_q:
                        done = True
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        if event.key == pygame.K_a:
                            motor_x.speed /= speed_increase
                            motor_y.speed /= speed_increase
                            motor_z.speed /= speed_increase
                        if event.key == pygame.K_d:
                            motor_x.speed *= speed_increase
                            motor_y.speed *= speed_increase
                            motor_z.speed *= speed_increase

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                motor_x.send(-1)
            elif keys[pygame.K_RIGHT]:
                motor_x.send(1)
            else:
                motor_x.send(0)
            
            if keys[pygame.K_DOWN]:
                motor_y.send(-1)
            elif keys[pygame.K_UP]:
                motor_y.send(1)
            else:
                motor_y.send(0)
            
            if keys[pygame.K_s]:
                motor_z.send(-1)
            elif keys[pygame.K_w]:
                motor_z.send(1)
            else:
                motor_z.send(0)

            clock.tick(messages_per_sec)            
                        
    else:                    
        while not done:
            for event in pygame.event.get():                
                if joystick.get_button(Buttons.select):
                    done = True
                if joystick.get_button(Buttons.up):
                    motor_x.speed *= speed_increase
                    motor_y.speed *= speed_increase
                    motor_z.speed *= speed_increase
                if joystick.get_button(Buttons.down):
                    motor_x.speed /= speed_increase
                    motor_y.speed /= speed_increase
                    motor_z.speed /= speed_increase

            l3_axis = [joystick.get_axis(i) for i in [Axis.l3_x,Axis.l3_y]] # [0,1]
            r3_axis = [joystick.get_axis(i) for i in [Axis.r3_x,Axis.r3_y]]
            
            motor_x.send(l3_axis[0])
            motor_y.send(l3_axis[1])
            motor_z.send(r3_axis[1])

            clock.tick(messages_per_sec)
            
    pygame.quit()

if __name__ == "__main__":
    main()

