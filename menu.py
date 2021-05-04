import pygame







'''from game import Game'''


class Menu():
    def __init__(self, game):
        self.game = game
        self.menu_game_state = "Start"
        self.run_display = True
    
    #BLIT SCREEN method
    def update_menu(self):
        #self.game.screen.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_keys()


class Main_menu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = 'Start'
        self.menu_heights = [125,120,115,115,120,125]



    def menu_input(self):
        self.move_selector()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
            elif self.state == "Other":
                print("Other Game Modes")
            elif self.state == "Options":
                print("Options")
            elif self.state == "Credits":
                print("Credits")

    def move_selector(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
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
            elif self.state == "Crdits":
                self.game.is_credits = self.game.WHITE
                self.game.is_start = self.game.BLACK
                self.state = "Start"
        if self.game.UP_KEY:
            if self.state == "Start":
                self.game.is_start = self.game.WHITE
                self.game.is_credits = self.game.BLACK
                self.state = "Credits"
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
            

    def animate_title(self):
        
        self.game.title_rect = self.game.title_surface.get_rect(center = (258,self.menu_heights[self.game.menu_index]))
        self.game.screen.blit(self.game.title_surface,self.game.title_rect)
        

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.screen.blit(self.game.bg_surface,(0,0))
            #self.game.screen.blit(self.game.title_surface,self.game.title_rect)
            #self.animate_menu()

            self.animate_title()
            menu_surface = self.game.game_font.render('Main Menu',True,self.game.WHITE)
            main_menu_rect = menu_surface.get_rect(center = (288,230))
            self.game.screen.blit(menu_surface,main_menu_rect)
            self.game.draw_buttons()
            self.game.draw_floor()
            self.game.floor_x_pos -= 1
            if self.game.floor_x_pos <= -576:
                self.game.floor_x_pos = 0
                #print('debug')
                
                #update game
            pygame.display.update()
            self.game.clock.tick(120)
            closer = self.game.menu_events()
            self.menu_input()
            #print('testing')
            self.update_menu()
            if closer:
                print('debug')
                #self.game.reset_keys()
                break

class Other_game_modes(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Night"

    def display_menu(self):
        pass
    
    def menu_input(self):
        pass


class Options_menu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Volume"
    
    def display_menu(self):
        pass

    def menu_input(self):
        pass

class Credits(Menu):
    def __init__(self, game):
        Mene.__init__(self,game)

    def display_menu(self):
        pass    




 
'''
class Menu():

    def __init__(self,game):
        
        self.game = game
        self.state = "Start"
        self.menu_width, self.menu_height = (self.game.width/2),(self.game.height/2)
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.offset = -100


    def draw_cursor(self):
        self.game.draw_text('*',15,self.cursor_rect.x,self.cursor_rect.y) # call function from game class

    def blit_screen(self):
        self.game.screen.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_keys()


class Main_menu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = "Start"
        self.startx,self.starty = (self.menu_width),((self.menu_height) + 30) #for start game button
        self.optionsx,self.optionsy = (self.menu_width),((self.menu_height) + 50) #for options button
        self.creditsx,self.creditsy = (self.menu_width),((self.menu_height) + 70) #for credits button
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        
    def display_menu(self):
        self.run_display = True
        while self.run_display:

            self.game.menu_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.menu_width, self.menu_height)
            self.game.draw_text('Start Game', 20, self.startx, self.starty)
            self.game.draw_text('Options', 20, self.optionsx, self.optionsy)
            self.game.draw_text('Credits', 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()
            print("display events is running")

    #moves the cursor up or down depending on input from user
    def move_cursor(self):
        #down key input possibilities
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

        #up key input possibilities
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_Rect.midtop = (self.creditsx + self.offset,self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            
    #checks for enter onto a particular option in main menu
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                pass
            elif self.state == 'Credits':
                pass
            self.run_display = False


'''

