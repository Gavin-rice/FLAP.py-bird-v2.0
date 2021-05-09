import pygame, sys

'''from game import Game'''


class Menu():
    def __init__(self, game):
        self.game = game
        self.menu_game_state = "Start"
        self.run_display = True
        self.main_on,self.other_on,self.options_on,self.credits_on = True, False, False, False
        self.menu_heights = [125,120,115,115,120,125]

    def update_menu(self):
        #self.game.screen.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_keys()

    def animate_title(self):
        
        self.game.title_rect = self.game.title_surface.get_rect(center = (258,self.menu_heights[self.game.menu_index]))
        self.game.screen.blit(self.game.title_surface,self.game.title_rect)
        self.game.menu_bird_surface = self.game.bird_frames[self.game.menu_bird_index]
        self.game.screen.blit(self.game.menu_bird_surface,self.game.menu_bird_rect)


class Main_menu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = 'Start'
        



    def move_selector(self):
        if self.game.DOWN_KEY:
            if self.state == "Quit":
                self.game.is_quit = self.game.WHITE
                self.game.is_start = self.game.BLACK
                self.state = "Start"
                #
                # .print('DOWN')
            elif self.state == "Start":
                self.game.is_start = self.game.WHITE
                self.game.is_other = self.game.BLACK
                self.state = "Other"
            elif self.state == "Other":
                self.game.is_other = self.game.WHITE
                self.game.is_options = self.game.BLACK
                self.state = "Options"
            elif self.state == "Options":
                self.game.is_options = self.game.WHITE
                self.game.is_credits = self.game.BLACK
                self.state = "Credits"
            elif self.state == "Credits":
                self.game.is_credits = self.game.WHITE
                self.game.is_quit = self.game.BLACK
                self.state = "Quit"
            
        if self.game.UP_KEY:
            if self.state == "Start":
                self.game.is_start = self.game.WHITE
                self.game.is_quit = self.game.BLACK
                self.state = "Quit"
            elif self.state == "Other":
                self.game.is_other = self.game.WHITE
                self.game.is_start = self.game.BLACK
                self.state = "Start"
            elif self.state == "Options":
                self.game.is_options = self.game.WHITE
                self.game.is_other = self.game.BLACK
                self.state = "Other"
            elif self.state == "Credits":
                self.game.is_credits = self.game.WHITE
                self.game.is_options = self.game.BLACK
                self.state = "Options"
            elif self.state == "Quit":
                self.game.is_quit = self.game.WHITE
                self.game.is_credits = self.game.BLACK
                self.state = "Credits"
                
    def main_menu_inputs(self):
        self.move_selector()
        if self.game.START_KEY:
            if self.state == "Start":
                self.run_display = False
                self.game.playing = True
            elif self.state == "Other":
                print("Other Game Modes")
                self.run_display = False
                self.game.curr_menu = self.game.other
                self.run_display = True
                self.game.curr_menu.display_menu()
            elif self.state == "Options":
                print("Options")
                self.run_display = False
                self.game.curr_menu = self.game.options
                self.run_display = True
                self.game.curr_menu.display_menu()
            elif self.state == "Credits":
                print("Credits")
            elif self.state == "Quit":
                self.game.running, self.game.playing = False, False
                pygame.quit()
                sys.exit()

            #self.run_display = False


        

    def draw_buttons(self):
        self.game.draw_text("Start Game",288,350,self.game.is_start)
        self.game.draw_text("Other game modes", 288, 400, self.game.is_other)
        self.game.draw_text("Options", 288, 450, self.game.is_options)
        self.game.draw_text("Credits", 288, 500, self.game.is_credits)
        
        self.game.draw_text("Quit Game",288,600,self.game.is_quit)

        '''
        start_surface = self.game_font.render("Start Game",True,self.is_start)
        start_rect = start_surface.get_rect(center = (288,300))
        
        other_surface = self.game_font.render("Other game modes",True,self.is_other)
        other_rect = other_surface.get_rect(center = (288,350))

        #put on the screen
        self.screen.blit(start_surface,start_rect)
        self.screen.blit(other_surface,other_rect)
        '''

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.update_menu()
            self.game.screen.blit(self.game.bg_surface,(0,0))
            #self.game.screen.blit(self.game.title_surface,self.game.title_rect)
            #self.animate_menu()
            self.animate_title()
            how_to_play_surface = self.game.game_font.render('Arrow buttons to scroll\n',True,self.game.WHITE)
            enter_surface = self.game.game_font.render('Enter button to select',True,self.game.WHITE)
            jump_surface = self.game.game_font.render('Space button to flap',True,self.game.WHITE)

            #HOW TO PLAY
            how_to_surface = self.game.game_font.render('HOW TO PLAY:',True,self.game.RED)
            how_to_rect = how_to_surface.get_rect(center = (288,680))
            self.game.screen.blit(how_to_surface,how_to_rect)

            #print('testing')
            how_to_play_rect = how_to_play_surface.get_rect(center = (288,750))
            enter_rect = enter_surface.get_rect(center = (288,800))
            jump_rect = jump_surface.get_rect(center = (288,850))
            self.game.screen.blit(how_to_play_surface,how_to_play_rect)
            self.game.screen.blit(enter_surface,enter_rect)
            self.game.screen.blit(jump_surface,jump_rect)
            
            menu_surface = self.game.Menu_font.render('Main Menu',True,self.game.WHITE)
            main_menu_rect = menu_surface.get_rect(center = (288,230))
            self.game.screen.blit(menu_surface,main_menu_rect)
            self.draw_buttons()
            self.game.draw_floor()
            self.game.floor_x_pos -= 1
            if self.game.floor_x_pos <= -576:
                self.game.floor_x_pos = 0
                #print('debug')
                
                #update game
            #pygame.display.update()
            self.game.clock.tick(120)
            closer = self.game.menu_events()
            self.main_menu_inputs()
            

            if closer:
                #print('debug')
                self.run_display = False
                #self.game.reset_keys()
                break

