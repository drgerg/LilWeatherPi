#!/usr/bin/env python3
#
#   outMainDATA.py - A working file to build the data logging parts of outMain.py.

#     Copyright (c) 2019,2020 - Gregory Allen Sanders.

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import datetime,time,argparse,bme280,os,subprocess,logging,signal,sys,statistics,mysql.connector,configparser,pickle,Adafruit_DHT
from time import sleep
import RPi.GPIO as GPIO
from mysql.connector import MySQLConnection, Error

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 24
timeVal = 0
rstart = 0
accResults = []
pklData = []
tableData = []
numBadPings = 0
pressure = 0
outTemp = 0
outHumidity = 0
extraTemp1 = 0 # CPU temp
#
## DHT22 SENSOR DATA GRABBER FUNCTION
#
def dht22Data():
    humidity = None
    tempC = None
    while humidity == None or tempC == None:
        humidity, tempC = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        time.sleep(3)
    return humidity, tempC
#    
##      Setup for Sensor Data Logging.  Each parameter gets logged for a minute
##      then we run some stats, and share the output of that with the next step.
#
def datagrabber():
    global timeVal
    start = time.time()
    accPress = []
    accTemp = []
    accHum = []

    while time.time() - start < 57:                       ## The plan here is to run this for a minute,
                                                          ## then get the median values to return.
        outTemp2,pressure = bme()                         ## ACQUIRE alternateTEMP,PRES
        outHumidity,outTemp = dht22Data()                 ## ACQUIRE humidity and temp from DHT22

        accPress.append(pressure)
        accTemp.append(outTemp)
        accHum.append(outHumidity)

    loopTimer = time.time() - start
    logger.debug('time.time() - start = ' + str(loopTimer))
    pressure = statistics.median(accPress)                ## Get the middle value in the list of values
    outTemp = statistics.median(accTemp)                  ## accumulated over the last 60 seconds
    outHumidity = statistics.median(accHum)

    logger.debug('outMainData.py datagrabber() has run and is returning values to mydb().')
    return pressure,outTemp,outHumidity,timeVal
#
##
# 
#
# A calculation to approximate the dewpoint when humidity is over 50%
# Td = T - ((100 - RH)/5.)
#   
#   THESE ARE THE FINAL VARIABLES WE WANT TO PASS TO THE DATABASE
#   
#   pressure
#   outTemp
#   outHumidity
#   extraTemp1 = CPU temp
#   
#   I'm going to use the prefix 's_' to indicate a 'samples' list variable.  So 'outTemp' becomes 's_outTemp'.
#   's_outTemp' contains the list of values accumulated during this one-shot gathering episode.
#
## GRAB SENSOR DATA FROM THE BME280 MODULE
#
def bme():  #####  7/10/2021 - aDDED DHT22 SENSOR FOR TEMP/HUMIDITY.  LOOK FOR dht22Data() function.

    s_outTemp = []
    s_pressure = []
    tstart = time.time()

    while time.time() - tstart < 2:
        tempC,pres = bme280.readBME280All()
        s_outTemp.append(tempC)
        s_pressure.append(pres)
    outTemp = statistics.mean(s_outTemp)
    pressure = statistics.mean(s_pressure)

    return outTemp,pressure
