import pygame

from Game import Game
pygame.init()

if __name__ == "__main__":
    game:Game = Game()
    game.main()
pygame.quit ()