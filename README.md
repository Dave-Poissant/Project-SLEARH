# Project-SLEARH
Articulated robotic hand designed for sign language education

# Preriquisites:
Hardware:
  - Arduino Mega 2560;
  - 1 usb to printer type cable;
  - 1 drive for the motors ( (PCA-96 85) link: https://www.sunfounder.com/pca9685-16-channel-12-bit-pwm-servo-driver.html);
  - 12 electrical step motors ((TowerPro SG90 Mini-engrenage Micro Servo 9g) link: https://lamassue.fr/product/towerpro-sg90-mini-engrenage-micro-servo-9g/);
  - RaspberryPi 3B+;
  - Micro-SD card (for RPi image);
  
Software;
  - Python 3.7(installed for this gitProject, but not necessarily needed);
  - Python Library:
    - pySerial;
    - tkinter;
  - Arduino IDE for the compiler;
  - Arduino Library:
    - Adafruit_PWMServoDriver.h;
    - ArduinoJson.h;
    - Wire.h;
    (But they all should be downloaded with the plateformio.ini)
    
# Steps to start your project:
  - Read the Mechanics/README.md for informations on how to build the hand;
  - Read the Electrics/README.md for informations on how to plug the motors and the drive on the arduino;
  - Install your favorite python IDE;
  - Open this git repo in a new project and create a python RunTool for UI_Main_Script.py script (that's where the application starts);
  - Install pySerial on your computer (it will appears in your python <python path>/Lib/*);
  (Now, your python side of the project should be up to run)
  - Install VsCode on your computer;
  - Install plateformio and ArduinoIDE in your vscode;
  - Set your Arduino_debug.exe path in your VsCode setups;
  - Build the project one first time (and it should load all the needed libraries);
  (Now, your Arduino side of the project should be up to run)

  - Plug the Arduino to your computer and start the UI_Main_Script.py to start the application and the Arduino thread!
  
 # Steps to be able to run to application on the Raspberry Pi 3b+
  - Flash your Micro-SD card with an up to date RPi image running a linux operating system (you can flash your Micro-SD card with this       tool: https://www.balena.io/etcher/);
  - Connect your Micro-SD card in your RPi and open it with an internet cable or via VMWare for example;
  - On the first RPi's run, set your preferences;
  - Now, open a terminal and instal python 3.6 (or niewer, this could take some time) (this link could be usefull: https://github.com/instabot-py/instabot.py/wiki/Installing-Python-3.7-on-Raspberry-Pi);
  - Install the PySerial library with:
    $ sudo apt-get install pyserial
  - If you're connected to your RPi via VMWare or ssh, run this command:
    - $ export DISPLAY=:0
  - Create your project directory where you want it on your RPi:
    - $ cd "DIRECTORY PATH"
    - $ mkdir "PROJECT NAME"
    - $ cd "PROJECT NAME"
    - $ git clone "THE PROJECT'S LINK"
    - $ git pull
  - The project should now be copied locally onto your RPi;
  
  - Now go to the project's Ui_Main_script.py path on your RPi and run the program through a terminal:
    - $ python Ui_Main_Script.py
  
# Now Have Fun !
