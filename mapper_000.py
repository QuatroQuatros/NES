class Mapper_000:
    def __init__(self, prgBanks, chrBanks, id):
        self.nPRGBanks = prgBanks
        self.nCHRbanks = chrBanks
        self.id = id

    # def cpu_map_read(self, addr, mapped_addr):
    #     if(addr >= 0x8000 and addr <= 0xFFFF):

    #         if(self.nPRGBanks > 1):
    #             mapped_addr = addr & 0x7FFF
    #             return True
    #         else:
    #             #retornar isso
    #             mapped_addr = addr & 0x3FFF
    #             return True

    #     return False

    # def cpu_map_write(self, addr, mapped_addr):
    #     if(addr >= 0x8000 and addr <= 0xFFFF):
    #         if(self.nPRGBanks > 1):
    #             mapped_addr = addr & 0x7FFF
    #             return True
    #         else:
    #             mapped_addr = addr & 0x3FFF
    #             return True

    #     return False

    def cpu_map_read(self, addr, mapped_addr):
        if(addr >= 0x8000 and addr <= 0xFFFF):

            if(self.nPRGBanks > 1):
                mapped_addr = addr & 0x7FFF
                return mapped_addr
            else:
                mapped_addr = addr & 0x3FFF
                return mapped_addr

        return False

    def cpu_map_write(self, addr, mapped_addr):
        if(addr >= 0x8000 and addr <= 0xFFFF):
            if(self.nPRGBanks > 1):
                mapped_addr = addr & 0x7FFF
                return mapped_addr
            else:
                mapped_addr = addr & 0x3FFF
                return mapped_addr

        return False



    # def ppu_map_read(self, addr, mapped_addr):
    #     if(addr >= 0x0000 and addr <= 0x1FFF):
    #         mapped_addr = addr
    #         return True
    #     return False

    def ppu_map_read(self, addr, mapped_addr):
        if(addr >= 0x0000 and addr <= 0x1FFF):
            mapped_addr = addr
            return mapped_addr
        return False

    def ppu_map_write(self, addr, mapped_addr):
        if(addr >= 0x0000 and addr <= 0x1FFF):
            if(self.nCHRbanks == 0):
                mapped_addr = addr
                return True
        return False
