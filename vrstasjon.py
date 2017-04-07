from datetime import datetime
from sense_hat import SenseHat
from time import sleep
from threading import Thread
import os
import time
import datetime
#bfadvfadshubogvhu
##### Innstillinger ##### temp_calibrated = temp - ((cpu_temp - temp)/FACTOR)  - temp_calibrated = temp - ((cpu_temp - temp)/5.466)


FILENAME = "testklasserom.csv" ##########################FILNAVN#######################
WRITE_FREQUENCY = 1 #hvor mye data den skal samle p fr den legger det til i csv filen, hy verdi vil ke levetid p SD kort
TEMP_H=True #sl av rapportering av enkelte sensorer?
TEMP_P=True
HUMIDITY=True
PRESSURE=False
DELAY=50 # hvor mange sekund det skal ta mellom hver loggfring, husk  endre i "def plotlywrite() > sleep(XXX)"


##### Funksjoner #####
sense = SenseHat()
def file_setup(filename):  # overskrift for kolonner i csv fil
	header =[]
	if TEMP_H:
		header.append("temp1")
	if TEMP_P:
		header.append("temp2")
	if HUMIDITY:
		header.append("fuktighet")
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
	temp_h = sense.get_temperature_from_pressure()
	temp_h_c = temp_h - 3.5 - ((cpu) / 5.466)  # formel for korreksjon av temperaturmler 
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

def get_sense_data(): # selve innskaffelsen av sensor data
	sense_data=[]

	
	def getCPUtemperature():
		res = os.popen('vcgencmd measure_temp').readline()
		return(res.replace("temp=","").replace("'C\n","")) # gjr utdata til desimaltall istedet for tekst 

	cpu = float(getCPUtemperature()) #gjr info til tall 
	
	if TEMP_H:		#temperatur fra sensor1
		temp_h = sense.get_temperature_from_humidity()
		temp_h_c = temp_h - 2 - ((cpu) / 5.466)# formel for korreksjon av temperaturmler 
		temp_h_cc = round(temp_h_c, 1) #formater utdata til én desimal
		sense_data.append(temp_h_cc)

	if TEMP_P:		#temperatur fra sensor2
		temp_f = sense.get_temperature_from_pressure()
		temp_f_c = temp_f - 3.5 - ((cpu) / 5.466)# formel for korreksjon av temperaturmler 
		temp_f_c = round(temp_f_c, 1) #formater utdata til én desimal
		sense_data.append(temp_f_c)

	if HUMIDITY:	#fuktighetprosent
		humidity = sense.get_humidity() # skaff info luftfuktighet
		humidity = round(humidity, 1) #formater utdata til én desimal
		sense_data.append(humidity) 

	if PRESSURE:	#lufttrykk i mBar
		pressure = sense.get_pressure() # skaff info lufttrykk
		pressure = round(pressure, 1) #formater utdata til én desimal
		sense_data.append(pressure)

	
	sense_data.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) # legg til tidspunkt
	



	return sense_data


def timed_log():
	while True:
		log_data()
		sleep(DELAY)



####plotly########
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
stream_tokens = tls.get_credentials_file()['stream_ids']
token_1 = stream_tokens[-1]   
token_2 = stream_tokens[-2]
token_3 = stream_tokens[-3]
print (token_1)
print (token_2)
print (token_3)
stream_id1 = dict(token=token_1, maxpoints=60)
stream_id2 = dict(token=token_2, maxpoints=60)
stream_id3 = dict(token=token_3, maxpoints=60)



trace1 = go.Scatter(x=[], y=[], stream=stream_id1, name='temp', mode = 'lines')
trace2 = go.Scatter(x=[], y=[], stream=stream_id2,name='fuktighet', mode = 'lines', marker=dict(color='rgb(148, 103, 189'))
trace3 = go.Scatter(x=[], y=[], stream=stream_id3, yaxis='y2', name='trykk', mode = 'lines', marker=dict(color='rgb(255, 0, 0'))

data = [trace1, trace2, trace3]
layout = go.Layout(
    title='vrstasjon',
    yaxis=dict(
	title='celsius' + ' og' + ' %' + ' luftfuktighet'
    ),
    yaxis2=dict(
	title='mBar',
	titlefont=dict(
	    color='rgb(148, 103, 189)'
	),
	tickfont=dict(
	    color='rgb(148, 103, 189)'
	),
	overlaying='y',
	side='right'
		
		),
)

fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='vrstasjon')
s_1 = py.Stream(stream_id=token_1)
s_2 = py.Stream(stream_id=token_2)
s_3 = py.Stream(stream_id=token_3)
s_1.open()
s_2.open()
s_3.open()	


def show(): #bruk raspberry LED display
	while True:
		sense.set_rotation(180) #sett orienteringen til raspberry LED
		sense.show_message(displaytemp() + "c", scroll_speed=0.06, text_colour=[0, 255, 0]) #innstillinger for LED
		sense.show_message(displayhumidity() + "%", scroll_speed=0.06, text_colour=[0, 0, 255])#innstillinger for LED
		#sense.show_message(displaypressure() + "mBar", scroll_speed=0.06, text_colour=[255,0,122])
		sleep(0)
		continue
	
		
def plotlywrite(): #skriv til plot.ly url 
	while True:
		tid = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
		temperatur = displaytemp()
		luftfuktighet = displayhumidity()
		lufttrykk = displaypressure()
		s_1.write(dict(x=tid,y=temperatur))
		s_2.write(dict(x=tid,y=luftfuktighet))
		s_3.write(dict(x=tid,y=lufttrykk))
		print(temperatur,luftfuktighet,lufttrykk)
		sleep(50)
		


Thread(target= show).start()  #start raspberry led
Thread(target= plotlywrite).start() # start skriving til plotly
sense = SenseHat()
batch_data= []

if FILENAME == "":		#hvis ingen filnavn er spesifisert, legg til SenseLog+dato i filnavnet
	filename = "SenseLog-"+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+".csv" 
	file_setup(filename)
else:

	filename = FILENAME+"-"+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+".csv"		#hvis filnavn er spesifisert, legg til dato inni filnavnet
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
