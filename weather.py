from datetime import datetime
from sense_hat import SenseHat
from time import sleep
from threading import Thread
import subprocess
import os
##### Innstillinger ##### temp_calibrated = temp - ((cpu_temp - temp)/FACTOR)  - temp_calibrated = temp - ((cpu_temp - temp)/5.466)


FILENAME = "test" #filnavn
WRITE_FREQUENCY = 1 #hvor mye data den skal samle på før den legger det til i csv filen, høy verdi vil øke levetid på SD kort
TEMP_H=True			#slå av rapportering av enkelte sensorer?
TEMP_P=True
HUMIDITY=True
PRESSURE=True
DELAY=30 # hvor mange sekund det skal ta mellom hver loggføring

##### Funksjoner #####

def file_setup(filename):  # overskrift for kolonner i csv fil
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


def displaytemp(): #vis temperatur i LED
	cpu = float(getCPUtemperature())
	temp_h = sense.get_temperature_from_humidity()
	temp_h_c = temp_h - ((cpu) / 5.466) 
	temp_h_cc = round(temp_h_c, 1)
	return str(temp_h_cc)
	
	
def displayhumidity():  #vis fuktighetprosent i LED
	humidity = sense.get_humidity()
	humidity = round(humidity, 1)
	return str(humidity)
	
	
def getCPUtemperature(): #skaff CPU temperatur og formater utdata til rent desimaltall
	res = os.popen('vcgencmd measure_temp').readline()
	return(res.replace("temp=","").replace("'C\n",""))

def get_sense_data(): # selve innskaffelsen av sensor data
	sense_data=[]

	
	def getCPUtemperature():
		res = os.popen('vcgencmd measure_temp').readline()
		return(res.replace("temp=","").replace("'C\n",""))

	cpu = float(getCPUtemperature())
	
	if TEMP_H:		#temperatur fra sensor1
		temp_h = sense.get_temperature_from_humidity()
		temp_h_c = temp_h - ((cpu) / 5.466)
		temp_h_cc = round(temp_h_c, 1)
		sense_data.append(temp_h_cc)

	if TEMP_P:		#temperatur fra sensor2
		temp_f = sense.get_temperature_from_pressure()
		temp_f_c = temp_f - ((cpu) / 5.466)
		temp_f_c = round(temp_f_c, 1)
		sense_data.append(temp_f_c)

	if HUMIDITY:	#fuktighetprosent
		humidity = sense.get_humidity()
		humidity = round(humidity, 1)
		sense_data.append(humidity)

	if PRESSURE:	#lufttrykk i mBar
		pressure = sense.get_pressure()
		pressure = round(pressure, 1) 
		sense_data.append(pressure)

	sense_data.append(datetime.now())



	return sense_data


def timed_log(): #forsinkelse i logg
	while True:
		log_data()
		sleep(DELAY)




##### Programm #####
sense = SenseHat()
batch_data= []

if FILENAME == "":		#hvis ingen filnavn er spesifisert, legg til SenseLog+dato i filnavnet
	filename = "SenseLog-"+str(datetime.now())+".csv" 
else:					#hvis filnavn er spesifisert, legg til dato inni filnavnet
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
			
	sense.set_rotation(180)        #sett orienteringen til raspberry LED
	sense.show_message(displaytemp(), scroll_speed=0.10, text_colour=[0, 255, 0])
	sense.show_message(displayhumidity(), scroll_speed=0.10, text_colour=[0, 0, 255])
	
	