from game import Game
  

print('Game has started')
g = Game()

while g.is_running:

    g.game_loop() 