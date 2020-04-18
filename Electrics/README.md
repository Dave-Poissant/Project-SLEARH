# Electrical Parts list

    Name	              Description	                                Quantity
    ------------------------------------------------------------------------
    Arduino board	      Arduino Mega 2560	                              1
    Servo driver	      PCA9685 16 channel PWM servo Driver	            1
    Servo motors	      SG90 servo motor	                              12

# Electrical Connections:

  # Arduino pins:
    - 5V:         Ard1 -------> Dr6
    - Gnd:        Ard2 -------> Dr3
    - Vin:        Ard3 -------> Dr7
    - Gnd:        Ard4 -------> Dr1
    - 5V:         Ard5 -------> Dr2
    - scl(pin21): Ard6 -------> Dr4
    - sda(pin20): Ard7 -------> Dr5
    
  # Drive pins:
    - Gnd:        Dr1 --------> Ard4
    - V+:         Dr2 --------> Ard5
    - Gnd:        Dr3 --------> Ard2
    - scl         Dr4 --------> Ard6
    - sda         Dr5 --------> Ard7
    - Vcc         Dr6 --------> Ard1
    - V+          Dr7 --------> Ard3
    
    - 0           Dr8 --------> motor 0
    - 1           Dr9 --------> motor 1
    - 2           Dr10 -------> motor 2
    - 3           Dr11 -------> motor 3
    - 4           Dr12 -------> motor 4
    - 5           Dr13 -------> motor 5
    - 6           Dr14 -------> motor 6
    - 7           Dr15 -------> motor 7
    - 8           Dr16 -------> motor 8
    - 9           Dr17 -------> motor 9
