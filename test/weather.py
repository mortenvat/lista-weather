from datetime import datetime
from sense_hat import SenseHat
from time import sleep
from threading import Thread
import os
#bfadvfadshubogvhu
##### Innstillinger ##### temp_calibrated = temp - ((cpu_temp - temp)/FACTOR)  - temp_calibrated = temp - ((cpu_temp - temp)/5.466)


FILENAME = "testklasserom.csv" ##########################FILNAVN#######################
WRITE_FREQUENCY = 1 #hvor mye data den skal samle på før den legger det til i csv filen, høy verdi vil øke levetid på SD kort
TEMP_H=True

#slå av rapportering av enkelte sensorer?
TEMP_P=True
HUMIDITY=True
PRESSURE=False
DELAY=30 # hvor mange sekund det skal ta mellom hver loggføring


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
	temp_h_c = temp_h - 4 - ((cpu) / 5.466)  # formel for korreksjon av temperaturmåler 
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
		return(res.replace("temp=","").replace("'C\n","")) # gjør utdata til rent desimaltall istedet for tekst 

	cpu = float(getCPUtemperature()) #gjør info til tall 
	
	if TEMP_H:		#temperatur fra sensor1
		temp_h = sense.get_temperature_from_humidity()
		temp_h_c = temp_h - 4 - ((cpu) / 5.466)# formel for korreksjon av temperaturmåler 
		temp_h_cc = round(temp_h_c, 1) #formater utdata til ën desimal
		sense_data.append(temp_h_cc)

	if TEMP_P:		#temperatur fra sensor2
		temp_f = sense.get_temperature_from_pressure()
		temp_f_c = temp_f - 4 - ((cpu) / 5.466)# formel for korreksjon av temperaturmåler 
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

        
	sense_data.append(datetime.now().strftime("%Y-%m-%d %H:%M")) # legg til tidspunkt
	



	return sense_data


def timed_log(): #forsinkelse i logg
	while True:
		log_data()
		sleep(DELAY)



####plotly########
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import numpy as np 
stream_tokens = tls.get_credentials_file()['stream_ids']
token_1 = stream_tokens[-1]   # I'm getting my stream tokens from the end to ensure I'm not reusing tokens
token_2 = stream_tokens[-2]
token_3 = stream_tokens[-3]
print (token_1)
print (token_2)
print (token_3)
stream_id1 = dict(token=token_1, maxpoints=60)
stream_id2 = dict(token=token_2, maxpoints=60)
stream_id3 = dict(token=token_3, maxpoints=60)


trace1 = go.Scatter(x=[], y=[], stream=stream_id1, name='temp')
trace2 = go.Scatter(x=[], y=[], stream=stream_id2, name='fuktighet', mode = 'lines+markers', marker=dict(color='rgb(148, 103, 189)'))
trace3 = go.Scatter(x=[], y=[], stream=stream_id3, yaxis='y2', name='trykk', mode = 'lines+markers', marker=dict(color='rgb(255, 0, 0'))

data = [trace1, trace2, trace3]
layout = go.Layout(
    title='weather station',
    yaxis=dict(
        title='celsius'
    ),
    yaxis2=dict(
        title='%',
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
plot_url = py.plot(fig, filename='multple-trace-axes-streaming')
s_1 = py.Stream(stream_id=token_1)
s_2 = py.Stream(stream_id=token_2)
s_3 = py.Stream(stream_id=token_3)
s_1.open()
s_2.open()
s_3.open()	
sense = SenseHat()
batch_data= []
class message(Thread):
	Thread.show(self)
	self.daemon = True 
	self.start()
	def show(self):
		sense.set_rotation(180)        #sett orienteringen til raspberry LED
		sense.show_message(displaytemp() + "c", scroll_speed=0.06, text_colour=[0, 255, 0]) #innstillinger for LED
		sense.show_message(displayhumidity() + "%", scroll_speed=0.06, text_colour=[0, 0, 255])#innstillinger for LED
		#sense.show_message(displaypressure() + "mBar", scroll_speed=0.06, text_colour=[255,0,122])
while True:
	if DELAY == 0:
		tid = datetime.now().strftime('%Y-%m-%d %H:%M')
		y1 = displaytemp()
		y2 = displayhumidity()
		y3 = displaypressure()
		print (y1,y2,y3)
		s_1.write(dict(x=tid,y=y1))
		s_2.write(dict(x=tid,y=y2))
		s_3.write(dict(x=tid,y=y3))
	
	#######plotly#########
	##### Programm #####

	if FILENAME == "":		#hvis ingen filnavn er spesifisert, legg til SenseLog+dato i filnavnet
		filename = "SenseLog-"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+".csv" 
		file_setup(filename)
		else
			filename = FILENAME#+"-"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+".csv"		#hvis filnavn er spesifisert, legg til dato inni filnavnet
			file_setup(filename)


	

	elif DELAY > 0:
		sense_data = get_sense_data()
		Thread(target= timed_log).start()


	sense_data = get_sense_data()
	elif DELAY == 0:
		log_data()
	elif len(batch_data) >= WRITE_FREQUENCY:
		print("Writing to file..")
		with open(filename,"a") as f:
			for line in batch_data:
				f.write(line + "\n")
			batch_data = []


	message()
	continue




