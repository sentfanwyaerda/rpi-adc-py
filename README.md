rpi-adc-py
==========

*RaspberryPi ADC toolset*

###Setup
I use the Adafruit cobbler to connect my GPIO pins to the breadboard. I use the MCP3008 as ADC. On the right side: Pin 1&2 VCC (3,3V), Pin 3&8 GND, Pin 4 CLK > #18, Pin 5 MISO > #23, Pin 6 MOSI > #24, Pin 7 CS > #25. The left side has 8 adcpins [0,7] to connect sensors.
```
0: Electret Microphone Amplifier MAX4466 (signal copy)
1:
2:
3:
4: TMP36 Analoge Temperature sensor
5: CdS photo cell
6: 
7: Electret Microphne Amplifier MAX4466
```

###Installation
```
sudo apt-get install python-dev python-smbus i2ctools python-setuptools
sudo easy_install rpi.gpio #or sudo apt-get install python-rpi.gpio
echo "i2c-bmc2708\ni2c-dev" >> /etc/modules
echo "#blacklist spi-bcm2708\n#blacklist i2c-bcm2708" > /etc/modprobe.d/raspi-blacklist.conf
```
and detect your current connected i2c with: ``i2cdetect -y 1``

```git clone https://github.com/sentfanwyaerda/rpi-adc-py.git```
