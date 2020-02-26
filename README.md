# Project-SLEARH
Articulated robotic hand designed for sign language education

# Preriquisites:
Hardware:
  - Arduino Mega 2560;
  - 1 usb to printer type cable;
  - 1 drive for the motors ( (PCA-96 85) link: https://www.sunfounder.com/pca9685-16-channel-12-bit-pwm-servo-driver.html);
  - 12 electrical step motors ((TowerPro SG90 Mini-engrenage Micro Servo 9g) link: https://lamassue.fr/product/towerpro-sg90-mini-engrenage-micro-servo-9g/);
  - RaspberryPi 3B+;
  
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
    
# Step to start your project:
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
  
# Now Have Fun !
