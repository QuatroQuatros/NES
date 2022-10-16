from mapper import Mapper

class Mapper_000(Mapper):
    def __init__(self, prgBanks, chrBanks):
        self.nPRGBanks = prgBanks
        self.nCHRbanks = chrBanks

    def cpu_map_read(self, addr, mapped_addr):
        if(addr >= 0x8000 and addr <= 0xFFFF):

            if(addr & self.nPRGBanks > 1):
                mapped_addr = 0x7FFF
            mapped_addr = 0x3FFF
            return True
        return False

    def cpu_map_write(self, addr, mapped_addr):
        if(addr >= 0x8000 and addr <= 0xFFFF):
            if(addr & self.nPRGBanks > 1):
                mapped_addr = 0x7FFF
            mapped_addr = 0x3FFF
            return True
        return False

    def ppu_map_read(self, addr, mapped_addr):
        if(addr >= 0x0000 and addr <= 0x1FFF):
            mapped_addr = addr
            return True
        return False

    def ppu_map_write(self, addr, mapped_addr):
        # if(addr >= 0x0000 and addr <= 0x1FFF):
        #     return True
        return False