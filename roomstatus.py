import serial
import json

# Connet to the Pi's serial connection, which matches the same BAUD as the Pico
BAUD = 9600
ser = serial.Serial("/dev/ttyS0", BAUD)

print("Reading...")

text = ""
logging = False

# Monitor the data, look for a * to note the beginning of a data chunk.
# The next * will note the end of a data chunk.
# Everything in between two *'s will be the data we need.
while True: 
    received_data = ser.read()
    print(received_data)

    data_str = str(received_data)

    data = data_str[2]

    if data == "*" and logging == False:
        logging = True
    elif data != "*" and logging == True:
        text = text + data
    elif data == "*" and logging == True:
        logging = False
        break

# Split the data up so we can find the moisture and temperature values
sensor_data = text.split(":")

print(sensor_data)

temp = sensor_data[0]

# Get soil data for the Bird of Paradise
bop_moisture = sensor_data[2]
bop_percent = sensor_data[3]

# Get soil data for the Monstera
mon_moisture = sensor_data[5]
mon_percent = sensor_data[6]

# Get Humidity
humidity = sensor_data[7]

# Format the data into a JSON file
jsondata = {}
jsondata["room"] = []
jsondata["room"].append({
    'temperature': temp,
    'bop_moisture': bop_moisture,
    'bop_percent': bop_percent,
    'mon_moisture': mon_moisture,
    'mon_percent': mon_percent,
    'humidity' : humidity
})

# Save it to the web server's folder
with open('/home/pi/www/sandygrayplants/roomstatus.json', 'w') as outfile:
    json.dump(jsondata, outfile)
