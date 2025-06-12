import RPi.GPIO as GPIO     # Importing libraries used in program
import time
from datetime import datetime
import LCD1602 as LCD
import keypadfunc as key    # do key.shiftkeypad
import RFIDTest as RFID
import DHT11
import PCF8591 as ADC
import urllib.request
from flask import Flask
from flask import send_file
from picamera import PiCamera
import serial

API_KEY = "FDQ2OAPC0L7M0G17"    # Write API key for ThingSpeak channel
Ch_id = "2216444"               # Channel ID of ThingSpeak channel
field_no = 1
readings = 1
elem_no = 0
values = []
values1 = []
mycamera = PiCamera()           # Setting Raspberry Pi camera
mycamera.resolution = (1280,720)    # Setting resolution of Raspberry Pi camera

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)          #Set to BCM mode

GREEN = 17             #Setting GPIO pins as variables
YELLOW = 16
RED = 13
Button = 12
Buzz = 6
TRIG = 5
ECHO = 4
IR = 18
Blue = "1400415E76"      #Setting RFID numbers as variables
Circle = "46003BB194"
Rectangle = "5300C7E99B"
BlueBal = 20              #Setting initial balance for each RFID
CircleBal = 10
RectBal = 0
count = 0                  #Variable to count number of vehicles ie RFID tags, initialized to zero
i = 0
switch = 0                 #Variable to indicate if the toll gate system is on or not
SERIAL_PORT = '/dev/ttyS0'

GPIO.setup(GREEN,GPIO.OUT)   #Setting all three LEDs as outputs
GPIO.setup(YELLOW,GPIO.OUT)
GPIO.setup(RED,GPIO.OUT)
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)  #Setting Push Button as input with pull-down resistor
GPIO.setup(Buzz,GPIO.OUT)     #Setting buzzer as output
GPIO.setup(TRIG,GPIO.OUT)     #Setting Trigger as output and Echo as input for Ultrasensonic sensor
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(IR,GPIO.IN,pull_up_down=GPIO.PUD_UP)   #Setting PIR sensor as input with pull-up resistor
p = GPIO.PWM(Buzz,500)      #Setting PWM signal output to Buzzer with frequency 500
LCD.init(0x27,1)            #Initializing LCD with I2C address 27
ADC.setup(0x48)             #Setting up ADC with I2C address 48



myapp = Flask(__name__)  #Setting flask web server
@myapp.route('/')        #Setting up index page
def index():        
    return "Welcome to the Smart Toll Gate!"

@myapp.route('/General_Info')      #Setting up static route 1
def gen_info():
    return "Number of cars that pass through: {}\nTemperature: {:2.2f} C\nHumidity: {} %".format(count, temperature, humidity)

@myapp.route('/Vehicle_Speed')      #Setting up static route 2
def car_speed():                    #Prints speeds of the three RFID cars
    return "Speed of Blue Car: {:2.2f} km/h Speed of Circle Car: {:2.2f} km/h Speed of Rectangle Car: {:2.2f} km/h".format(BlueSpeed, CircleSpeed, RectSpeed)

@myapp.route('/Balance/<RFID>')     #Setting up dynamic route 1
def car_bal(RFID):                  #Prints RFID cars' current balance
    response = "car balance = "
    if(RFID == 'A'):
        car = "Blue " + response + str(BlueBal)
        check = BlueBal
    elif(RFID == 'B'):
        car = "Circle " + response + str(CircleBal)
        check = CircleBal
    elif(RFID == 'C'):
        car = "Rectangle " + response + str(RectBal)
        check = RectBal
    else:
        return "This is not a car registered with us"
    if(check<0):
        check = "   Your balance is low! Time to pay!"
        return car + check
    else:
        return car
   
@myapp.route('/Balance/<RFID>/<take>')      #Setting up dynamic route 2
def cam(RFID, take):                        #Allows to take image or video of RFID car if one is low
    if(BlueBal<0 or CircleBal<0 or RectBal<0):
        timestamp = datetime.now().isoformat()
        if(RFID == 'A'):
            balance = BlueBal
        elif(RFID == 'B'):
            balance = CircleBal
        elif(RFID == 'C'):
            balance = RectBal
        else:
            return "This is not a car registered with us"
        if(take == 'I'):                    #For Image Capture
            photo_path = "/home/pi/Desktop/U23/Flaskpic1.jpg"
            mycamera.start_preview()
            mycamera.annotate_text=" Pic taken at time {} with balance: {}".format(datetime.now().isoformat(), balance)
            time.sleep(10)
            mycamera.capture(photo_path)

            mycamera.stop_preview()
            response = send_file(photo_path,mimetype="image/jpeg")

        elif(take == 'V'):                  #For Video Recording
            mycamera.start_preview()
            mycamera.start_recording('/home/pi/Desktop/U23/video.h264')
            mycamera.annotate_text="Video taken at time {} with balance {}".format(datetime.now().isoformat(), balance)
            time.sleep(10)
            mycamera.stop_recording()
            mycamera.stop_preview()
            photo_path = "/home/pi/Desktop/U23/video.h264"
            response = send_file(photo_path,mimetype="video/h264")
        return response
    else:
        return "None of the balances are critically low"

