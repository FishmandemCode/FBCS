# FBCS (Finger Based Check-in System)
Final Semester Project (Finger Based Check-in System)

What is the Product?
- An authentication system to stream line the commercial check in process while increasing security
- Uses Fingerprints to authenticate users

Key Skills Utilized:
- Python: The primary language orchestrating the system's control logic, ensuring robust functionality and seamless integration.
- HTML, CSS & JavaScript: Crafted an intuitive Web GUI to enhance user interaction, providing a seamless experience for system operation.
- SQL: Employed a secure and scalable database for the storage of user login information, ensuring data integrity and access control.
- lask: Hosted the Web Server internally, leveraging Flask's lightweight and powerful capabilities for optimal performance within the network.
- Hardware Integration: Utilized Raspberry Pi as the central hub, demonstrating proficiency in hardware orchestration. Integrated the R307 Finger-based Scanner for reliable biometric data collection, enhancing security measures.

Key Features:
- Fingerprint scanner: The R307 finger print scanner used in this project waits for a finger to be placed on the scanner, once done, if authenticated, it activates the solenoid to unlock the door. The scanner is also used during the enrollment process to store alongside the user ID.
- Web based application with the GUI: The user will use to interact with the application. Uses Flask to run a web application that will give the user the option to either log in with just the credentials, or to create a new account.
- Door lock that unlocks when authenticated: A 12V solenoid that is activated when the fingerprint is authenticated causing it to contract, in turn unlocking the door. 
- LCD that displays interim messages: During the authentication and registering parts of the process. Connects to the 5V of the pi to get power while the SDA and SCL pins connect to their corresponding ones on the Pi.

How it Works:
- User chooses between the options presented in the web application GUI. They either log in with their credentials, unlock the lock by scanning their fingerprint by selecting “Authenticate”, or create a new account.
- If the first two options are selected, and the system authenticates the user, the door is unlocked for 5 seconds (this value can be modified to the needs of the customer) allowing the user to open the door and go in.
- If the third option is selected, a new screen appears asking the user to enter their Email ID, User and Password after which they are prompted to enroll their fingerprint by following the instructions on the screen.
- In order to view the GUI, the web application will be accessed by entering the provided IP address of the raspberry Pi into the browser. For this purpose, any screen can be used, either a monitor with a keyboard or mouse, or for a more modern look, an iPad or tablet which will allow for touch screen use while looking sleek and being efficient. 

How It was Built:
![image](https://github.com/FishmandemCode/FBCS/assets/106996740/b84b8e40-93aa-4154-884e-662c140c117b)

Schematic:
![image](https://github.com/FishmandemCode/FBCS/assets/106996740/20af741a-706d-4755-9f0c-666432edd6c9)

References:
Anon. (-). Raspberry Pi 4 4GB. CanaKit.
https://www.canakit.com/raspberry-pi-4-4gb.html

Heidenreich, M (2020, 25 Nov). How to Use the LCD1602 I2C Display with Raspberry Pi (Python Tutorial with Multi-Threading). YouTube.
https://www.youtube.com/watch?v=DHbLBTRpTWM

Rovai, M (2018, 17 Mar). Python WebServer With Flask & Raspberry Pi. Medium.
https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d

Mohanan, V. (2021, 11 May). Interfacing R307 Optical Fingerprint Scanner with Arduino Boards for Biometric Authentication. Circuitstate.
https://circuitstate.com/tutorials/interfacing-r307-optical-fingerprint-scanner-with-arduino-boards-for-biometric-authentication/#r307-specifications

Neupane, A (2021, 12 Mar). Python Flask Authentication Tutorial - Learn Flask Login. YouTube.
https://www.youtube.com/watch?v=71EU8gnZqZQ&t=854s

Tim. (2023, 15 Feb). Raspberry Pi Imager - How to Use. Core Electronics.
https://core-electronics.com.au/guides/raspberry-pi/raspberry-pi-imager/

Tim. (2023, 16 Feb). Controlling a Solenoid with Raspberry Pi and a Relay. Core Electronics.
https://core-electronics.com.au/guides/solenoid-control-with-raspberry-pi-relay/










