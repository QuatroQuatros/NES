from mapper_000 import Mapper_000

class Cartucho:
    def __init__(self, rom):
        self.rom = rom

        self.nMapperId = 0
        self.nPRGBanks = 0
        self.nCHRBanks = 0

        self.vPRGMemory = [0]
        self.vCHRMemory = [0]

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
        self.bImageValid = False

        with open(self.rom, 'rb') as f:
            byte = f.read()
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
            print(self.name[0:3], self.prg_rom_chunks, self.chr_rom_chunks, self.mapper1, self.mapper2)


            #Mapper ID
            self.nMapperId = ((self.mapper2 >> 4) << 4) | (self.mapper1 >> 4)


            self.mirrors = ['HORIZONTAL','VERTICAL','ONESCREEN_LO','ONESCREEN_HI']
            self.mirror = self.mirrors[0]

            if(self.mapper1 & 0x01 == 1):
                self.mirror = self.mirrors[1]


            n = 16

            self.trainer = (self.mapper1 & 0x04 != 0)
            if(self.trainer):
                n += 0x200
                

            #File format
            self.nFileType = 1

            if(self.nFileType == 0):
                pass

            elif(self.nFileType == 1):
                # start = 0x10 + (0x200 * self.trainer)
                # end = start + (0x4000 * self.prg_rom_chunks)
                # memory_pointer = 0x8000

                self.nPRGBanks = self.prg_rom_chunks
                self.vPRGMemory = [0] * (self.nPRGBanks * 16384)

                for i in range(len(self.vPRGMemory)):
                    # print(i, self.trainer, len(self.vPRGMemory))
                    self.vPRGMemory[i] = byte[i+n]

                # print(self.vPRGMemory[0x3FF0:0x3FFF])
                # input()


                self.nCHRBanks = self.chr_rom_chunks
                if(self.nCHRBanks == 0):
                     self.vCHRMemory = [0]*(8192)
                else:   
                    self.vCHRMemory = [0]*(self.nCHRBanks * 8192)

                n += len(self.vPRGMemory)
                for i in range(len(self.vCHRMemory)):
                    self.vCHRMemory[i] = byte[i+n]


            elif(self.nFileType ==2):
                pass

            if(self.nMapperId == 0):
                self.mapper = Mapper_000(self.nPRGBanks, self.nCHRBanks, self.nMapperId)
            #n tem isso
            else:
                self.mapper = Mapper_000(self.nPRGBanks, self.nCHRBanks, self.nMapperId)
                pass
            self.bImageValid = True


    def imageValid(self):
        return self.bImageValid

    # def cpu_read(self, addr, data):
    #     mapped_addr = 0

    #     if(self.mapper.cpu_map_read(addr, mapped_addr)):
    #         print('MEMORIA', hex(self.vPRGMemory[0x3FFC]), hex(self.vPRGMemory[0x3FFD]))
    #         input()
    #         data = self.vPRGMemory[mapped_addr]
    #         print('cartucho', hex(addr), hex(data))
    #         return True
    #     else:
    #         return False

    # def cpu_write(self, addr, data):
    #     mapped_addr = 0
    #     if(self.mapper.cpu_map_write(addr, mapped_addr)):
    #         self.vPRGMemory[mapped_addr] = data
    #         return True
    #     else:
    #         return False


    def cpu_read(self, addr, data):
        mapped_addr = 0
        mapped_addr = self.mapper.cpu_map_read(addr, mapped_addr)
        if( mapped_addr != False):
            data = self.vPRGMemory[mapped_addr]
            return data
        else:
            return False

    def cpu_write(self, addr, data):
        mapped_addr = 0
        mapped_addr = self.mapper.cpu_map_write(addr, mapped_addr)
        if( mapped_addr != False):
            self.vPRGMemory[mapped_addr] = data
            return True
        else:
            return False


    # def ppu_read(self, addr, data):
    #     mapped_addr = 0
    #     if(self.mapper.ppu_map_read(addr, mapped_addr)):
    #         data = self.vPRGMemory[mapped_addr]
    #         return True
    #     else:
    #         return False

    # def ppu_write(self, addr, data):
    #     mapped_addr = 0
    #     if(self.mapper.ppu_map_read(addr, mapped_addr)):
    #         self.vCHRMemory[mapped_addr] = data
    #         return True
    #     else:
    #         return False

    def ppu_read(self, addr, data):
        mapped_addr = 0
        mapped_addr = self.mapper.ppu_map_read(addr, mapped_addr)
        if( mapped_addr != False):
            data = self.vCHRMemory[mapped_addr]
            return data
        else:
            return False

    def ppu_write(self, addr, data):
        mapped_addr = 0
        mapped_addr = self.mapper.ppu_map_read(addr, mapped_addr)
        if(mapped_addr != False):
            self.vCHRMemory[mapped_addr] = data
            return True
        else:
            return False


# rom = 'jogos/Castlevania.nes'
# t = Cartucho(rom)

