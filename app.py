'''
TBJ_Fingerprint Based Check-In System_BN_AM
Code Author - Bilal Nasir & Mohammed Amash Khan
Course - TBJ655
Instructor - Benjamin Shefler
Program - Computer Engineering Technology (ECT)
'''

#Libraries 
from flask import Flask, render_template , url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from time import sleep
import time
import RPi.GPIO as GPIO
import adafruit_fingerprint
import serial


lcd = LCD()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, True)

#Establishes the Connection to the Fingerprint
try:
    uart = serial.Serial("/dev/ttyS0",baudrate = 57600, timeout=1)
    finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    exit(1)

#creates a new Flask Web Application
app = Flask(__name__)
#Configures the SQLalchemy library
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Passes app(flaskwebapp) as a parameter to SQLAlchemy contructor & assigns it to db varible
db = SQLAlchemy(app)

#Create a database model 'User' using SQLAlchemy which can represent & interact with a user record in the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

#Function to Enroll Finger Print the function run when the register button is pressed in the webapplicaiton
def enroll_finger(location):

   #Forloop below runs twice as it needs to capture the fingerprint twice for better Templating
   for fingerimg in range(1, 3):
      if fingerimg == 1:
         lcd.text("Enter Finger",1)
         print("Place finger on sensor...", end="")
      else:
         lcd.text("Enter Finger",1)
         lcd.text("Again",2)
         sleep(2)
         lcd.clear()
         print("Place same finger again...", end="")

      #While loop below takes the image of the finger if adafruit_fingerprint.OK 
      #if fingerprint image is not detected it will fail the enrollment & return
      while True:
         i = finger.get_image()
         if i == adafruit_fingerprint.OK:
               print("Image taken")
               sleep(0.5)
               break
         if i == adafruit_fingerprint.NOFINGER:
               print(".", end="")
         elif i == adafruit_fingerprint.IMAGEFAIL:
               lcd.text("Enroll Failed", 1)
               sleep(2)
               print("Imaging error")
               return False
         else:
               print("Other error")
               lcd.text("Enroll Failed", 1)
               sleep(2)
               return False

      #Compare the two images if both are same then it will proceed ahead with templating 
      #if there are issues whether the image is a mess, feature are different invalid it will fail the enrollment & return
      print("Templating...", end="")
      i = finger.image_2_tz(fingerimg)
      if i == adafruit_fingerprint.OK:
         print("Templated")
      else:
         if i == adafruit_fingerprint.IMAGEMESS:
            lcd.text("Enroll Failed", 1)
            sleep(2)
            print("Image too messy")
         elif i == adafruit_fingerprint.FEATUREFAIL:
            lcd.text("Enroll Failed", 1)
            sleep(2)
            print("Could not identify features")
         elif i == adafruit_fingerprint.INVALIDIMAGE:
            lcd.text("Enroll Failed", 1)
            sleep(2)
            print("Image invalid")
         else:
            lcd.text("Enroll Failed", 1)
            sleep(2)
            print("Other error")
         return False

     #This if statement will only run when the figering is 1 in the forloop menaing after the first fingerprint scan it will prompt the message to remoove finger
      if fingerimg == 1:
         lcd.text("Remove Finger",1)
         print("Remove finger")
         time.sleep(1)
         while i != adafruit_fingerprint.NOFINGER:
            i = finger.get_image()

   #After the for loop for taking the finger image & comparing if valid if everything goes well
   #It will create the model & if there is any error in this process it will fail the enrollment to re-try again
   print("Creating model...", end="")
   i = finger.create_model()
   if i == adafruit_fingerprint.OK:
      print("Created")
   else:
      if i == adafruit_fingerprint.ENROLLMISMATCH:
         lcd.text("Enroll Failed", 1)
         sleep(2)
         print("Prints did not match")
      else:
         lcd.text("Enroll Failed", 1)
         sleep(2)
         print("Other error")
      return False

   #It will store the model into the fingerprint memory itself
   i = finger.store_model(location)
   if i == adafruit_fingerprint.OK:
      lcd.clear()
      lcd.text("Enroll Success", 1)
      sleep(2)
      print("Stored")
   else:
      if i == adafruit_fingerprint.BADLOCATION:
         lcd.text("Enroll Failed", 1)
         sleep(2)
         print("Bad storage location")
      elif i == adafruit_fingerprint.FLASHERR:
         lcd.text("Enroll Failed", 1)
         sleep(2)
         print("Flash storage error")
      else:
         lcd.text("Enroll Failed", 1)
         sleep(2)
         print("Other error")
      return False
   lcd.clear()

   return True

