# from cpu import CPU

# cpu = CPU()

# while cpu.complete != 1:
#     cpu.clock()

import pygame, sys
from bus import BUS

# rom = 'jogos/Castlevania.nes'
#rom = 'jogos/teste.4444'
rom = 'jogos/Donkey Kong.nes'
bus = BUS(rom)


while bus.cpu.complete != 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
    bus.clock()
    pygame.display.flip()