def distance():         # Function to measure distance of object using Ultrasonic sensor
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(TRIG,1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)       # Activating trigger of ultrasonic sensor for 10 microseconds
    while GPIO.input(ECHO) == 0:     # Using dummy variable to wait until echo signal activates to take t1 time
        a=0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:     # Using dummy variable to wait until ultrasonic singal is fully recieved to take t2 time
        a=0
    time2= time.time()
    duration = time2-time1
    return duration*1000000/58      # Converting time to distance in centimeter using ultrasonic formula


def action(self): # Function after interrupt from PIR sensor (Infrared)
    IRed = 1
    global i
    global BlueBal
    global CircleBal
    global RectBal
    if (i == 0):
        BlueBal = 20
        CircleBal = 10
        RectBal = 0
        i = i + 1
    while (IRed and not switch):      #Checks if toll gate system is first off
        print("Do you want to pay or enqiure (Press 1 for payment, 2 for enquiry, click anything else to cancel)")
        affirm = key.shiftkeypad()
        time.sleep(0.5)
        if(affirm == 1 or affirm == 2):
            print("You have selected: {}".format(affirm))
        if (affirm == 2 and __name__ == '__main__'):
            myapp.run(host = '0.0.0.0', port = 5040)    #Opens and allows for flask to function
        elif (affirm == 1):
            print("Which car are you driving? Choose between A for blue, B for circle, and C for rectangle")
            type = key.keypad()     #Keypad used to type in values
            time.sleep(0.5)
            if(type == 'A' or type == 'B' or type == 'C'):
                print("You have selected: {}. Make your payment (between 01 and 99)".format(type)) # doesnt print right says A is 10
                digit1 = key.shiftkeypad()  #Keypad used to accept numbers
                time.sleep(0.5)
                print("First digit recieved")
                digit2 = key.shiftkeypad()
                time.sleep(0.5)
                print("Second digit recieved")
                digit =str(digit1) + str(digit2)
                if(type == 'A'):
                    s = BlueBal
                    s = s + int(digit)      #Increments keypad-inputted amount into current balance
                    BlueBal=s
                    print("BlueBal = {}".format(BlueBal))       #Prints new balance after payment
                    IRed = 0
                elif(type == 'B'):
                    s = CircleBal
                    s = s + int(digit)
                    CircleBal=s
                    print("CircleBal = {}".format(CircleBal))
                    IRed = 0
                else:
                    s = RectBal
                    s = s + int(digit)
                    RectBal=s
                    print("RectBal = {}".format(RectBal))
        else:
            break       #If invalid value pressed, breaks out loop
                   
def validate_rfid(code):    #validating RFID data from reader
          s = code.decode("ascii")
          if (len(s) == 12) and (s[0] == "\n") and (s[11] == "\r"):
              return s[1:11]
          else:
              return False
           
ser = serial.Serial(baudrate = 2400,  bytesize = serial.EIGHTBITS,  parity = serial.PARITY_NONE,  port = SERIAL_PORT, stopbits = serial.STOPBITS_ONE,  timeout = 1)

def codenum():          
    while switch:
        ser.flushInput()
        ser.flushOutput()
        data=ser.read(12)

        code = validate_rfid(data)
        if code:
            print ("RFID tag: {}".format(code))
            return code
        time.sleep(1)
       
def change(self):      #Function after interrupt from PushButton that changes the state of the gate system
    global switch
    if (switch == 0):
        switch = 1
    else:
        switch = 0

def read_speed():     #Reads from channel 1 (variable potentiometer) and returns digital values to modify speed of car
    ADC1_units= ADC.read(1)
    ADC1_volts=(ADC1_units*3.3)/256
    time.sleep(0.5)
    return (ADC1_units)

def read_rate():      #Reads from channel 0 (potentiometer with a fixed value) and returns digital values to modify rate of deduction after passing toll gate
    ADC0_units= ADC.read(0)
    ADC0_volts=(ADC0_units*3.3)/256
    time.sleep(0.5)
    return (ADC0_units)
       
GPIO.add_event_detect(IR,GPIO.FALLING,callback=action,bouncetime=2000)     #Interrupt without polling for PIR sensor with a bouncetime of 2 seconds
GPIO.add_event_detect(Button, GPIO.FALLING, callback=change, bouncetime=2000) #Interrupt without polling for Push Button with a bouncetime of 2 seconds
   
