# AD5274 Python Library

This is a python library for using the Analog AD5274 Digital Rheostat with an I2C interface.  Please see the following link for more information about the HW:  https://www.analog.com/en/products/ad5274.html .  

This library uses the libmraa low level skeleton library for communication (https://iotdk.intel.com/docs/master/mraa/)

This module was inspired by a C module using libmraa for this hardware, but I can't seem to find the original C module to give credit where credit is due.  
If anyone finds this C module let me know so I can link to it.

This has been tested on an Intel Edison, but technically should be able to work on any platform for which libmraa is available.

This will likely work for an AD5272 as well, but it has not been tested, so it's unknown as to what, if any, changes would be necessary.  

This software is provided as-is.