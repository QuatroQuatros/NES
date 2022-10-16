from mapper_000 import Mapper_000

class Cartucho:
    def __init__(self, rom):
        self.rom = rom

        self.nMapperId = 0
        self.nPRGBanks = 0
        self.nCHRBanks = 0

        self.vPRGMemory = [0]

        self.header_size = 0x10

        self.name = [0] * 4
        self.prg_rom_chunks = 0
        self.chr_rom_chunks = 0
        self.mapper1 = 0
        self.mapper2 = 0 
        self.prg_ram_size = 0
        self.tv_system1 = 0
        self.tv_system2 = 0
        self.unused = [0] * 5

        with open(self.rom, 'rb') as f:
            byte = f.read()
            # print(byte)
            # input()
            for i in range(self.header_size):
                if( i <= 3):
                    self.name[i] = byte[i]
                elif(i == 4):
                    self.prg_rom_chunks = byte[i]
                elif(i == 5):
                    self.chr_rom_chunks = byte[i]
                elif(i == 6):
                    self.mapper1 = byte[i]
                elif(i == 7):
                    self.mapper2 = byte[i]
                elif(i == 8):
                    self.prg_ram_size = byte[i]
                elif(i == 9):
                    self.tv_system1 = byte[i]
                elif(i == 10):
                    self.tv_system2 = byte[i]
                else:
                    pass

            if(self.mapper1 & 0x04):
                pass

            #Mapper ID
            self.nMapperId = ((self.mapper2 >> 4) << 4) | (self.mapper1 >> 4)

            #File format
            self.nFileType = 1

            if(self.nFileType == 0):
                pass
            elif(self.nFileType == 1):
                self.nPRGBanks = self.prg_rom_chunks
                self.vPRGMemory = bytearray(self.nPRGBanks * 16384)
                for i in range(len(self.vPRGMemory)):
                    self.vPRGMemory[i] = byte[i]

                self.nCHRBanks = self.chr_rom_chunks
                self.vCHRMemory = bytearray(self.nCHRBanks * 8192)
                for i in range(len(self.vCHRMemory)):
                    self.vCHRMemory[i] = byte[i]


            elif(self.nFileType ==2):
                pass

            if(self.nMapperId == 0):
                self.mapper = Mapper_000(self.nPRGBanks, self.nCHRBanks)
                print(self.vCHRMemory)
                # input()
            #n tem isso
            else:
                pass


    def cpu_read(self, addr, data):
        mapped_addr = 0
        if(self.mapper.cpu_map_read(addr, mapped_addr)):
            data = self.vPRGMemory[mapped_addr]
            return True
        else:
            return False

    def cpu_write(self, addr, data):
        mapped_addr = 0
        if(self.mapper.cpu_map_write(addr, mapped_addr)):
            self.vPRGMemory[mapped_addr] = data
            return True
        else:
            return False

    def ppu_read(self, addr, data):
        mapped_addr = 0
        if(self.mapper.ppu_map_read(addr, mapped_addr)):
            data = self.vPRGMemory[mapped_addr]
            return True
        else:
            return False

    def ppu_write(self, addr, data):
        mapped_addr = 0
        if(self.mapper.ppu_map_read(addr, mapped_addr)):
            self.vPRGMemory[mapped_addr] = data
            return True
        else:
            return False


# rom = 'jogos/Castlevania.nes'
# t = Cartucho(rom)

