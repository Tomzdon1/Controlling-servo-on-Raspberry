import socket
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
pwm.start(5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
pwm1 = GPIO.PWM(14, 100)
pwm1.start(5)


mysocket = socket.socket()
host = socket.gethostbyname(socket.getfqdn())
port = 9874

angle = 122
angle1=122

if host == "127.0.1.1":
    import commands
    host = commands.getoutput("hostname -I")
print "host = " + host

#Prevent socket.error: [Errno 98] Address already in use
mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

mysocket.bind((host, port))

mysocket.listen(5)

c, addr = mysocket.accept()

while True:

      data = c.recv(1024)
      data = data.replace("\r\n", '') #remove new line character
      inputStr = "Received " + data + " from " + addr[0]
      print inputStr
      c.send("Hello from Raspberry Pi!\nYou sent: " + data + "\nfrom: " + addr[0] + "\n")
      duty=float(angle) /10+ 2.5
      pwm.ChangeDutyCycle(duty)
      if data == "ON" and  angle < 181:
        angle=angle+3
        duty=float(angle) /10+ 2.5
        pwm.ChangeDutyCycle(duty)
        print angle
      if data == "OFF" and  angle> 60:
        angle=angle-3
        duty=float(angle) /10+ 2.5
        pwm.ChangeDutyCycle(duty)
        print angle

      if data == "ADD" and angle1 > 61:
        angle1=angle1+3
        duty1=float(angle1) /10+ 2.5
        pwm1.ChangeDutyCycle(duty1)
        print angle1

      if data == "SUB" and angle1 > 61:
        angle1=angle1-3
        duty1=float(angle1) /10+ 2.5
        pwm1.ChangeDutyCycle(duty1)
        print angle1
c.send("Server stopped\n")
print "Server stopped"
c.close()
