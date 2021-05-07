from game import *
  
if __name__ == "__main__":
    print('Game has started')
    g = Game()

    while g.is_running:
        g.curr_menu.display_menu()
        #print('Gamer')
        #g.show_menu()
        g.game_loop() 
    