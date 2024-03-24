import math
import time
from machine import ADC, Pin

class MQ135V2(object):

    __adc = None
    
    # ADC value to voltage first degree equation coefficients
    __alpha = 0.000838616
    __beta = 0.097068
    RLOAD = 22.0
    RZERO = 100
    PARA = 116.6020682
    PARB = 2.769034857
    CORA = 0.00035
    CORB = 0.02718
    CORC = 1.39538
    CORD = 0.0018
    CORE = -0.003333333
    CORF = -0.001923077
    CORG = 1.130128205
    ATMOCO2 = 417.06
    
    def __init__(self, pin_adc):
        self.__adc = ADC(Pin(pin_adc))
        self.__adc.atten(ADC.ATTN_11DB)
        self.__adc.width(ADC.WIDTH_12BIT) 
        
        
    def get_correction_factor(self, temperature, humidity):
        """Calculates the correction factor for ambient air temperature and relative humidity

        Based on the linearization of the temperature dependency curve
        under and above 20 degrees Celsius, asuming a linear dependency on humidity,
        provided by Balk77 https://github.com/GeorgK/MQ135/pull/6/files
        """
        if temperature < 20:
            return self.CORA * temperature * temperature - self.CORB * temperature + self.CORC - (humidity - 33.) * self.CORD
        return self.CORE * temperature + self.CORF * humidity + self.CORG
    
    def get_resistance(self):
        """Returns the resistance of the sensor in kOhms // -1 if not value got in pin"""
        value = 0
        for i in range(256):
            value += self.__adc.read()
        value = value >> 8
        if value <= 0:
            value = 1
        last_value = (2048.0/value - 1.0) * self.RLOAD
        if last_value <= 0:
            last_value = 1
        return last_value
    
    def get_corrected_resistance(self, temperature, humidity):
        """Gets the resistance of the sensor corrected for temperature/humidity"""
        return self.get_resistance()/ self.get_correction_factor(temperature, humidity)

    def get_ppm(self):
        """Returns the ppm of CO2 sensed (assuming only CO2 in the air)"""
        return self.PARA * math.pow((self.get_resistance()/ self.RZERO), -self.PARB)

    def get_corrected_ppm(self, temperature, humidity):
        """Returns the ppm of CO2 sensed (assuming only CO2 in the air)
        corrected for temperature/humidity"""
        return self.PARA * math.pow((self.get_corrected_resistance(temperature, humidity)/ self.RZERO), -self.PARB)

    def get_rzero(self):
        """Returns the resistance RZero of the sensor (in kOhms) for calibratioin purposes"""
        return self.get_resistance() * math.pow((self.ATMOCO2/self.PARA), (1./self.PARB))

    def get_corrected_rzero(self, temperature, humidity):
        """Returns the resistance RZero of the sensor (in kOhms) for calibration purposes
        corrected for temperature/humidity"""
        return self.get_corrected_resistance(temperature, humidity) * math.pow((self.ATMOCO2/self.PARA), (1./self.PARB))

