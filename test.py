import signal
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib as Stepper
from xbox360controller import Xbox360Controller as Xbox

def Enable(Motor):
    if(Motor == "X"):
        GPIO.output(2,0)
    elif(Motor == "Y"):
        GPIO.output(3,0)
    elif(Motor == "TZ"):
        GPIO.output(4,0)

def Disable(Motor):
    if(Motor == "X"):
        GPIO.output(2,1)
    elif(Motor == "Y"):
        GPIO.output(3,1)
    elif(Motor == "TZ"):
        GPIO.output(4,1)

def Mover_Motor(Motor_sel, Direccion = True, Paso = 1):
    Enable(Motor_sel)
    Motor.motor_go(Direccion,"Full",Paso,.001,True,.05)
    Disable(Motor_sel)

#Configuracion Driver de stepper
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)

GPIO.output(2,1)
GPIO.output(3,1)
GPIO.output(4,1)
GPIO_pins = (14,15,18)

direction = 20
step = 21

Motor = Stepper.A4988Nema(direction,step,GPIO_pins,"A4988")

#Codigo Robot
controller = Xbox(0,axis_threshold = 0.2)
Codigo_1 = open("Codigo_edit.txt","w")
Codigo_2 = open("Codigo.txt")

Estado = 0
controller.set_led(Xbox.LED_BLINK_SLOW)
x = 0
y = 0
z = 0

try:
    controller.set_led(Xbox.LED_ROTATE)
    while(True): #Inicio
        if(Estado == 'Manual'):
            print("Manual")
            Stop = False
            controller.set_led(Xbox.LED_TOP_RIGHT_ON)
            
            while(not Stop):    #Se queda en modo Manual hasta oprimir STOP
                #Movimiento de los ejes en manual checa si tiene deadman switch (Gatillos L o R)
                #Dirección de movimiento por joystick L Izquierda-Negativo, Derecha-Positivo
                #Selección de eje por botones X-X, Y-Y, B-Z
                #Guardar Codigo es A
                if(controller.button_x.is_pressed):
                    print("moviendo x")
                    if(controller.axis_l.x > 0.5 and
                            (controller.trigger_l.value > 0.3 or
                                controller.trigger_r.value > 0.3)):
                        Direccion = True
                        Mover_Motor("X",True,1)
                        x = x+1
                        print("Positivo")

                    #Movimiento en X negativo
                    elif(controller.axis_l.x < -0.5 and
                            (controller.trigger_l.value > 0.3 or
                                controller.trigger_r.value > 0.3)):
                        Direccion = False
                        Mover_Motor("X",True,1)
                        x = x-1
                        print("Negativo")

                elif(controller.button_y.is_pressed):
                    print("moviendo y")
                    #Movimiento en Y positivo
                    if(controller.axis_l.x > 0.5 and
                            (controller.trigger_l.value > 0.3 or
                                controller.trigger_r.value > 0.3)):
                        Direccion = True
                        Mover_Motor("Y",True,1)
                        x = x+1
                        print("Positivo")

                    #Movimiento en Y negativo
                    elif(controller.axis_l.x < -0.5 and
                            (controller.trigger_l.value > 0.3 or
                                controller.trigger_r.value > 0.3)):
                        Direccion = False
                        Mover_Motor("Y",True,1)
                        x = x-1
                        print("Negativo")

                elif(controller.button_b.is_pressed):
                    print("moviendo z")
                    #Movimiento en Z positivo
                    if(controller.axis_l.x > 0.5 and
                            (controller.trigger_l.value > 0.3 or
                                controller.trigger_r.value > 0.3)):
                        Direccion = True
                        Mover_Motor("TZ",True,1)
                        x = x+1
                        print("Positivo")

                    #Movimiento en Z negativo
                    elif(controller.axis_l.x < -0.5 and
                            (controller.trigger_l.value > 0.3 or
                                controller.trigger_r.value > 0.3)):
                        Direccion = False
                        Mover_Motor("TZ",True,1)
                        x = x-1
                        print("Negativo")

                elif(controller.button_mode.is_pressed):
                    Estado = 0
                    Stop = True
                    controller.set_led(Xbox.LED_ROTATE)


        elif(Estado == 'Auto'):
            print("Auto")
            Stop = False
            controller.set_led(Xbox.LED_TOP_LEFT_ON)

            while(not Stop):    #Se queda en modo Auto hasta oprimir STOP
                if(controller.button_mode.is_pressed):
                    Estado = 0
                    Stop = True
                    controller.set_led(Xbox.LED_ROTATE)


        if(controller.button_trigger_r.is_pressed):
            Estado = "Manual"
        elif(controller.button_trigger_l.is_pressed):
            Estado = "Auto"


except KeyboardInterrupt:
    pass

controller.set_led(Xbox.LED_BLINK_SLOW)
GPIO.cleanup()
