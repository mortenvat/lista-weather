from datetime import datetime
from sense_hat import SenseHat
from time import sleep
from threading import Thread
import os
import plotly.plotly as py
from plotly.graph_objs import *
import time

##### Innstillinger ##### temp_calibrated = temp - ((cpu_temp - temp)/FACTOR)  - temp_calibrated = temp - ((cpu_temp - temp)/5.466)


FILENAME = "test.csv" ##########################FILNAVN#######################
WRITE_FREQUENCY = 1 #hvor mye data den skal samle på før den legger det til i csv filen, høy verdi vil øke levetid på SD kort
TEMP_H=True			#slå av rapportering av enkelte sensorer?
TEMP_P=True
HUMIDITY=True
PRESSURE=True
DELAY=1 # hvor mange sekund det skal ta mellom hver loggføring

##### Funksjoner #####

def file_setup(filename):  # overskrift for kolonner i csv fil
	header =[]
	if TEMP_H:
		header.append("temp1")
	if TEMP_P:
		header.append("temp2")
	if HUMIDITY:
		header.append("luftfuktighet")
	if PRESSURE:
		header.append("lufttrykk")
	header.append("tidspunkt")

	with open(filename,"w") as f:
		f.write(",".join(str(value) for value in header)+ "\n")

def log_data():
	output_string = ",".join(str(value) for value in sense_data)
	batch_data.append(output_string)


def displaytemp(): #vis temperatur i LED
	cpu = float(getCPUtemperature())
	temp_h = sense.get_temperature_from_humidity()
	temp_h_c = temp_h - ((cpu) / 5.466)  # formel for korreksjon av temperaturmåler ##### 0.0071*temp_h*temp_h+0.86*temp_h-10.0 ##### temp - ((cputemp - temp) / 2)
	temp_h_cc = round(temp_h_c, 1)  #formater utdata til ën desimal
	return str(temp_h_cc)
	
	
def displayhumidity():  #vis fuktighetprosent i LED
	humidity = sense.get_humidity()
	humidity = round(humidity, 1)
	return str(humidity)
	
def displaypressure(): # vis lufttrykk i LED
	pressure = sense.get_pressure()
	pressure = round(pressure, 1)
	pressure = int(pressure)
	return str(pressure)
	
	
def getCPUtemperature(): #skaff CPU temperatur
	res = os.popen('vcgencmd measure_temp').readline() 
	return(res.replace("temp=","").replace("'C\n",""))

	sense_data=[]
def get_sense_data(): # selve innskaffelsen av sensor data

	
	def getCPUtemperature():
		res = os.popen('vcgencmd measure_temp').readline()
		return(res.replace("temp=","").replace("'C\n","")) # gjør utdata til rent desimaltall istedet for tekst 

	cpu = float(getCPUtemperature()) #gjør info til tall 
	
	if TEMP_H:		#temperatur fra sensor1
		temp_h = sense.get_temperature_from_humidity()
		temp_h_c = temp_h - ((cpu) / 5.466)# formel for korreksjon av temperaturmåler 
		temp_h_cc = round(temp_h_c, 1) #formater utdata til ën desimal
		sense_data.append(temp_h_cc)

	if TEMP_P:		#temperatur fra sensor2
		temp_f = sense.get_temperature_from_pressure()
		temp_f_c = temp_f - ((cpu) / 5.466)# formel for korreksjon av temperaturmåler 
		temp_f_c = round(temp_f_c, 1) #formater utdata til rent desimaltall
		sense_data.append(temp_f_c)

	if HUMIDITY:	#fuktighetprosent
		humidity = sense.get_humidity() # skaff info luftfuktighet
		humidity = round(humidity, 1) #formater utdata til rent desimaltall
		sense_data.append(humidity) 

	if PRESSURE:	#lufttrykk i mBar
		pressure = sense.get_pressure() # skaff info lufttrykk
		pressure = round(pressure, 1) #formater utdata til rent desimaltall
		sense_data.append(pressure)

	sense_data.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) # legg til tidspunkt 



	return sense_data


def timed_log(): #forsinkelse i logg
	while True:
		log_data()
		sleep(DELAY)


##### Programm #####
sense = SenseHat()
batch_data= []

if FILENAME == "":		#hvis ingen filnavn er spesifisert, legg til SenseLog+dato i filnavnet
	filename = "SenseLog-"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+".csv" 
else:					#hvis filnavn er spesifisert, legg til dato inni filnavnet
	filename = FILENAME #+"-"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+".csv"

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
	sense.show_message(displaytemp() + "c", scroll_speed=0.06, text_colour=[0, 255, 0]) #innstillinger for LED
	sense.show_message(displayhumidity() + "%", scroll_speed=0.06, text_colour=[0, 0, 255])#innstillinger for LED
	sense.show_message(displaypressure() + "mBar", scroll_speed=0.06, text_colour=[255,0,122])
	
	