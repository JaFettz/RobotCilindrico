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

Codigo_1 = open("Codigo_edit.txt","w+")
Codigo_2 = open("Codigo.txt","r")

Estado = 0
controller.set_led(Xbox.LED_BLINK_SLOW)

#Pasos por movimiento
pasos_x = 0
pasos_y = 0
pasos_z = 0
#Pasos absolutos
pasos_x_abs = 0
pasos_y_abs = 0
pasos_z_abs = 0


try:
    controller.set_led(Xbox.LED_ROTATE)
    while(True): #Inicio
        if(Estado == 'Manual'):
            print("Manual")
            Stop = False
            Codigo_1 = open("Codigo_edit.txt","w")
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
                        pasos_x = pasos_x+1
                        print("Positivo")

                    #Movimiento en X negativo
                    elif(controller.axis_l.x < -0.5 and
                            (controller.trigger_l.value > 0.3 or
                                controller.trigger_r.value > 0.3)):
                        Direccion = False
                        Mover_Motor("X",True,1)
                        pasos_x = pasos_x-1
                        print("Negativo")

                elif(controller.button_y.is_pressed):
                    print("moviendo y")
                    #Movimiento en Y positivo
                    if(controller.axis_l.x > 0.5 and
                            (controller.trigger_l.value > 0.3 or
                                controller.trigger_r.value > 0.3)):
                        Direccion = True
                        Mover_Motor("Y",True,1)
                        pasos_y = pasos_y+1
                        print("Positivo")

                    #Movimiento en Y negativo
                    elif(controller.axis_l.x < -0.5 and
                            (controller.trigger_l.value > 0.3 or
                                controller.trigger_r.value > 0.3)):
                        Direccion = False
                        Mover_Motor("Y",True,1)
                        pasos_y = pasos_y-1
                        print("Negativo")

                elif(controller.button_b.is_pressed):
                    print("moviendo z")
                    #Movimiento en Z positivo
                    if(controller.axis_l.x > 0.5 and
                            (controller.trigger_l.value > 0.3 or
                                controller.trigger_r.value > 0.3)):
                        Direccion = True
                        Mover_Motor("TZ",True,1)
                        pasos_z = pasos_z+1
                        print("Positivo")

                    #Movimiento en Z negativo
                    elif(controller.axis_l.x < -0.5 and
                            (controller.trigger_l.value > 0.3 or
                                controller.trigger_r.value > 0.3)):
                        Direccion = False
                        Mover_Motor("TZ",True,1)
                        pasos_z = pasos_z-1
                        print("Negativo")

                elif(controller.button_a.is_pressed):
                    Data = ["X\n", "{}\n".format(pasos_x), "Y\n", "{}\n".format(pasos_y), "TZ\n", "{}\n".format(pasos_z)]
                    Codigo_1.writelines(Data)
                    print("Guardado")
                    while(controller.button_a.is_pressed):
                        pasos_x = 0
                        pasos_y = 0
                        pasos_z = 0
                    #controller.set_rumble(0.5,0.5,500)

                elif(controller.button_mode.is_pressed):
                    Estado = 0
                    Stop = True
                    controller.set_led(Xbox.LED_ROTATE)
                    Codigo_1.close()


        elif(Estado == 'Auto'):
            print("Auto")
            Stop = False
            Codigo_1 = open("Codigo_edit.txt","r")
            Codigo_2 = open("Codigo.txt","r")
            controller.set_led(Xbox.LED_TOP_LEFT_ON)

            while(not Stop):    #Se queda en modo Auto hasta oprimir STOP
                if(controller.button_a.is_pressed):
                    Codigo = Codigo_1.readlines()
                    Stop_2 = False
                    controller.set_led(Xbox.LED_BOTTOM_LEFT_BLINK_ON)
                    while(not Stop_2):
                        for i in range(int(len(Codigo)/2)):
                            if(controller.button_mode.is_pressed):
                                Stop_2 = True
                                controller.set_led(Xbox.LED_ROTATE)
                            Eje = Codigo[i*2]
                            Pasos = int(Codigo[i*2+1])
                            if(Pasos < 0):
                                Pasos = Pasos*-1
                                Direccion = False
                            else:
                                Direccion = True

                            if(Pasos != 0):
                                Mover_Motor(Eje,True,Pasos)


                        Stop_2 = True
                        controller.set_led(Xbox.LED_TOP_LEFT_ON)
                        Codigo_2.close()

                elif(controller.button_b.is_pressed):
                    Codigo = Codigo_2.readlines()
                    Stop_2 = False
                    controller.set_led(Xbox.LED_BOTTOM_RIGHT_BLINK_ON)
                    while(not Stop_2):
                        for i in range(int(len(Codigo)/2)):
                            if(controller.button_mode.is_pressed):
                                Stop_2 = True
                                controller.set_led(Xbox.LED_ROTATE)
                            Eje = Codigo[i*2]
                            Pasos = int(Codigo[i*2+1])
                            if(Pasos < 0):
                                Pasos = Pasos*-1
                                Direccion = False
                            else:
                                Direccion = True

                            if(Pasos != 0):
                                Mover_Motor(Eje,True,Pasos)

                        Stop_2 = True
                        controller.set_led(Xbox.LED_TOP_LEFT_ON)
                        Codigo_2.close()


                elif(controller.button_mode.is_pressed):
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
