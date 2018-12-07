from time import sleep
import mraa as m

class ad5274:
    AD5272_DEV_ADDR = 0x2F  # << 1
    I2C_WRITE = 0
    I2C_READ = 1

    AD5272_WRITE = (AD5272_DEV_ADDR | I2C_WRITE)

    AD5272_READ = (AD5272_DEV_ADDR | I2C_READ)

    AD5272_MAX_RESISTANCE = 0x64   # 100 kohm in this instance
    #// commands
    NO_OPERATION = 0x00
    WRITE_WIPER_POSITION = 0x04
    READ_WIPER_POSITION = 0x08
    STORE_WIPER_POSITION = 0x0C
    SOFTWARE_RESET = 0x10
    READ_STORED_WIPER = 0x14
    GET_ADDR_LAST_PROG_WIPER = 0x18
    WRITE_CONTROL_REG = 0x1C
    READ_CONTROL_REG = 0x20
    SHUTDOWN_REG = 0x24
    #// some options for READ_STORED_WIPER
    FIRST_WIPER_LOCATION = 0x01
    LAST_WIPER_LOCATION = 0x32
    #// options for WRITE_CONTROL_REG
    DISABLE_ALL = 0x00
    STORE_WIPER_POSITION_ENABLE  = 0x01
    SET_WIPER_POSITION_ENABLE = 0x02
    RESISTOR_CALIB_DISABLE = 0x04
    WIPER_POSITION_STORE_SUCCESS = 0x08

    #// options for SHUTDOWN_REG
    WAKE_UP  = 0x00  
    SHUTDOWN  = 0x01

    I2C_BUS = 6
    def __init__(self, bus=6, address=0x2F):

        self.I2C_BUS = bus
        self.AD5272_DEV_ADDR= address
        self.Ad5272_Init()

    def Ad5272_Init(self):
        self.Write_Control(self.STORE_WIPER_POSITION_ENABLE | self.SET_WIPER_POSITION_ENABLE)


    def Shutdown(self):
            x = m.I2c(self.I2C_BUS)
            x.address(self.AD5272_DEV_ADDR | self.AD5272_WRITE)
            ba = bytearray(2)
            ba[0] = self.SHUTDOWN_REG
            ba[1] = self.SHUTDOWN
            x.write(ba)


    def Wake_Up(self): 
            x = m.I2c(self.I2C_BUS)
            x.address(self.AD5272_DEV_ADDR | self.AD5272_WRITE)
            ba = bytearray(2)
            ba[0] = self.SHUTDOWN_REG
            ba[1] = self.WAKE_UP
            x.write(ba)


    def Reset(self):
            x = m.I2c(self.I2C_BUS)
            x.address(self.AD5272_DEV_ADDR | self.AD5272_WRITE)
            ba = bytearray(2)
            ba[0] = self.SOFTWARE_RESET
            ba[1] = 0x00
            x.write(ba)


    def Set_Wiper(self,sixteen_bit_value):
        
        if(sixteen_bit_value > 0x3FF):
            print ("Bit value exceeds bounds.")
            
        else:
            x = m.I2c(self.I2C_BUS)
            x.address(self.AD5272_DEV_ADDR | self.AD5272_WRITE)
            ba = bytearray(2)
            ba[0] = (self.WRITE_WIPER_POSITION | (sixteen_bit_value >> 8))
            ba[1] = sixteen_bit_value & 0x00FF
            x.write(ba)

    def Set_Wiper_Resistance(self,resistance):
            if (resistance > self.AD5272_MAX_RESISTANCE) or (resistance < 0):
                print ("Resistance value exceeds bounds")
            else:
                self.Set_Wiper((resistance / self.AD5272_MAX_RESISTANCE) * 1023);
            


    def Set_Wiper_Percentage(self,percent):
            if (percent > 100) or (percent < 0):
                print ("Percentage exceeds bounds.")
            else:
                self.Set_Wiper((percent / 100) * 1023)



    def Set_Stored_Wiper(self,location):
            if (location < 0x01) or (location > 0x32):
                print( "Wiper location exceeds bounds.")
            else:
                self.Set_Wiper(self.Read_Stored(location))



    def Read_Wiper(self):
            x = m.I2c(self.I2C_BUS)
            x.address(self.AD5272_DEV_ADDR | self.AD5272_WRITE)
            ba = bytearray(2)
            ba[0] = self.READ_WIPER_POSITION
            ba[1] = 0x00
            x.write(ba)
            positionarray = x.read(2)
            position = 0
            position = (positionarray[0] << 8) | positionarray[1]

            return position


    def Save_Wiper(self):
            x = m.I2c(self.I2C_BUS)
            x.address(self.AD5272_DEV_ADDR | self.AD5272_WRITE)
            x.writeByte(self.STORE_WIPER_POSITION)
            x.writeByte(0x00)
            time.sleep(0.35)



    def Read_Stored(self,location):
            x = m.I2c(self.I2C_BUS)
            x.address(self.AD5272_DEV_ADDR | self.AD5272_WRITE)
            x.writeByte(location & 0x00FF)
            value = x.readByte() << 8
            value |= x.readByte()
            return value


    def Read_Last_Stored_Addr(self):
            x = m.I2c(self.I2C_BUS)
            x.address(self.AD5272_DEV_ADDR | self.AD5272_WRITE)
            x.writeByte(self.GET_ADDR_LAST_PROG_WIPER)
            x.writeByte(0x00)
            location = x.readByte()
            return location


    def Write_Control(self,control):
            x = m.I2c(self.I2C_BUS)
            x.address(self.AD5272_DEV_ADDR | self.AD5272_WRITE)
            ba = bytearray(2)
            ba[0] = self.WRITE_CONTROL_REG
            ba[1] = control
            x.write(ba)

    def Read_Control(self):
        x = m.I2c(self.I2C_BUS)
        x.address(self.AD5272_DEV_ADDR | self.AD5272_WRITE)
        ba = bytearray(2)
        ba[0] = self.READ_CONTROL_REG
        ba[1] = 0x00
        x.write(ba)
        control = x.readByte()#i2c_readAck()

        return control;


    def Save_Success(self):
            r = self.Read_Control()
            if r & 0x08:
                ret = true
            else:
                ret = false                
            return ret;

    def Set_Voltage(self, voltage):
        
        wipervalue = int( (30000/(voltage-5)-2940)*256/20000 )
        wipervalue = wipervalue << 2
        self.Set_Wiper(wipervalue)
      
    def Read_Voltage(self):
        wipervalue = self.Read_Wiper()
        wipervalue = wipervalue >> 2  #shift it 2 since those bits are not part of the actual value
        voltage=float( (30000.0/(20000.0*wipervalue/256.0+2940.0))+5 )
        
        return voltage  



if __name__ == "__main__":
        pot = ad5274()
        #Init()
        ctrl = pot.Read_Control()
        print (ctrl)
        wiper = pot.Read_Wiper()
        print (str(wiper))
        pot.Set_Wiper(0x028)
        pot.Set_Voltage(12.0)
        voltage = pot.Read_Voltage()
        print (str(voltage))
        wiper = pot.Read_Wiper()
        print (str(wiper))