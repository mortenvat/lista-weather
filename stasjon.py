##### Libraries #####
from sense_hat import SenseHat
from datetime import datetime 
from time import sleep
from threading import Thread


#### logging #####

FILENAME = "sense"
WRITE_FREQUENCY = 50
DELAY=600


#### funk ####
def file_setup(filename):
	header =("temp_h","temp_p","fuktighet","lufttrykk","timestamp")
	

	with open(filename,"w") as f:
                f.write(",".join(str(value) for value in header)+ "\n")
		
def log_data():
	output_string = ",".join(str(value) for value in sense_data)
        batch_data.append(output_string)

def get_sense_data():
  sense_data=[]

  sense_data.append(sense.get_temperature_from_humidity())
  sense_data.append(sense.get_temperature_from_pressure())
  sense_data.append(sense.get_humidity())
  sense_data.append(sense.get_pressure())
  
  
sense_data.append(datetime.now())
return sense_data
	
def timed_log():
	while True():
		log_data()
		sleep(DELAY)

#### prog ####
sense = SenseHat()

batch_data=[]
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
		
	
	if len(batch_data) >= WRITE_FREQUENCY
		print ("writing to file..")
		with open(filename,"a" as f:
			for line in batch_data:
				f.write(line + "\n")
				
	print(sense_data)