class Other_games_menu(Menu):
    def __init__(self,game):
        Menu.__init__(self, game)
        self.state = "Night"
        self.is_night = self.game.BLACK
        self.is_challenge = self.game.WHITE
        self.is_return = self.game.WHITE

    def draw_buttons(self):
        self.game.draw_text("Night Mode",288,350,self.is_night)
        self.game.draw_text("Challenge Mode",288,400,self.is_challenge)

        self.game.draw_text("Main menu",288,500,self.is_return)

    def display_menu(self):
        self.run_display = True
        self.game.menu_state = "Other"
        while self.run_display:
            self.update_menu()
            self.game.screen.blit(self.game.bg_surface,(0,0))

            self.animate_title()
            
            menu_surface = self.game.game_font.render('Other Game Modes Menu',True,self.game.WHITE)
            main_menu_rect = menu_surface.get_rect(center = (288,230))
            self.game.screen.blit(menu_surface,main_menu_rect)
            self.draw_buttons()
            self.game.draw_floor()
            self.game.floor_x_pos -= 1
            if self.game.floor_x_pos <= -576:
                self.game.floor_x_pos = 0

            self.game.clock.tick(120)
            closer = self.game.menu_events()
            self.menu_input()

            if closer:
                
                break


    def move_selector(self):
        if self.game.DOWN_KEY:
            #print('down')
            if self.state == 'Night':
                self.is_night = self.game.WHITE
                self.is_challenge = self.game.BLACK
                self.state = 'Challenge'
            elif self.state == 'Challenge':
                self.is_challenge = self.game.WHITE
                self.is_return = self.game.BLACK
                self.state = 'Return'
            elif self.state == 'Return':
                self.is_return = self.game.WHITE
                self.is_night = self.game.BLACK
                self.state = 'Night'
        if self.game.UP_KEY:
            #print("up")
            if self.state == 'Night':
                self.is_night = self.game.WHITE
                self.is_return = self.game.BLACK
                self.state = 'Return'
            elif self.state == 'Challenge':
                self.is_challenge = self.game.WHITE
                self.is_night = self.game.BLACK
                self.state = 'Night'
            elif self.state == 'Return':
                self.is_return = self.game.WHITE
                self.is_challenge = self.game.BLACK
                self.state = 'Challenge'




    def menu_input(self):
        self.move_selector()
        if self.game.START_KEY:
            if self.state == "Night":
                self.game.bg_surface = self.game.bg_night_surface
                self.game.playing = True
            elif self.state == "Challenge":
                print("Challenge Mode")
            elif self.state == "Return":
                self.run_display = False
                self.game.curr_menu = self.game.main_menu
                self.run_display = True
                self.game.curr_menu.display_menu()

class Options_menu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = "Volume"
        self.names = ["Volume","Colour","Test","Test1"]
        self.descripts = ["Volume controls", "Change bird color", "Test text", "Test text 1"]
        self.name_colours = [self.game.BLACK,self.game.WHITE,self.game.WHITE,self.game.WHITE]
        self.menu_index = 0
        

    def draw_buttons(self):
        self.game.draw_text(self.descripts[0],288,350,self.name_colours[0])
        self.game.draw_text(self.descripts[1],288,400,self.name_colours[1])
        self.game.draw_text(self.descripts[2],288,450,self.name_colours[2])
        self.game.draw_text(self.descripts[3],288,500,self.name_colours[3])


    def display_menu(self):

        self.game.menu_state = "Options"
        self.run_display = True
        
        while self.run_display:
            self.update_menu()
            self.game.screen.blit(self.game.bg_surface,(0,0))

            self.animate_title()
            
            menu_surface = self.game.game_font.render('Options Menu',True,self.game.WHITE)
            main_menu_rect = menu_surface.get_rect(center = (288,230))
            self.game.screen.blit(menu_surface,main_menu_rect)
            self.draw_buttons()
            self.game.draw_floor()
            self.game.floor_x_pos -= 1
            if self.game.floor_x_pos <= -576:
                self.game.floor_x_pos = 0

            self.game.clock.tick(120)
            closer = self.game.menu_events()
            self.menu_input()

            if closer:
                
                break
        pass

    def move_selector(self):
        pass

    def menu_input(self):
        self.move_selector()
        if game.START_KEY:
            pass
        pass

class Credits(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Roll"

    def display_menu(self):
        pass


class Pause_menu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = "Paused"

    def display_menu(self):
        pass

    def check_input(self):
        pass