while True:
    code = 1
    Bal = 1
    Deduce = int(read_rate() / 15)      #Determing the value of deduction for toll gate
    if not switch:                  #When the toll gate system is off
        GPIO.output(RED, True)      #Red LED is on
        GPIO.output(GREEN, False)   #Green LED is off
        LCD.write(0, 0, "Press the button")    

    elif (switch == 1):      #When the toll gate system is turned on  
        p.start(0)           #Setting initial Duty Cycle to zero
        GPIO.output(RED, False)     #Red LED is turned off
        GPIO.output(GREEN, True)    #Green LED is turned on
        LCD.write(0,0,"                ")   #LCD clears
        LCD.write(0,0, "Toll Gate on!")
        time.sleep(1)

        result = DHT11.readDht11(27)      #Storing read data from DHT11 (Temperature, Humidity Sensor) to a variable
        if result:
            humidity, temperature = result
            print ("Humidity: {}%,  Temperature: {} C".format(humidity, temperature))   #Printing Humidity and Temperature values to terminal
            time.sleep(1)
        while(distance() < 10):     #Allows into loop only if distance of vehicle is less than 10 cm ie car approaching toll gate
            p.ChangeDutyCycle(0)    #Change Duty Cycle of PWM signal of buzzer to zero
            if (count == 0):        
                BlueSpeed = 0
                CircleSpeed = 0
                RectSpeed = 0
            if(code == 1):          
                code = codenum()    #Stores read data from RFID reader to a variable
                print("code = {}".format(code))
            count = count+1         #Incremenets count of cars
            speed = 180*read_speed()/255    #Sets speed value from range of 0 to 255 to 0 to 180 km/hr
            print("Speed is {}".format(speed))
            LEDvolt = 3.3*speed*256/180     #Converts speed to voltage value with range 0 to 3.3 V and stores to variable
            ADC.write(LEDvolt)              #Writes this voltage value to ADC which is connected to Yellow LED and affect its brightness based on the voltage value from a range of 0 to 3.3 V
            if(code == Blue):               #Checks for specific RFID
                print("Balance of blue car is {}".format(BlueBal))
                BlueBal-=Deduce
                print("New balance of blue car is {}".format(BlueBal))
                Bal = BlueBal
                BlueSpeed = speed
                print("Speed of blue is {:2.2f} km/h".format(BlueSpeed))
            elif (code == Circle):
                print("Balance of Circle car is {}".format(CircleBal))
                CircleBal-=Deduce
                print("New balance of Circle car is {}".format(CircleBal))
                Bal = CircleBal
                CircleSpeed = speed
                print("Speed of circle is {:2.2f} km/h".format(CircleSpeed))
            elif (code == Rectangle):
                print("Balance of Rectangle car is {}".format(RectBal))
                RectBal-=Deduce
                print("New balance of Rectangle car is {}".format(RectBal))
                Bal = RectBal
                RectSpeed = speed
                print("Speed of rectangle is {:2.2f} km/h".format(RectSpeed))
            if(Bal<1):      #If balance of any one car is zero or below, the buzzer is swicthed on
                p.ChangeDutyCycle(1)    #Duty Cycle of PWM signal changed to full (100%) to turn on Buzzer
                time.sleep(5)           #Buzzer rings for 5 seconds
                p.ChangeDutyCycle(0)    #Duty Cycle set back to zero, setting off the buzzer
            x = urllib.request.urlopen("https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}&field4={}".format(API_KEY, speed, count, temperature, humidity)) #Reads (downloads) RPi values for speed, count of cars, temperature, and humidity to ThingSpeak
            y = urllib.request.urlopen("https://api.thingspeak.com/channels/{}/fields/{}.csv?results={}".format(Ch_id, field_no, readings)) #Writes (uploads) speed value from ThingSpeak
            data=y.read().decode('ascii')
            data=",".join(data.split("\n"))
            for i in range(5, readings*3+3, 3):
                values.append(data.split(",")[i])
            element=float(values[-1])       #Choosing most reent speed value
            LCD.write(0,1, "Speed:{:2.2f}km/h".format(element)) #Prints speed value on LCD
            time.sleep(3)   #Allows LCD to display value for 3 seconds
            LCD.write(0,1,"                ")   #Clears the first line of the LCD
            y = urllib.request.urlopen("https://api.thingspeak.com/channels/{}/fields/{}.csv?results={}".format(Ch_id, 2, readings))   #Writes (uploads) count value from ThingSpeak
            data=y.read().decode('ascii')
            data=",".join(data.split("\n"))
            for i in range(5, readings*3+3, 3):
                values1.append(data.split(",")[i])
            element=float(values1[-1])  #Choosing most recent count value
            LCD.write(0,1, "Count:{}".format(element))  #Prints count value on LCD
            time.sleep(3)
            LCD.write(0,0,"                ")   #Clears both lines of the LCD as it moves back into the loop and restarts
            LCD.write(0,1,"                ")