#
## START WRITE-TO-DATABASE FUNCTION
# Be aware that because we are using WiFi to connect to the network, we have to make arrangements in case
# the connection drops.  It happens.  So we are getting sensor data, putting it in a list, checking for a .pkl file
# which will exist if the connection test failed last time around, appending our new data to the data from that .pkl file,
# ping the SQL server machine, if good: write rows of data from our list and delete the .pkl file. If not good: dump the 
# appended list to the .pkl file (which overwrites it if it existed) and then swing back
# around to do it all again.
#
def mydb():
    global pklData,numBadPings
    # Get current values from all the sensors.
    pressure,outTemp,outHumidity,timeVal = datagrabber()
    # Get the vent fan RPM from the pickle file.
    try:
        fan1 = pickle.load(open(OMDHome + '/fanSpd.pkl', 'rb'))
    except EOFError:
        logger.debug("Encountered an empty .pkl file.  Moving on without it.")
        fan1 = 0
        pass
    # Get the CPU temperature from the system.
    cpuT = cpuTemp()[1]
    # Now make sure all the variables are of the right type.  Take no chances.
    prs = float(pressure)
    otmp = float(outTemp)
    ohmd = float(outHumidity)

    dtNow = int(time.time())
    dataTable = [dtNow,prs,otmp,ohmd,cpuT]  # Put all the readings into a list.
    if os.path.exists(OMDHome + '/allData.pkl'):            ## This .pkl file will exist if the upcoming ping test failed last time around.
        pklData = pickle.load(open(OMDHome + '/allData.pkl', 'rb'))
    pklData.append(dataTable)                               ## Merge the recent data with the .pkl file data just in case we are still offline
    logger.debug('dataTable was appended to pklData')
    DBhost=config.get('mySQL','Address')                    # get the mySQL login data from our config file.
    DBuser=config.get('mySQL','User')
    DBpasswd=config.get('mySQL','Password')
    DBdatabase=config.get('mySQL','Database')
    DBtable=config.get('mySQL','Table1')
    # Don't stop now . . . keep going!!!
    ## Check to see if we can ping the machine mySQL is running on
    pingRes = subprocess.call(['/bin/ping', '-c', '1', DBhost], stdout=subprocess.DEVNULL)  ## Ping test to make sure the SQL machine is there.
    logger.debug("Ping for server returned: " + str(pingRes))
    if pingRes == 0:                                        # We are connected.  Move ahead.  If not, don't do any of this stuff.
        if numBadPings > 0:
            logger.info("Connection to SQL server machine restored.")
        numBadPings = 0                                     # Prep the data, and send it to the SQL machine.
        for row in pklData:                                 # Normally there will only be one row. UNLESS the network was down, 
            dtNow = row[0]                                  # in which case there can be many.
            prs = row[1]
            otmp = row[2]
            ohmd = row[3]
            # xohmd = row[7]
            cpuT = row[8]

            try:
                # prepare the database connector 
                mydb = mysql.connector.connect(
                    host=DBhost,
                    user=DBuser,
                    passwd=DBpasswd,
                    database=DBdatabase
                )
                cursor = mydb.cursor()                      # Attempt a connection with the remote database. If it is not there, 
                cursor.execute("select database();")        # an exception will be logged and we will save our data for the 
                record = cursor.fetchone()                  # next go-round.
                logger.debug("Got the database: " + str(record))
                addRecord = ('INSERT INTO ' + DBdatabase + '.' + DBtable + '' \
                    ' (dateTime,pressure,outTemp,outHumidity,cpuTemp)' \
                    ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
                addData = (dtNow,prs,otmp,ohmd,cpuT)
                logger.debug(addRecord %addData)
                cursor.execute(addRecord,addData)
                cursor.execute("SELECT * FROM " + DBdatabase + '.' + DBtable + " where id=(select max(id) from " + DBdatabase + '.' + DBtable + ")")
                record = cursor.fetchone()
                logger.debug('The last record contains: ' + str(record))
                mydb.commit()
                cursor.close()
                mydb.close()
                pklData = []                                ## RESET pklData to an empty list.
                if timeVal > 0:
                    elapsedTime = time.time() - timeVal
                    # logger.info('From last Rain tick check to writing the database record was ' + str(elapsedTime) + ' seconds.')
                if os.path.exists(OMDHome + '/allData.pkl'):
                    os.remove(OMDHome + '/allData.pkl')
                    logger.debug("allData.pkl Pickle file erased.")
            except Exception:
                logger.info('Unable to connect with mySQL database.  Details to follow: ', exc_info=True)
                pass
            funNStr = sys._getframe().f_code.co_name
            logger.debug("Finished the " + funNStr + " function")
    else:                                                           # We are NOT CONNECTED.  Save our readings to a .pkl file
        logger.info("Ping test for SQL server machine failed.")
        numBadPings += 1
        pickle.dump(pklData, open(OMDHome + '/allData.pkl', 'wb+'), pickle.HIGHEST_PROTOCOL)
        logger.debug("allData.pkl updated.")
        logger.info ("Number of bad pings is: " + str(numBadPings) + ".")
        if numBadPings >= 3:
            logger.info("Too many bad pings.  Setting up to reboot.")
            os.mknod(OMDHome + '/rebootItNow')
#
##  END OF WRITE-TO-DATABASE FUNCTION
#

#
## Grab the CPU temperature while you're at it.
#
def cpuTemp():
# Return CPU temperature in C and F
    ct = os.popen('vcgencmd measure_temp').readline()
    cpuRtn = ct.replace("temp=","").replace("'C\n","")
    cpuT1=float(cpuRtn)
    cpuT2=float(9/5 * cpuT1 + 32.00)
    return cpuT1,cpuT2
#
## = = = = = = = =  END OF WEATHER CODE - START OF ERROR HANDLING, LOGGING AND WRAPUP CODE  = = = = = = = = =
#
def SignalHandler(signal, frame):
        if signal == 2:
            sigStr = 'CTRL-C'
            logger.info('* * * ' + sigStr + ' caught. * * * ')
        print("SignalHandler invoked")
        logger.info("Cleaning up")
        GPIO.cleanup()
        logger.info("Shutting down gracefully")
        logger.debug("Wrote to log in SignalHandler")
        logger.info("Finished SignalHandler")
        logger.info("That's all folks.  Goodbye")
        logger.info(" - - - - outMainDATA.py DATA LOGGING STOPPED INTENTIONALLY - - - - ")
        sys.exit(0)

if __name__ == "__main__":
    #
    ## Arg parsing moved down here so we can use functions from this file as a module without conflicting the commandline arguments.
    #
    parserOMD = argparse.ArgumentParser()
    parserOMD.add_argument("-d", "--debug", help="Turn on debugging output to log file.", action="store_true")
    OMDHome = os.getcwd()
    logger = logging.getLogger(__name__)
    #
    config = configparser.RawConfigParser()
    config.read(OMDHome + '/out.conf')
    #
    argsOMD = parserOMD.parse_args()

    if argsOMD.debug:
        import traceback
        logging.basicConfig(filename=OMDHome + '/outMainDATA.log', format='[%(name)s]:%(levelname)s: %(message)s. - %(asctime)s', datefmt='%D %H:%M:%S', level=logging.DEBUG)
        logging.info("Debugging output enabled")
    else:
        logging.basicConfig(filename=OMDHome + '/outMainDATA.log', format='%(asctime)s - %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', level=logging.INFO)
    #
    logger.info(" - - - - outMainDATA.py DATA LOGGING STARTED - - - - ")
    logger.info("  INITIAL CONFIGURATION COMPLETE  ")
    logger.info("'HOME' path is: " + OMDHome)
    #
    ## END Args parsing and logging setup.
    #
    import traceback
    try:
        signal.signal(signal.SIGINT, SignalHandler)  ## This one catches CTRL-C from the local keyboard
        signal.signal(signal.SIGTERM, SignalHandler) ## This one catches the Terminate signal from the system
        logger.debug(" Top of try")
        while True:
            mydb()
        pass

        logger.debug("Bottom of try")
#            logger.flush()
    except Exception:
        logger.info("Exception caught at bottom of try.", exc_info=True)
        error = traceback.print_exc()
        logger.info(error)
        logger.info("That's all folks.  Goodbye")
        logger.info(" - - - - outMainDATA.py DATA LOGGING STOPPED BY EXCEPTION - - - - ")
