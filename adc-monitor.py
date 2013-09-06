#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
DEBUG = 0 # 0,1,2


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

def readadc_avg(adcnum, clockpin, mosipin, misopin, cspin, size=50):
	adcout = []
	for i in range (0, size):
		adcout.append( readadc(adcnum, clockpin, mosipin, misopin, cspin) * 1.000 )
	avg = sum(adcout) / len(adcout)
	return avg

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

VCC = 3.3
R = 1.000

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

factor = 1

while True:
        # read the analog pins
        adcpin0 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS) / factor
        adcpin1 = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS) / factor
	adcpin2 = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS) / factor
	adcpin3 = readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS) / factor
	adcpin4 = readadc_avg(4, SPICLK, SPIMOSI, SPIMISO, SPICS) / factor
	adcpin5 = readadc_avg(5, SPICLK, SPIMOSI, SPIMISO, SPICS) / factor
	adcpin6 = readadc(6, SPICLK, SPIMOSI, SPIMISO, SPICS) / factor
	adcpin7 = readadc_avg(7, SPICLK, SPIMOSI, SPIMISO, SPICS) / factor

	#value4 = (adcpin4 / 1.023) * 2.0
	value4 = ( ( (adcpin4 / R ) * VCC ) - 500 ) / 10

	#value5 = ( VCC * ( R / ( R + adcpin5 )) )
	#value5 = ( ( adcpin5 / 10.23 ) * VCC )
	#value5 = VCC * ( adcpin5 / R )
	value5 = (adcpin5 / 10.23 )

        if DEBUG:
	       	print 'ADC: MCP3008 \t    0:[ {pin0}\t]   1:[ {pin1}\t]   2:[ {pin2}\t]   3:[ {pin3}\t]   4:[ {pin4}\t]   5:[ {pin5}\t]   6:[ {pin6}\t]   7:[ {pin7}\t]' .format(pin0 = adcpin0, pin1 = adcpin1, pin2 = adcpin2, pin3 = adcpin3, pin4 = adcpin4, pin5 = adcpin5, pin6 = adcpin6, pin7 = adcpin7)

	if DEBUG != 2:
		print 'ADC: Values:\t      [{empty}\t]     [{empty}\t]     [{empty}\t]     [{empty}\t]     [ {v4}*C\t] lux:[ {v5}%\t]     [{empty}\t]     [{empty}\t]' .format(v5 = round(value5, 1), v4 = round(value4,1), empty = "   " )

        # hang out and do nothing for a half second
        time.sleep(0.05)
