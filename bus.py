from cpu import CPU
from ppu import PPU
from cartucho import Cartucho

class BUS:
    def __init__(self, rom):
        #Dispositivos conectados
        self.cpu = CPU(self)
        self.cartucho = Cartucho(rom)
        self.ppu = PPU(self.cartucho)
        #memoria da CPU
        self.cpu_ram = [0] * (2048)

        #contador
        self.system_clock_counter = 0

        self.cpu.reset()

        # rom = 'jogos/teste.4444'
        # #rom = 'jogos/4444.bin'
        # #rom = 'jogos/o6502-2022-10-15-161248.bin'
        # #rom = 'jogos/Castlevania.nes'

        # with open(rom, 'rb') as f:
        #     byte = f.read()
        #     print(byte)
        #     input()
        #     for i in range(len(byte)):
        #         self.cpuRam[0x8000 + i] = byte[i]
        # print(self.cpuRam[0x8000:0x802C])
        # print(self.cpuRam[0x8010:0x8016])
        # self.cpuRam[0xFFFC] = 0x00
        # self.cpuRam[0xFFFD] = 0x80

    
        


    def cpu_write(self, addr, data):
        if(self.cartucho.cpu_write(addr, data)):
            pass

        elif addr >= 0x0000 and addr <= 0x1FFF:
            self.cpu_ram[addr & 0x07FF] = data
        elif (addr >= 0x2000 and addr <= 0x3FFF):
            self.ppu.cpu_write(addr & 0x0007, data)

    def cpu_read(self, addr, readonly = False):
        data = 0x00
        if(self.cartucho.cpu_read(addr, data)):
            print('entrei aqui')
        elif addr >= 0x0000 and addr <= 0x1FFF:
            data = self.cpu_ram[addr & 0x07FF]
        elif (addr >= 0x2000 and addr <= 0x3FFF):
            data = self.ppu.cpu_read(addr & 0x0007, readonly)
        return data
        
    def clock(self):
        self.ppu.clock()
        if(self.system_clock_counter % 3 == 0):
            self.cpu.clock()
        else:
            self.system_clock_counter += 1

    def draw(self, status, pc, a, x, y, stack, opcode):
        self.ppu.draw(status, pc, a, x, y, stack, opcode, self.cpu_ram[0x00:0x10])


