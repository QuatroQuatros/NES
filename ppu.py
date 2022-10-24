import pygame
from tile import Tile
from random import randint
from pygame import gfxdraw

class PPU:
    def __init__(self, cartucho):
        pygame.init()
        pygame.font.init()
        self.cartucho = cartucho
        self.tblName = [[0]*1024, [0]*1024]
        self.tblPalette = [0] * 32
        self.tblPattern = [[0]*4096, [0]*4096]
        # self.tblPattern = [0] * 8192 #isso n é necessario

        self.frame_complete = False
        self.scanline = 0
        self.cycle = 0


        #status
        self.unused = 5
        self.sprite_overflow = 1
        self.sprite_zero_hit = 1
        self.vertical_blank = 1
        self.status_reg = 0

        #mask
        self.grayscale = 1
        self.render_background_left = 1
        self.render_sprites_left = 1
        self.render_background = 1
        self.render_sprites = 1
        self.enhance_red = 1
        self.enhance_green = 1
        self.enhance_blue = 1

        self.nmi = False
        self.mask_reg = 0

        #control
        self.nametable_x = 1
        self.nametable_y = 1
        self.increment_mode = 1
        self.pattern_sprite = 1
        self.pattern_background = 1
        self.sprite_size = 1
        self.slave_mode = 1 # unused
        self.enable_nmi = 1
        self.control_reg = 0

        self.addr_latch = 0x00
        self.ppu_data_buffer = 0x00
        self.ppu_addr = 0x0000

        #loop Register
        self.loop = {
            "coarse_x": 5,
            "coarse_y": 5,
            "nametable_x": 1,
            "nametable_y": 1,
            "fine_y": 3,
            "unused": 1,
            "reg": 0x0000,
        }

        self.vram_addr = self.loop
        self.tram_addr = self.loop


        self.fine_x = 0x00

        self.bg_next_tile_id     = 0x00
        self.bg_next_tile_attrib = 0x00
        self.bg_next_tile_lsb    = 0x00
        self.bg_next_tile_msb    = 0x00


        self.bg_shifter_pattern_lo = 0x0000
        self.bg_shifter_pattern_hi = 0x0000
        self.bg_shifter_attrib_lo  = 0x0000
        self.bg_shifter_attrib_hi  = 0x0000


        # self.coarse_x = 5
        # self.coarse_y = 5
        # self.nametable_x = 1
        # self.nametable_y = 1
        # self.fine_y = 3
        # self.unused = 1
        # self.reg = 0x0000
        




        self.palScreen = [0] * 64
        self.sprNameTable = [0] *2
        # self.sprPatternTable = [0] *2
        self.sprPatternTable = [pygame.Rect(128, 128,2,2), pygame.Rect(128, 128,2,2)] 

        # self.width = 512 + 300
        # self.height = 448 

        self.nSelectedPalette = 0x00
        self.width = 256 + 300
        self.height = 240

        self.screen = pygame.display.set_mode([self.width, self.height])
        self.screen.fill((0,0,118), (341,0, 300, 240))
        pygame.display.set_caption('NES Emulator by 4.444')
        self.my_font = pygame.font.Font('PressStart2P.ttf', 10)
        self.tiles = pygame.sprite.Group()

        pygame.display.flip()


        #palScreen colors

        self.palScreen[0x00] = (84, 84, 84)
        self.palScreen[0x01] = (0, 30, 116)
        self.palScreen[0x02] = (8, 16, 144)
        self.palScreen[0x03] = (48, 0, 136)
        self.palScreen[0x04] = (68, 0, 100)
        self.palScreen[0x05] = (92, 0, 48)
        self.palScreen[0x06] = (84, 4, 0)
        self.palScreen[0x07] = (60, 24, 0)
        self.palScreen[0x08] = (32, 42, 0)
        self.palScreen[0x09] = (8, 58, 0)
        self.palScreen[0x0A] = (0, 64, 0)
        self.palScreen[0x0B] = (0, 60, 0)
        self.palScreen[0x0C] = (0, 50, 60)
        self.palScreen[0x0D] = (0, 0, 0)
        self.palScreen[0x0E] = (0, 0, 0)
        self.palScreen[0x0F] = (0, 0, 0)

        self.palScreen[0x10] = (152, 150, 152)
        self.palScreen[0x11] = (8, 76, 196)
        self.palScreen[0x12] = (48, 50, 236)
        self.palScreen[0x13] = (92, 30, 228)
        self.palScreen[0x14] = (136, 20, 176)
        self.palScreen[0x15] = (160, 20, 100)
        self.palScreen[0x16] = (152, 34, 32)
        self.palScreen[0x17] = (120, 60, 0)
        self.palScreen[0x18] = (84, 90, 0)
        self.palScreen[0x19] = (40, 114, 0)
        self.palScreen[0x1A] = (8, 124, 0)
        self.palScreen[0x1B] = (0, 118, 40)
        self.palScreen[0x1C] = (0, 102, 120)
        self.palScreen[0x1D] = (0, 0, 0)
        self.palScreen[0x1E] = (0, 0, 0)
        self.palScreen[0x1F] = (0, 0, 0)

        self.palScreen[0x20] = (236, 238, 236)
        self.palScreen[0x21] = (76, 154, 236)
        self.palScreen[0x22] = (120, 124, 236)
        self.palScreen[0x23] = (176, 98, 236)
        self.palScreen[0x24] = (228, 84, 236)
        self.palScreen[0x25] = (236, 88, 180)
        self.palScreen[0x26] = (236, 106, 100)
        self.palScreen[0x27] = (212, 136, 32)
        self.palScreen[0x28] = (160, 170, 0)
        self.palScreen[0x29] = (116, 196, 0)
        self.palScreen[0x2A] = (76, 208, 32)
        self.palScreen[0x2B] = (56, 204, 108)
        self.palScreen[0x2C] = (56, 180, 204)
        self.palScreen[0x2D] = (60, 60, 60)
        self.palScreen[0x2E] = (0, 0, 0)
        self.palScreen[0x2F] = (0, 0, 0)

        self.palScreen[0x30] = (236, 238, 236)
        self.palScreen[0x31] = (168, 204, 236)
        self.palScreen[0x32] = (188, 188, 236)
        self.palScreen[0x33] = (212, 178, 236)
        self.palScreen[0x34] = (236, 174, 236)
        self.palScreen[0x35] = (236, 174, 212)
        self.palScreen[0x36] = (236, 180, 176)
        self.palScreen[0x37] = (228, 196, 144)
        self.palScreen[0x38] = (204, 210, 120)
        self.palScreen[0x39] = (180, 222, 120)
        self.palScreen[0x3A] = (168, 226, 144)
        self.palScreen[0x3B] = (152, 226, 180)
        self.palScreen[0x3C] = (160, 214, 228)
        self.palScreen[0x3D] = (160, 162, 160)
        self.palScreen[0x3E] = (0, 0, 0)
        self.palScreen[0x3F] = (0, 0, 0)

    def getScreen(self):
        return self.screen

    def getNameTable(self, i):
        return self.sprNameTable[i]

    def getPatternTable(self, i, pallete):
        for y in range(16):
            for x in range(16):
                n = y * 256 + x * 16

                for row in range(8):
                    tile_lsb = self.ppu_read(i * 0x1000 + n + row + 0)
                    tile_msb = self.ppu_read(i * 0x1000 + n + row + 8)
                    for col in range(8):
                        pixel = (tile_lsb & 0x01) + (tile_msb & 0x01)
                        tile_lsb >>=1
                        tile_msb >>=1

                        self.sprPatternTable[i] = x * 8 + (7 - col), y * 8 + row
                        self.getColourFromPaletteRam(pallete, pixel)

        return self.sprPatternTable[i]

    def getColourFromPaletteRam(self, pallete, pixel):
        return self.palScreen[self.ppu_read(0x3F00 + (pallete << 2) + pixel) & 0x3F]


    def clear(self):
        self.screen.fill((0,0,118), (341,0, 300, 230))

    def draw(self, status, pc, a, x, y, stack, opcode, ram):
        self.clear()
        status = self.my_font.render(f'STATUS:  {hex(status)}', False, (255, 255, 255))
        self.screen.blit(status, (342,5))
        pc = self.my_font.render(f'PC:      {hex(pc)}', False, (255, 255, 255))
        self.screen.blit(pc, (342,25))
        a = self.my_font.render(f'A:       {hex(a)}', False, (255, 255, 255))
        self.screen.blit(a, (342,50))
        x = self.my_font.render(f'X:       {hex(x)}', False, (255, 255, 255))
        self.screen.blit(x, (342,75))
        y = self.my_font.render(f'Y:       {hex(y)}', False, (255, 255, 255))
        self.screen.blit(y, (342,100))
        stack = self.my_font.render(f'STACK:   {hex(stack)}', False, (255, 255, 255))
        self.screen.blit(stack, (342,125))
        opcode = self.my_font.render(f'OPCODE:    {hex(opcode)}', False, (255, 255, 255))
        self.screen.blit(opcode, (342,150))
        addr = self.my_font.render(f'0x000', False, (255, 255, 255))
        self.screen.blit(addr, (342,175))
        ram = self.my_font.render(f'{ram}', False, (255, 255, 255))
        self.screen.blit(ram, (342,200))
        pygame.display.flip()

    def cpu_read(self, addr, readonly = False):
        data = 0x00

        if(addr == 0x0000): #control
            pass

        elif(addr == 0x0001): #mask
            pass

        elif(addr == 0x0002): #status
            data = (self.status_reg & 0xE0) | (self.ppu_data_buffer & 0x1F)
            self.vertical_blank = 0
            self.addr_latch = 0

        elif(addr == 0x0003): #OAM addr
            pass

        elif(addr == 0x0004): #OAM data
            pass

        elif(addr == 0x0005): #scroll
            pass

        elif(addr == 0x0006): #PPU addr
            pass

        elif(addr == 0x0007): #PPU data
            data = self.ppu_data_buffer
            self.ppu_data_buffer = self.ppu_read(self.vram_addr.reg)

            if(self.ppu_addr > 0x3F00):
                data = self.ppu_data_buffer

            if self.increment_mode:
                self.vram_addr.reg += 1
            else:
                self.ppu += 32
            #     data = self.ppu_data_buffer
            # self.ppu_addr += 1


        return data

    def cpu_write(self, addr, data):
        if(addr == 0x0000): #control
            self.control_reg = data
            self.tram_addr['nametable_x'] = self.nametable_x
            self.tram_addr['nametable_y'] = self.nametable_y

        elif(addr == 0x0001): #mask
            self.mask_reg = data

        elif(addr == 0x0002): #status
            pass

        elif(addr == 0x0003): #OAM addr
            pass

        elif(addr == 0x0004): #OAM data
            pass

        elif(addr == 0x0005): #scroll
            if(self.addr_latch == 0):
                self.fine_x = data & 0x07
                self.tram_addr['coarse_x'] = data >> 3
                self.addr_latch = 1
            else:
                self.tram_addr['fine_y'] = data & 0x07
                self.tram_addr['coarse_y'] = data >> 3
                self.addr_latch = 0

        elif(addr == 0x0006): #PPU addr
            if(self.addr_latch == 0):
                self.tram_addr['reg'] =  ((data & 0x003F) << 8) | (self.tram_addr['reg'] & 0x00FF)
                
                self.addr_latch = 1
            else:
                self.tram_addr['reg'] =  (self.tram_addr['reg'] & 0xFF00) | data
                self.vram_addr = self.tram_addr
                self.addr_latch = 0

        elif(addr == 0x0007): #PPU data
            self.ppu_write(self.vram_addr['reg'], data)
            if self.increment_mode:
                self.vram_addr['reg'] += 1
            else:
                self.ppu += 32


    # def ppu_read(self, addr, readonly = False):
    #     data = 0x00
    #     addr &= 0x3FFF
    #     if(self.cartucho.ppu_read(addr, data)):
    #        pass

    #     elif(addr >= 0x0000 and addr <= 0x1FFF):
    #         data = self.tblPattern[((addr & 0x1000) >> 12)][addr & 0x0FFF]

    #     elif(addr >= 0x2000 and addr <= 0x3EFF):
    #         if(self.cartucho.mirror == 'VERTICAL'):

    #             if (addr >= 0x0000 and addr <= 0x03FF):
    #                 data = self.tblName[0][addr & 0x03FF] 
    #             if (addr >= 0x0400 and addr <= 0x07FF):
    #                 data = self.tblName[1][addr & 0x03FF] 
    #             if (addr >= 0x0800 and addr <= 0x0BFF):
    #                 data = self.tblName[0][addr & 0x03FF] 
    #             if (addr >= 0x0C00 and addr <= 0x0FFF):
    #                 data = self.tblName[1][addr & 0x03FF] 

    #         elif(self.cartucho.mirror == 'HORIZONTAL'):

    #             if (addr >= 0x0000 and addr <= 0x03FF):
    #                 data = self.tblName[0][addr & 0x03FF] 
    #             if (addr >= 0x0400 and addr <= 0x07FF):
    #                 data = self.tblName[0][addr & 0x03FF] 
    #             if (addr >= 0x0800 and addr <= 0x0BFF):
    #                 data = self.tblName[1][addr & 0x03FF] 
    #             if (addr >= 0x0C00 and addr <= 0x0FFF):
    #                 data = self.tblName[1][addr & 0x03FF] 


    #     elif(addr >= 0x3F00 and addr <= 0x3FFF):
    #         addr &= 0x001F
    #         if(addr == 0x0010): addr = 0x0000
    #         if(addr == 0x0014): addr = 0x0004
    #         if(addr == 0x0018): addr = 0x0008
    #         if(addr == 0x001C): addr = 0x000C
    #         data = self.tblPalette[addr]
    #     return data

    def ppu_read(self, addr, readonly = False):
        data = 0x00
        print(hex(addr))
        addr &= 0x3FFF

        if(addr >= 0x0000 and addr <= 0x1FFF):
            data = self.tblPattern[((addr & 0x1000) >> 12)][addr & 0x0FFF]

        elif(addr >= 0x2000 and addr <= 0x3EFF):
            if(self.cartucho.mirror == 'VERTICAL'):

                if (addr >= 0x0000 and addr <= 0x03FF):
                    data = self.tblName[0][addr & 0x03FF] 
                if (addr >= 0x0400 and addr <= 0x07FF):
                    data = self.tblName[1][addr & 0x03FF] 
                if (addr >= 0x0800 and addr <= 0x0BFF):
                    data = self.tblName[0][addr & 0x03FF] 
                if (addr >= 0x0C00 and addr <= 0x0FFF):
                    data = self.tblName[1][addr & 0x03FF] 

            elif(self.cartucho.mirror == 'HORIZONTAL'):

                if (addr >= 0x0000 and addr <= 0x03FF):
                    data = self.tblName[0][addr & 0x03FF] 
                if (addr >= 0x0400 and addr <= 0x07FF):
                    data = self.tblName[0][addr & 0x03FF] 
                if (addr >= 0x0800 and addr <= 0x0BFF):
                    data = self.tblName[1][addr & 0x03FF] 
                if (addr >= 0x0C00 and addr <= 0x0FFF):
                    data = self.tblName[1][addr & 0x03FF] 


        elif(addr >= 0x3F00 and addr <= 0x3FFF):
            addr &= 0x001F
            if(addr == 0x0010): addr = 0x0000
            if(addr == 0x0014): addr = 0x0004
            if(addr == 0x0018): addr = 0x0008
            if(addr == 0x001C): addr = 0x000C
            data = self.tblPalette[addr]

        else:
            data = self.cartucho.ppu_read(addr, data)

        return data

    def ppu_write(self, addr, data):
        if(self.cartucho.ppu_write(addr, data)):
            pass

        elif(addr >= 0x0000 and addr <= 0x1FFF):
            self.tblPattern[(addr & 0x1000) >> 12][addr & 0x0FFF] = data

        elif(addr >= 0x2000 and addr <= 0x3EFF):
            if(self.cartucho.mirror == 'VERTICAL'):

                if (addr >= 0x0000 and addr <= 0x03FF):
                    self.tblName[0][addr & 0x03FF] = data
                if (addr >= 0x0400 and addr <= 0x07FF):
                    self.tblName[1][addr & 0x03FF] = data
                if (addr >= 0x0800 and addr <= 0x0BFF):
                    self.tblName[0][addr & 0x03FF] = data
                if (addr >= 0x0C00 and addr <= 0x0FFF):
                    self.tblName[1][addr & 0x03FF] = data
                    
            elif(self.cartucho.mirror == 'HORIZONTAL'):

                if (addr >= 0x0000 and addr <= 0x03FF):
                    self.tblName[0][addr & 0x03FF] = data
                if (addr >= 0x0400 and addr <= 0x07FF):
                    self.tblName[0][addr & 0x03FF] = data
                if (addr >= 0x0800 and addr <= 0x0BFF):
                    self.tblName[1][addr & 0x03FF] = data
                if (addr >= 0x0C00 and addr <= 0x0FFF):
                    self.tblName[1][addr & 0x03FF] = data

        elif(addr >= 0x3F00 and addr <= 0x3FFF):
            addr &= 0x001F
            if(addr == 0x0010): addr = 0x0000
            if(addr == 0x0014): addr = 0x0004
            if(addr == 0x0018): addr = 0x0008
            if(addr == 0x001C): addr = 0x000C
            self.tblPalette[addr] = data
        addr &= 0x3FFF
    
    def IncrementScrollX(self):
        if (self.render_background or self.render_sprites):
            if (self.vram_addr['coarse_x'] == 31):
                self.vram_addr['coarse_x'] = 0
                self.vram_addr['nametable_x'] = ~self.vram_addr['nametable_x']
            else:
                self.vram_addr['coarse_x'] += 1
    
    def IncrementScrollY(self):
        if (self.render_background or self.render_sprites):
            if (self.vram_addr['fine_y'] < 7):
                self.vram_addr['fine_y'] += 1
                
        else:
            self.vram_addr['fine_y'] = 0
            if (self.vram_addr['coarse_y'] == 29):
                self.vram_addr['coarse_y'] = 0
                self.vram_addr['nametable_y'] = ~self.vram_addr['nametable_y']

            elif (self.vram_addr['coarse_y'] == 31):
                self.vram_addr['coarse_y'] = 0

            else:
                self.vram_addr['coarse_y'] += 1



    def TransferAddressX(self):
        if (self.render_background or self.render_sprites):
           self.vram_addr['nametable_x'] = self.tram_addr['nametable_x']
           self.vram_addr['coarse_x']    = self.tram_addr['coarse_x']

    def TransferAddressY(self):
        if (self.render_background or self.render_sprites):
            self.vram_addr['fine_y']      = self.tram_addr['fine_y']
            self.vram_addr['nametable_y'] = self.tram_addr['nametable_y']
            self.vram_addr['coarse_y']    = self.tram_addr['coarse_y']
    
    def LoadBackgroundShifters(self):
        self.bg_shifter_pattern_lo = (self.bg_shifter_pattern_lo & 0xFF00) | self.bg_next_tile_lsb
        self.bg_shifter_pattern_hi = (self.bg_shifter_pattern_hi & 0xFF00) | self.bg_next_tile_msb
        
        if(self.bg_shifter_attrib_lo & 0xFF00) | (self.bg_next_tile_attrib & 0b01):
            self.bg_shifter_attrib_lo  = 0xFF
        else:
            self.bg_shifter_attrib_lo = 0x00

        if(self.bg_shifter_attrib_hi & 0xFF00) | (self.bg_next_tile_attrib & 0b10):
            self.bg_shifter_attrib_hi  = 0xFF
        else:
            self.bg_shifter_attrib_lo = 0x00
            
    def UpdateShifters(self):
        
        if (self.render_background):
            self.bg_shifter_pattern_lo <<= 1
            self.bg_shifter_pattern_hi <<= 1
            self.bg_shifter_attrib_lo <<= 1
            self.bg_shifter_attrib_hi <<= 1
		
	

    def clock(self):

        if self.scanline >= -1 and self.scanline < 240:
            if(self.scanline == -1 and self.cycle == 1):
                self.vertical_blank = 0

            if(self.cycle >= 2 and self.cycle < 258) or (self.cycle >= 321 and self.cycle < 338):
                self.UpdateShifters()

                if((self.cycle -1) % 8) == 0:
                    self.LoadBackgroundShifters()
                    self.bg_next_tile_id = self.ppu_read(0x2000 | (self.vram_addr['reg'] & 0x0FFF))

                elif((self.cycle -1) % 8) == 2:
                    if (self.vram_addr['coarse_y'] & 0x02):
                         self.bg_next_tile_attrib >>= 4
                    
                    if (self.vram_addr['coarse_x'] & 0x02): 
                        self.bg_next_tile_attrib >>= 2
                    self.bg_next_tile_attrib &= 0x03


                elif((self.cycle -1) % 8) == 4:
                    self.bg_next_tile_lsb = self.ppu_read((self.pattern_background << 12) + (self.bg_next_tile_id << 4) + (self.vram_addr['fine_y']) + 0)

                elif((self.cycle -1) % 8) == 6:
                    self.bg_next_tile_msb = self.ppu_read((self.pattern_background << 12) + (self.bg_next_tile_id << 4) + (self.vram_addr['fine_y']) + 8)

                elif((self.cycle -1) % 8) == 7:
                    self.IncrementScrollX()

            if (self.cycle == 256):
                self.IncrementScrollY()
            
            if (self.cycle == 257):
                self.LoadBackgroundShifters()
                self.TransferAddressX()
        
            if (self.cycle == 338 or self.cycle == 340):
            
                self.bg_next_tile_id = self.ppu_read(0x2000 | (self.vram_addr['reg'] & 0x0FFF))
		

            if(self.scanline == -1 and self.cycle >= 280 and self.cycle < 305):
                self.TransferAddressY()
		

        if(self.scanline == 240):
            pass

        if (self.scanline >= 241 and self.scanline < 261):
            if(self.scanline == 241 and self.cycle == 1):
                self.vertical_blank = 1
                if(self.enable_nmi):
                    self.nmi = True

        self.bg_pixel = 0x00
        self.bg_palette = 0x00

        if(self.render_background):
            bit_mux = 0x8000 >> self.fine_x

            p0_pixel = (self.bg_shifter_attrib_lo & bit_mux) > 0
            p1_pixel = (self.bg_shifter_attrib_hi & bit_mux) > 0

            self.bg_pixel = (p1_pixel << 1) | p0_pixel

            
            bg_pal0 = (self.bg_shifter_attrib_lo & bit_mux) > 0
            bg_pal1 = (self.bg_shifter_attrib_hi & bit_mux) > 0

            self.bg_palette = (bg_pal1 << 1) | bg_pal0


        #make noise
        # gfxdraw.pixel(self.screen, self.cycle - 1, self.scanline, self.palScreen[(randint(0,64) % 2) if 0x3F else 0x30])
        gfxdraw.pixel(self.screen, self.cycle - 1, self.scanline, self.getColourFromPaletteRam(self.bg_palette, self.bg_pixel))
        
        # for y in range(30):
        #     for x in range(32):
        #         id = self.tblName[0][y * 32 + x]
        #         tile = Tile((255,255,255),8, 8)
        #         tile.rect.x = y*16
        #         tile.rect.y = x*16
        #         self.tiles.add(tile)


                # self.clear()
                # self.tblFont = pygame.font.Font('PressStart2P.ttf', 8)
                # tbl = self.tblFont.render(hex(self.tblName[0][y*32+x]), False, (255, 255, 255))
                # self.screen.blit(tbl, (x*16, y*16))

                # pygame.draw.rect(tile, (255,255,255) [0,0,8,8])
                # gfxdraw.pixel(self.screen, x*16, y*16, self.getPatternTable(0, self.nSelectedPalette))



        self.cycle += 1
        if(self.cycle >= 341): #256
            self.cycle = 0
            self.scanline += 1
            if(self.scanline >= 261): #240
                self.scanline -=1
                self.frame_complete = True

    def incPalette(self):
        self.nSelectedPalette &= 0x07
