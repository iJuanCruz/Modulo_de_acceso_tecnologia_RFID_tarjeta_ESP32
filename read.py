import network, time, urequests, utime, framebuf
from time import sleep
from machine import Pin, SoftSPI, I2C
from mfrc522 import MFRC522
from ssd1306 import SSD1306_I2C

#leds
registro_correcto = Pin(4, Pin.OUT)
registro_Incorrecto = Pin(2, Pin.OUT)

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
#conexion a red wifi
def conectaWifi(red, password):
     global miRed
     miRed = network.WLAN(network.STA_IF)     
     if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect('Xiaomi11TPro', '12345678')         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
     return True

        
def buscar_icono(ruta):
    dibujo= open(ruta, "rb")  # Abrir en modo lectura de bist
    dibujo.readline() # metodo para ubicarse en la primera linea de los bist
    xy = dibujo.readline() # ubicarnos en la segunda linea
    x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
    y = int(xy.split()[1])
    icono = bytearray(dibujo.read())  # guardar en matriz de bites
    dibujo.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)

def do_read():
    # Usuario creados
    valor1 = "0x396ebc83"
    nomchip = "Juan_Camilo_Cruz"
    valor2 = "0xb7d185333"
    nombre_tar = "Diego_Beltran"
    salinas = "Registro_Cortolima"
    alcalis = "Registro_Cortolima"
    alcalis_re = "Registro_Cortolima "
    res_pro = "Registro_Cortolima"
    fin = "Registro_Cortolima"


    try:
        
        while True:
            if conectaWifi("Xiaomi11TPro", "12345678"):
                oled.text("Conexion exitosa!", 0, 20)
                oled.show()
                time.sleep(0.05)
                oled.fill(0)
                url = "https://maker.ifttt.com/trigger/lector_rfid/with/key/cQbTK_pVPJSfq7z8oz1cZjK3yEbyd15n675JKLHrR_H?"
                #Envio de correos
                correo = "https://maker.ifttt.com/trigger/correo_rfid/with/key/cQbTK_pVPJSfq7z8oz1cZjK3yEbyd15n675JKLHrR_H?"
                #Mostar logo en Pantalla oled
                oled.blit(buscar_icono("Imagenes/Cortolima.pbm"), 3, 8) # ruta y sitio de ubicación
                oled.show()
                time.sleep(4)
                oled.fill(0)
                oled.show()
                #Mostar mensaje en pantalla oled
                oled.text("Ingresar tarjeta.", 0, 20)
                oled.show()
                time.sleep(3)
                oled.fill(0)
                oled.show()
         
                rdr = MFRC522(spi, sda)
            
                uid = ""
         
                (stat, tag_type) = rdr.request(rdr.REQIDL)
            
                if stat == rdr.OK:
                    (stat, raw_uid) = rdr.anticoll()
                    if stat == rdr.OK:
                        uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                        #comparar valor 1 con el valor ingresado en uid
                        if valor1 == uid:
                            print ("Registro correcto de ",nomchip, alcalis.format(uid))
                            registro_correcto(1)
                            utime.sleep(0.6)
                            registro_correcto(0)
                            utime.sleep(0.1)
                            #Imprimir en pantalla
                            oled.text('Registro correcto', 0, 15)
                            oled.text(nomchip, 0, 30)
                            oled.show()
                            time.sleep(4)
                            oled.fill(0)
                            oled.show()
                        
                     
                            # Envio de registro a IFTTT_Maker_Webhooks_Events
                            respuesta_registro = urequests.get(url+"&value1="+str(nomchip)+"&value2="+(alcalis))
                            respuesta_registro.close ()
                            #Envio de correo de registro de llegada
                        
                            respuesta_correo = urequests.get(correo+"&value1="+str(nomchip)+"&value2="+(alcalis))
                            respuesta_correo.close ()
                            time.sleep(1)
                        
                        elif valor2 == uid:
                            print ("Registro correcto de ", nombre_tar, alcalis_re.format(uid))
                            
                            #Encender Led
                            registro_correcto(1)
                            utime.sleep(0.6)
                            registro_correcto(0)
                            utime.sleep(0.1)
                            
                            #Imprimir en pantalla
                            oled.text('Registro correcto', 0, 15)
                            oled.text(nombre_tar, 0, 30)
                            oled.show()
                            time.sleep(4)
                            oled.fill(0)
                            oled.show()
                            # Envio de registro a IFTTT_Maker_Webhooks_Events
                            respuesta_registro = urequests.get(url+"&value1="+str(nombre_tar)+"&value2="+(alcalis_re))
                            respuesta_registro.close ()
                            #Envio de correo de registro de llegada                    
                            respuesta_correo = urequests.get(correo+"&value1="+str(nombre_tar)+"&value2="+(alcalis_re))
                            respuesta_correo.close ()
                            time.sleep(1)
 
                        else:
                            print("Error de autentificación")
                            registro_Incorrecto(1)
                            utime.sleep(0.6)
                            registro_Incorrecto(0)
                            utime.sleep(0.1)
                            oled.text("Error de ", 0, 15)
                            oled.text("autentificacion", 0, 25)
                            oled.show()
                            time.sleep(4)
                            oled.fill(0)
                            oled.show()
            else:
                print("Error de conexion con WIFI")
             
    except KeyboardInterrupt:
        print("Bye")

do_read()

if __name__==("__main__"):
    main()