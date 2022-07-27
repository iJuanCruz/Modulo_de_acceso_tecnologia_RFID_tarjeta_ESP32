import network, time, urequests
from time import sleep
from machine import Pin, SoftSPI, I2C
from mfrc522 import MFRC522
from ssd1306 import SSD1306_I2C
import framebuf

#Modulo RFID
sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.OUT)
spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
sda = Pin(5, Pin.OUT)

#pantalla led
ancho = 128
alto = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(ancho, alto, i2c)

print(i2c.scan())

def buscar_icono(ruta):
    dibujo= open(ruta, "rb")  # Abrir en modo lectura de bist
    dibujo.readline() # metodo para ubicarse en la primera linea de los bist
    xy = dibujo.readline() # ubicarnos en la segunda linea
    x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
    y = int(xy.split()[1])
    icono = bytearray(dibujo.read())  # guardar en matriz de bites
    dibujo.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)


def do_write():

    try:
        while (True):
            
            #Mostrar LOGO en pantalla
            oled.blit(buscar_icono("Imagenes/Cortolima.pbm"), 3, 8) # ruta y sitio de ubicación
            oled.show()
            time.sleep(2)
            oled.fill(0)
            oled.show()
            
            #imprimir mensaje en pantalla led
            oled.text("**Coloque la ", 0, 10)
            oled.text("tarjeta para ", 0, 25)
            oled.text("ser registrada** ", 0, 40)
            oled.show()
            time.sleep(4)
            oled.fill(0)
            oled.show()
            
            rdr = MFRC522(spi, sda)
    
            (stat, tag_type) = rdr.request(rdr.REQIDL)  


            if stat == rdr.OK:
                
                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:

                    print("Nueva tarjeta detectada")
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:
                        
                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                            
                        if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                            stat = rdr.write(8, b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f")
                            rdr.stop_crypto1()
                            if stat == rdr.OK:
                                print("Tarjeta registrada")
                              
                                oled.text("Tarjeta ", 0, 15)
                                oled.text("registrada", 0, 25)
                                oled.show()
                                time.sleep(4)
                                oled.fill(0)
                                oled.show()
                                print()
                          
                            else:
                                print("Fallo al registrar la tajeta")
                                oled.text("Fallo al registrar", 0, 15)
                                oled.text("la tajeta", 0, 25)
                                oled.show()
                                time.sleep(4)
                                oled.fill(0)
                                oled.show()  
                        else:
                            print("Error de autenticación")
                            oled.text("Error de ", 0, 15)
                            oled.text("autenticacion", 0, 25)
                            oled.show()
                            time.sleep(4)
                            oled.fill(0)
                            oled.show()                             
                    else:
                        print("No se puede seleccionar la etiqueta")
                        oled.text("No se puede ", 0, 15)
                        oled.text("seleccionar la etiqueta", 0, 25)
                        oled.show()
                        time.sleep(4)
                        oled.fill(0)
                        oled.show()   
         
    except KeyboardInterrupt:
        print("Bye")
do_write() 