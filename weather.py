from datetime import datetime
from sense_hat import SenseHat
from time import sleep
from threading import Thread
import subprocess
import os
##### Innstillinger ##### temp_calibrated = temp - ((cpu_temp - temp)/FACTOR)  - temp_calibrated = temp - ((cpu_temp - temp)/5.466)

# #!/usr/bin/python
# from sense_hat import SenseHat
# import time
# while True:
    # ap = SenseHat()
    # temp = ap.get_temperature()
    # print("Temp: %s C" % temp)               # Show temp on console

    # ap.set_rotation(180)        # Set LED matrix to scroll from right to left

    # ap.show_message("%.1f C" % temp, scroll_speed=0.10, text_colour=[0, 255, 0])
    # time.sleep(10)


FILENAME = "test"
WRITE_FREQUENCY = 1
TEMP_H=True
TEMP_P=True
HUMIDITY=True
PRESSURE=True
DELAY=30

##### Funksjoner #####

def file_setup(filename):
	header =[]
	if TEMP_H:
		header.append("temp_h")
	if TEMP_P:
		header.append("temp_p")
	if HUMIDITY:
		header.append("humidity")
	if PRESSURE:
		header.append("pressure")
	header.append("timestamp")

	with open(filename,"w") as f:
		f.write(",".join(str(value) for value in header)+ "\n")

def log_data():
	output_string = ",".join(str(value) for value in sense_data)
	batch_data.append(output_string)


def displaytemp():
	cpu = float(getCPUtemperature())
	temp_h = sense.get_temperature_from_humidity()
	temp_h_c = temp_h - ((cpu) / 5.466)
	temp_h_cc = round(temp_h_c, 1)
	return str(temp_h_cc)
	
	
def displayhumidity():
	humidity = sense.get_humidity()
	humidity = round(humidity, 1)
	return str(humidity)
	
	
def getCPUtemperature():
	res = os.popen('vcgencmd measure_temp').readline()
	return(res.replace("temp=","").replace("'C\n",""))

def get_sense_data():
	sense_data=[]

	# temp_c = sense.get_temperature()
	# humidity = sense.get_humidity()
	# pressure_mb = sense.get_pressure()
	# cpu_temp = subprocess.check_output("vcgencmd measure_temp", shell=True)
	# array = cpu_temp.split("=")
	# array2 = array[1].split("'")

	# cpu_tempc = float(array2[0])
	# cpu_tempc = float("{0:.2f}".format(cpu_tempc))
	# cpu_tempf = float(array2[0]) * 9.0 / 5.0 + 32.0
	# cpu_tempf = float("{0:.2f}".format(cpu_tempf))

	# temp_calibrated_c = temp_c - ((cpu_tempc - temp_c)/5.466)

	# # Format the data
	# temp_f = temp_calibrated_c * 9.0 / 5.0 + 32.0
	# temp_f = float("{0:.2f}".format(temp_f))
	# temp_calibrated_c = float("{0:.2f}".format(temp_calibrated_c))
	# humidity = float("{0:.2f}".format(humidity))
	# pressure_in = 0.0295301*(pressure_mb)
	# pressure_in = float("{0:.2f}".format(pressure_in))
	# pressure_mb = float("{0:.2f}".format(pressure_mb))
	#temp_calibrated = temp - ((vcgencmd measure_temp)/5.466)
	
	def getCPUtemperature():
		res = os.popen('vcgencmd measure_temp').readline()
		return(res.replace("temp=","").replace("'C\n",""))

	cpu = float(getCPUtemperature())
	
	if TEMP_H:
		temp_h = sense.get_temperature_from_humidity()
		temp_h_c = temp_h - ((cpu) / 5.466)
		temp_h_cc = round(temp_h_c, 1)
		sense_data.append(temp_h_cc)

	if TEMP_P:
		temp_f = sense.get_temperature_from_pressure()
		temp_f_c = temp_f - ((cpu) / 5.466)
		temp_f_c = round(temp_f_c, 1)
		sense_data.append(temp_f_c)

	if HUMIDITY:
		humidity = sense.get_humidity()
		humidity = round(humidity, 1)
		sense_data.append(humidity)

	if PRESSURE:
		pressure = sense.get_pressure()
		pressure = round(pressure, 1) 
		sense_data.append(pressure)

	sense_data.append(datetime.now())



	return sense_data


def timed_log():
	while True:
		log_data()
		sleep(DELAY)




##### Programm #####
sense = SenseHat()
batch_data= []

if FILENAME == "":
	filename = "SenseLog-"+str(datetime.now())+".csv"
else:
	filename = FILENAME+"-"+str(datetime.now())+".csv"

file_setup(filename)

if DELAY > 0:
	sense_data = get_sense_data()
	Thread(target= timed_log).start()

while True:
	sense_data = get_sense_data()
	if DELAY == 0:
		log_data()

	if len(batch_data) >= WRITE_FREQUENCY:
		print("Writing to file..")
		with open(filename,"a") as f:
			for line in batch_data:
				f.write(line + "\n")
			batch_data = []
			
	sense.set_rotation(180)        # Set LED matrix to scroll from right to left
	sense.show_message(displaytemp(), scroll_speed=0.10, text_colour=[0, 255, 0])
	sense.show_message(displayhumidity(), scroll_speed=0.10, text_colour=[0, 0, 255])
	
	