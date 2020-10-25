import ledStrip
import sys

dc = ledStrip.DeviceControl("85:58:1B:08:97:4D")

dc.turn_on()
print("LED encendido")
input()
print("Color cambiado")
dc.set_color(255,150,255)
input()
print("LED Apagado")
dc.turn_off()
input()
print("CX cerrada")
dc.close_connection()