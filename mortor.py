import time
import sys
import ibmiotf.application
import ibmiotf.device
import requests
import random
#Provide your IBM Watson Device Credentials
organization = "y45n29"
deviceType = "Raspberry.pi"
deviceId = "123456"
authMethod = "token"
authToken = "12345678"
def myCommandCallback(cmd):
        print("command recived:%s"%cmd.data)#commands
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='mortoron':
                print("mortor on")
        elif i=='mortor,off':
                print("mortor off")

try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)#.............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        hum=random.randint(10,40)
        #print(hum)
        temp =random.randint(30,80)
        soil=random.radint(10,60)
        #Send Temperature & Humidity to IBM Watson
        data = {'Temperature' : temp, 'Humidity': hum,'soilmosture':soil}
        #print (data)
        def myOnPublishCallback():
            print("Published Temperature = %s C" % temp, "Humidity = %s %%" % hum,"soilmoisture=%s%"%soil,"to IBM Watson")

        success=deviceCli.publishEvent("weather", "josn", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback
        r=requests.get('https://www.fast2sms.com/dev/bulk?authorization=qyRwp3eZ2olzuQPOB1CrgaNiFhSDjtVXdsM5cIGWmEb0Kv9LTHhTvLP5WRMF6cBNCQ3lYaG2x4gnKdI0&sender_id=FSTSMS&message=This is test message&language=english&route=p&numbers=9492261794')
        if temp>=70:
                print(r.status_code)
#disconnect
deviceCli.disconnect()

