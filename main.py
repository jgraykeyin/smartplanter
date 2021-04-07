from machine import UART, Pin, ADC, I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from DHT22 import DHT22
import utime

# Hardware settings for LCD
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Connect to the LCD
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Clear the screen and turn on the backlight
lcd.clear()
lcd.backlight_on()
lcd.move_to(0,0)

#Init the LEDS
led_red = machine.Pin(15, machine.Pin.OUT)
led_yellow = machine.Pin(14, machine.Pin.OUT)
led_green = machine.Pin(13, machine.Pin.OUT)
onboard_led = machine.Pin(25, machine.Pin.OUT)

# Make sure they're all off
led_red.off()
led_yellow.off()
led_green.off()

# But turn on the onboard LED
onboard_led.on()

# Initalize the DHT22 Humidity & Temp sensor
dht22 = DHT22(Pin(19,Pin.IN,Pin.PULL_UP))


# Function accepts name of plant and ADC pin num
def getSoilMoisture(name, adc):
    # Get data from the moisture sensor
    soil_sensor = ADC(adc)
    moisture = soil_sensor.read_u16()
    display = ""
    
    #min = 14200
    #max = 17000
    min = 14000
    max = 17000
    
    # Calculate the moisture percentage
    percent_init = ((moisture - min) * 100) / (max - min)
    percent = 100 - abs(percent_init)
    
    # Convert the numerical value into a readable value
    if moisture < min:
        display = "{}:Wet".format(name)
    elif moisture >= min and moisture < max:
        display = "{}:Dmp".format(name)
    elif moisture >= max:
        display = "{}:Dry".format(name)
        
    return [display, percent]


def getTemperature():
    # Get Temperature
    temp_sensor = ADC(4)
    temperature = temp_sensor.read_u16()
    to_volts = 3.3 / 65535
    temperature = temperature * to_volts
    celcius_degrees = 27 - (temperature - 0.706) / 0.001721
    return celcius_degrees


def selectLED(color):
    # Make sure only a single color is turned on
    if color == "green":
        led_green.on()
        led_yellow.off()
        led_red.off()
    elif color == "yellow":
        led_green.off()
        led_yellow.on()
        led_red.off()
    elif color == "red":
        led_green.off()
        led_yellow.off()
        led_red.on()
        

# Setup UART communications
BAUD = 9600
uart = UART(1, BAUD, tx=Pin(4), rx=Pin(5))

print("Starting...")

while True:
    
    # Get the temp and humidity
    T, H = dht22.read()

    # Get the temperature
    base_temp = T
    
    
    # Soil moisture for Bird of Paradise (BoP)
    bop_soil = getSoilMoisture("BoP", 0)
    bop_moisture = bop_soil[0]
    bop_percent = round(bop_soil[1])
    
    # Soil moisture for Monstera (MON)
    mon_soil = getSoilMoisture("MON", 1)
    mon_moisture = mon_soil[0]
    mon_percent = round(mon_soil[1])
    
    # Output temp to the LCD
    lcd.move_to(0,0)
    lcd.putstr("{} C  RH: {}%".format(round(base_temp), H))
    lcd.move_to(0,1)
    lcd.putstr("{}".format(bop_moisture))
    lcd.move_to(8,1)
    lcd.putstr("{}".format(mon_moisture))
    
    
    temperature = str(round(base_temp, 2))
    data = temperature + ":" + bop_moisture + ":" + str(bop_percent) + ":" + mon_moisture + ":" + str(mon_percent) + ":" + str(H) + "*"
    uart.write("{}".format(data))
    
    utime.sleep(10)



