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


def print_help_keyboard():
    print("\tPress LEFT and RIGHT to move in X-direction")
    print("\tPress DOWN and UP to move in Y-direction")
    print("\tPress W and S to move in Z-direction")
    print("\tPress D to increase sensitivity by 5% and A to do the opposite")
    print("\tPress 0 to set motor postion to 0")
    print("\tPress Q to quit")

def print_help_js():
    print("\tMove left joystick to move in X- and Y- direction")
    print("\tMove right joystick to move in Z-direction")
    print("\tPress UP-button to increase sensitivity by 5% and DOWN-button to do the opposite")
    print("\tPress X to set motor postion to 0")
    print("\tPress SELECT to quit")

class Motor:
    def __init__(self, sensitivity=1, n_bins=10, setup_name=None, device_ID=None, mqtt_client=None, motor_name=None, init=0):
        self.dx = 0
        self.x = init
        self.mqtt = MQTTDevice(setup=setup_name, device=device_ID, mqtt_client=mqtt_client)
        self.sensitivity = sensitivity
        self.bins = np.linspace(0, 1.01, n_bins)
        self.motor_name = motor_name

    def get_new_dx(self, defl, speed):
        return np.sign(defl) * speed * np.power(self.bins[np.digitize(np.abs(defl), self.bins)], self.sensitivity)

    def move(self, current_dx, speed):
        new_dx = self.get_new_dx(current_dx, speed)
        # if self.dx != new_dx:
        #     self.mqtt.move(self.motor_name, new_dx)
        #     self.dx = new_dx
        # else:
        #     pass
        self.mqtt.send(self.motor_name, new_dx)
        self.dx = new_dx
        self.x += self.dx

def display_params(screen, speed, motor_x, motor_y, motor_z):
    screen_size = pygame.display.get_surface().get_size()

    screen.fill(pygame.Color('white'))
    font = pygame.font.SysFont("DejaVu Sans Mono", 15)

    label = font.render("Speed: {:>3.1f}".format(speed), 1, (0,0,0))
    text_rect = label.get_rect(topleft=(0,0))
    screen.blit(label, text_rect)

    motor_color = (56,0,140)
    label = font.render("X: {:>8.1f}, dX: {:>5.1f}".format(motor_x.x, motor_x.dx), 1, motor_color)
    text_rect = label.get_rect(topleft=(5, screen_size[1]/4))
    screen.blit(label, text_rect)

    label = font.render("Y: {:>8.1f}, dY: {:>5.1f}".format(motor_y.x, motor_y.dx), 1, motor_color)
    text_rect = label.get_rect(topleft=(5, screen_size[1]/2))
    screen.blit(label, text_rect)
    
    label = font.render("Z: {:>8.1f}, dZ: {:>5.1f}".format(motor_z.x, motor_z.dx), 1, motor_color)
    text_rect = label.get_rect(topleft=(5, 3*screen_size[1]/4))
    screen.blit(label, text_rect)

    pygame.display.update()


def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))

# ============================================================================ #
# ============================================================================ #
# ============================================================================ #
def main():
    import pygame

    postion_file_name = ".pos.config"
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


    device_IDs = ["OCM2X", "OCM2Y", "OCM2X"]
    # ============== set joystick parameters ==============
    messages_per_sec = 50

    # using dx -> speed * binned(dx)^sensitivity NOT binned anymore
    speed = 50
    n_bins = 10
    sensitivity = 1.4
    speed_increase = 1.05

    if os.path.isfile(postion_file_name + '.npz'):
        init_postion = np.load(postion_file_name + '.npz')
    else:
        init_postion = {"x":0, "y":0, "z":0}
        print("No init postion file found, but will be created when program is closed")


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

    uc2.mqtt_client.on_message = on_message

    # add the motors
    motor_x = Motor(    sensitivity=sensitivity, 
                        n_bins=n_bins, 
                        setup_name=setup_name, 
                        device_ID=device_IDs[0], 
                        motor_name="MM_X", 
                        mqtt_client = uc2.mqtt_client, 
                        init=init_postion['x'])

    motor_y = Motor(    sensitivity=sensitivity, 
                        n_bins=n_bins, 
                        setup_name=setup_name, 
                        device_ID=device_IDs[1], 
                        motor_name="MM_Y",
                        mqtt_client = uc2.mqtt_client, 
                        init=init_postion['y'])


    motor_z = Motor(    sensitivity=sensitivity, 
                        n_bins=n_bins, 
                        setup_name=setup_name, 
                        device_ID=device_IDs[2], 
                        motor_name="MM_Z",
                        mqtt_client = uc2.mqtt_client, 
                        init=init_postion['z'])
                     

    
    # ============== initialize the joystick ==============
    pygame.init()

    screen = pygame.display.set_mode((220,100))
    pygame.display.set_caption("openCM2")
    
    clock = pygame.time.Clock() # Used to manage how fast the screen updates.

    joystick_count = pygame.joystick.get_count()
    if not joystick_count:
        print('No joystick connected, use keyboard')
        use_controller = False
        print_help_keyboard()
    else:
        use_controller = True
        print("Number of joysticks: {}".format(joystick_count))
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print_help_js()
    
    done = False

    while not done:
        display_params(screen, speed, motor_x, motor_y, motor_z)
        if not use_controller:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT or event.key == pygame.K_q:
                        done = True
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        if event.key == pygame.K_a:
                            speed /= speed_increase
                        if event.key == pygame.K_d:
                            speed *= speed_increase
                    if event.key == pygame.K_0:
                        motor_x.x = 0
                        motor_y.x = 0
                        motor_z.x = 0

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                motor_x.move(-1, speed)
            elif keys[pygame.K_RIGHT]:
                motor_x.move(1, speed)
            else:
                motor_x.move(0, speed)
            
            if keys[pygame.K_DOWN]:
                motor_y.move(-1, speed)
            elif keys[pygame.K_UP]:
                motor_y.move(1, speed)
            else:
                motor_y.move(0, speed)
            
            if keys[pygame.K_s]:
                motor_z.move(-1, speed)
            elif keys[pygame.K_w]:
                motor_z.move(1, speed)
            else:
                motor_z.move(0, speed)

            clock.tick(messages_per_sec)            
                        
        else:
            for event in pygame.event.get():                
                if joystick.get_button(Buttons.select):
                    done = True
                if joystick.get_button(Buttons.up):
                    speed *= speed_increase
                if joystick.get_button(Buttons.down):
                    speed /= speed_increase
                if joystick.get_button(Buttons.x):
                    motor_x.x = 0
                    motor_y.x = 0
                    motor_z.x = 0

            l3_axis = [joystick.get_axis(i) for i in [Axis.l3_x,Axis.l3_y]] # [0,1]
            r3_axis = [joystick.get_axis(i) for i in [Axis.r3_x,Axis.r3_y]]
            
            motor_x.move(l3_axis[0], speed)
            motor_y.move(l3_axis[1], speed)
            motor_z.move(r3_axis[1], speed)
            
            clock.tick(messages_per_sec)

    d = {"x": motor_x.x, "y": motor_y.x, "z": motor_z.x}
    np.savez_compressed(postion_file_name, **d)
            
    pygame.quit()

if __name__ == "__main__":
    main()

