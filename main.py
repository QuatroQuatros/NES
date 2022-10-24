# from cpu import CPU

# cpu = CPU()

# while cpu.complete != 1:
#     cpu.clock()

import pygame, sys
from bus import BUS

# rom = 'jogos/Castlevania.nes'
#rom = 'jogos/teste.4444'
rom = 'jogos/DonkeyKong.nes'
#rom = 'jogos/SuperMarioBros.nes'
#rom = 'jogos/cpu_dummy_reads.nes'
bus = BUS(rom)

clock = pygame.time.Clock()

while bus.cpu.complete != 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bus.incPalette()

    bus.ppu.tiles.draw(bus.ppu.screen)
    clock.tick(60)
    pygame.display.flip()
    bus.clock()



