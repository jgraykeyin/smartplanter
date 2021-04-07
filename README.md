# Pico RP2040 SmartPlanter

The RP2040 runs main.py which controls several sensors using the main.py program :
* Humidity & Temperature (DHT22)
* Two moisture sensor that are each embedded in plant soil

## Output ##
* Data is displayed on a 16x2 character LCD screen connected to the Pico
* Data is also sent to a Raspberry Pi using UART communication
* Raspberry pi runs a cronjob to check the data every 5 minutes and saves to a json file using roomstatus.py
* Website then fetches json file and displays the data online using app.js
