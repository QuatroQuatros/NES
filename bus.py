from cpu import CPU
from ppu import PPU
from cartucho import Cartucho

class BUS:
    def __init__(self, rom):
        #Dispositivos conectados
        self.cartucho = Cartucho(rom)
        self.cpu = CPU(self)
        self.ppu = PPU(self.cartucho)
        #memoria da CPU
        self.cpu_ram = [0] * 2048

        #contador
        self.system_clock_counter = 0

        


        if(self.cartucho.imageValid()):
            self.reset()




    
    def reset(self):
        self.system_clock_counter = 0
        self.cpu.reset()

    def cpu_read(self, addr, readonly = False):
        data = 0x00
        if addr >= 0x0000 and addr <= 0x1FFF:
            data = self.cpu_ram[addr & 0x07FF]

        elif (addr >= 0x2000 and addr <= 0x3FFF):
            data = self.ppu.cpu_read(addr & 0x0007, readonly)

        else:
            data = self.cartucho.cpu_read(addr, data)
        return data


        
    def cpu_write(self, addr, data):
        if(self.cartucho.cpu_write(addr, data)):
            pass

        elif addr >= 0x0000 and addr <= 0x1FFF:
            self.cpu_ram[addr & 0x07FF] = data

        elif (addr >= 0x2000 and addr <= 0x3FFF):
            self.ppu.cpu_write(addr & 0x0007, data)



    # def cpu_read(self, addr, readonly = False):
    #     data = 0x00
    #     print('bus', hex(addr))

    #     if(self.cartucho.cpu_read(addr, data)):
    #         print('to aqui')

    #     elif addr >= 0x0000 and addr <= 0x1FFF:
    #         data = self.cpu_ram[addr & 0x07FF]

    #     elif (addr >= 0x2000 and addr <= 0x3FFF):
    #         data = self.ppu.cpu_read(addr & 0x0007, readonly)

    #     print('addr e data =',addr, data)
    #     input()
    #     return data

    
    # def cpu_write(self, addr, data):
    #     if(self.cartucho.cpu_write(addr, data)):
    #         pass

    #     elif addr >= 0x0000 and addr <= 0x1FFF:
    #         self.cpu_ram[addr & 0x07FF] = data

    #     elif (addr >= 0x2000 and addr <= 0x3FFF):
    #         self.ppu.cpu_write(addr & 0x0007, data)


        
    def clock(self):
        self.ppu.clock()
        if(self.system_clock_counter % 3 == 0):
            self.cpu.clock()

        if(self.ppu.nmi):
            self.ppu.nmi = False
            self.cpu.nmi()

        self.system_clock_counter += 1


    def draw(self, status, pc, a, x, y, stack, opcode):
        self.ppu.draw(status, pc, a, x, y, stack, opcode, self.cpu_ram[0x00:0x10])

    def incPalette(self):
        self.ppu.incPalette()