#It will get num_value for the first empty slot in the fingerprint 
def get_num():
    i = len(finger.templates) + 1
    return i

#Function will run if user is valid(fingerprint is valid or user info is present inside the database)
def isT():
   lcd.text("Success", 1)
   lcd.text("Please Enter", 2)
   GPIO.output(18, 0)
   time.sleep(5)
   GPIO.output(18, 1)
#Opposite of above funtion if not valid the below message will be shown on the LCD
def isF():
   lcd.text("Retry", 1)
   lcd.text("Don't Enter", 2)
   sleep(2)

#Create the route for flask application opening the main index.html
@app.route("/", methods=['GET', 'POST'])
def open():
      return render_template('index.html')

#Create the route for the login page which is present wihtin the index.html
@app.route("/login", methods=['GET', 'POST'])
def login():
    #if the Authen button is pressed the below statmente will run prompting the user to enter fingerprint to if valid the isT()
    #function will run meaning success is validation vice versa is not valid isF() will run meaning user is not valid
    if 'Authen' in request.form:
        try:
            lcd.text("Place Your", 1)
            lcd.text("Finger", 2) 
            while ( f.readImage() == False ):
                pass
            f.convertImage(FINGERPRINT_CHARBUFFER1)

            result = f.searchTemplate()
            positionNumber = result[0]

            if ( positionNumber == -1 ):
                isF()
            else:
                isT()

        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            exit(1)

        lcd.clear()

    #if the submit button is pressed menaing the user has inputed his user & pass into the text_box then in this process the fingerprint is not used
    #the data inputed will be assigned to the username & password variable by request.form which will take the data from html page then compare
    #the data with the data present in the SQL database.

    #Database info can be checked in the instance file - users.db
    #CMD to run when present in the instance directory:
    #sudo sqlite3 users.db
    #SELECT * FROM user; (this will show all the data present in the sql database)

    elif 'submit' in request.form:
        username = request.form['name']
        password = request.form['pass']
        user = User.query.filter(User.username == username, User.password == password).first()
        if user is not None:
           lcd.text("Login Success", 1)
           isT()
        else:
           lcd.text("Invalid Info", 1)
           isF()

    sleep(1)
    lcd.clear()

    #after running everything it will return back to the main page
    return render_template('index.html')


#Create the route for the register page which is present wihtin the index.html
@app.route("/register", methods=['GET', 'POST'])
def Register():

   #if the register button is pressed meaning the user has inputed his data that will be stored into the SQL database it will create the variables
   #email, Username & Password the variables will be assigned via the request.form.
   if request.method == "POST":

      email = request.form['email']
      username = request.form['Rname']
      password = request.form['Rpass']
      user = User(username=username, password=password, email=email)
      #After create the variable it will run the function the enroll_finger if the function return true meaning the physical finger registration was 
      #a success then it will put the variable data into the SQL database if it return false meaning finger print registration failed then it will not
      #the variable data into the SQL database
      try:
         if finger.read_templates() != adafruit_fingerprint.OK:
            raise RuntimeError("Failed to read templates")
         print("Fingerprint templates:", len(finger.templates))
         if enroll_finger(get_num()):
            db.session.add(user)
            db.session.commit()
            lcd.text("Info Added", 1)
            sleep(1)

      except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

   lcd.clear()
   #after running everything it will return back to the main page
   return render_template('index.html')


if __name__ == "__main__":

    #create application context for the flask application & the method db.create_all() provided by SQLAlhemy create the the database table
    #based on the model defined in the applicaion
    with app.app_context():
        db.create_all()

    #method to start the flask applicaiton 
    #host='0.0.0.0' will allow any network device connected to same network to open the flask application
    #port = 80 is the default port for HTTP traffic used most commonly for web applications
    #debug = True urns on debug mode for the application, which enables more verbose error messages and other helpful debugging features
    app.run(host='0.0.0.0', port=80, debug=True)
