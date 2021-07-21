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
        self.game.show_scores = False
        self.game.bg_surface = self.game.bg_day_surface
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
                self.run_display = False
                self.game.curr_menu = self.game.credits
                self.game.curr_menu.display_menu()
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

            #self.game.game_over_surface = None
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
                #self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets\message.png').convert_alpha())
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


    def night_mode(self):
        self.game.bg_surface = self.game.bg_night_surface


    def menu_input(self):
        self.move_selector()
        if self.game.START_KEY:
            if self.state == "Night":
                self.night_mode()
                self.game.playing = True
            elif self.state == "Challenge":
                print("Challenge Mode")
                self.game.game_loop_challenge()
                self.run_display = False
                self.game.is_challenge_running = True
            elif self.state == "Return":
                self.game.bg_surface = self.game.bg_day_surface
                self.run_display = False
                self.game.curr_menu = self.game.main_menu
                self.run_display = True
                self.game.curr_menu.display_menu()

class Options_menu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        
        self.names = ["Volume","Colour","Test","Test1","Main"]
        self.state = self.names[0]
        self.descripts = ["Volume controls", "Change bird color", "Test text", "Test text 1","Main Menu"]
        self.name_colours = [self.game.BLACK,self.game.WHITE,self.game.WHITE,self.game.WHITE,self.game.WHITE]
        self.menu_index = 0
        

    def draw_buttons(self):

        self.game.draw_text(self.descripts[0],288,350,self.name_colours[0])
        self.game.draw_text(self.descripts[1],288,400,self.name_colours[1])
        self.game.draw_text(self.descripts[2],288,450,self.name_colours[2])
        self.game.draw_text(self.descripts[3],288,500,self.name_colours[3])

        self.game.draw_text(self.descripts[4],288,600,self.name_colours[4])

        


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
        l = len(self.names)
        if self.game.DOWN_KEY:
            if self.menu_index < (l - 1):
                self.name_colours[self.menu_index] = self.game.WHITE
                self.menu_index += 1
                self.state = self.names[self.menu_index]
                self.name_colours[self.menu_index] = self.game.BLACK
            elif self.menu_index == (l - 1):
                self.name_colours[self.menu_index] = self.game.WHITE
                self.menu_index = 0
                self.name_colours[self.menu_index] = self.game.BLACK
                pass
        if self.game.UP_KEY:
            if self.menu_index > 0:
                self.name_colours[self.menu_index] = self.game.WHITE
                self.menu_index -= 1
                self.state = self.names[self.menu_index]
                self.name_colours[self.menu_index] = self.game.BLACK
            elif self.menu_index == 0:
                self.name_colours[self.menu_index] = self.game.WHITE
                self.menu_index = (l - 1)
                self.name_colours[self.menu_index] = self.game.BLACK


    def menu_input(self):
        self.move_selector()
        if self.game.START_KEY:
            if self.state == "Volume":
                print("Volume control")
            elif self.state == "Colour":
                print("Colour")
                self.change_colour()
            elif self.state == "Test":
                print('Test')
            elif self.state == "Test1":
                print("Test1")
            elif self.state == "Main":
                print("main")
                self.run_display = False
                self.game.curr_menu = self.game.main_menu
                self.run_display = True
                self.game.curr_menu.display_menu()



    def change_colour(self):
        if self.game.bird_colour == "BLUE":
            self.game.bird_frames = self.game.RED_frames
            self.game.bird_colour = "RED"
        elif self.game.bird_colour == "RED":
            self.game.bird_frames = self.game.BLUE_frames
            self.game.bird_colour = 'BLUE'
        
class Credits(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Roll"
        self.creds_pos = 0

    def display_menu(self):
        self.run_display = True
        self.game.menu_state = "Credits"
        self.creds_pos = 0
        while self.run_display:
            self.update_menu()
            self.game.screen.blit(self.game.bg_surface,(0,0))

            
            
            
            self.game.draw_floor()
            self.draw_credits(self.creds_pos)
            self.creds_pos += 1
            self.game.floor_x_pos -= 1
            if self.game.floor_x_pos <= -576:
                self.game.floor_x_pos = 0
            if self.creds_pos > 1390:
                self.creds_pos = 0
                #self.game.START_KEY = True                 

            self.game.clock.tick(120)
            closer = self.game.menu_events()
            self.menu_input()

            if closer:
                print("yikes")
                break
        pass


    '''
            text_surface = self.game_font.render(text,True,color)
        text_rect = text_surface.get_rect(center = (x,y))

        self.screen.blit(text_surface,text_rect)
    
    '''

    def draw_credits(self,i):
        self.game.draw_creds("Developer",288,1030 - i,self.game.BLACK)
        self.game.draw_creds("Gavin Rice",288,1080 - i,self.game.WHITE)

        self.game.draw_creds("Source Code",288,1150 - i,self.game.BLACK)
        link = self.game.credit_mini_font.render("https://github.com/Gavin-rice/Flappy-Bird-v2",True,self.game.WHITE)
        link_rect = link.get_rect(center = (288,1200 - i))
        self.game.screen.blit(link,link_rect)

        self.game.draw_creds("Press enter to ",288,1300 - i, self.game.WHITE)
        self.game.draw_creds("return to menu",288,1350 - i, self.game.WHITE)


    
    def menu_input(self):
        if self.game.START_KEY:
            self.run_display = False
            self.game.curr_menu = self.game.main_menu
            self.run_display = True
            self.game.curr_menu.display_menu() 

class Pause_menu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = "Paused"



    def display_menu(self):
        pass

    def menu_input(self):
        pass
        