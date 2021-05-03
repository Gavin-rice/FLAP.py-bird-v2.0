import pygame, sys, random
from menu import Main_menu 

class Game():


    def __init__(self):

        #initialization
        pygame.init()
        pygame.mixer.pre_init(frequency = 44100,size = 16, channels = 1, buffer = 512) #pre-intitalize the mixer so othat there wont be any audio lag
        
        #game states
        self.is_running = True
        self.is_playing = True
        self.game_active = True
        #menu variables
        self.running = True
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

        #menu inputs
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

        #menu state
        self.menu_state = 'Start'

        self.is_start,self.is_other,self.is_options,self.is_credits = self.BLACK,self.WHITE,self.WHITE,self.WHITE
        #screen setup
        self.width = 576
        self.height = 1024
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
        #game settings
        self.display = pygame.Surface((self.width,self.height)) #defines a surface of the same size as the screen

        #score variables
        self.score = 0
        self.high_score = 0

        #menu setup
        self.title_surface = pygame.image.load('assets\logo.png').convert_alpha()
        self.title_surface = pygame.transform.scale(self.title_surface,(400,90))
        self.title_rect = self.title_surface.get_rect(center = (288,120))

        self.menu_index = 0
   
        self.main_menu = Main_menu(self)
        self.curr_menu = self.main_menu

        #menu controls
        self.BACK_KEY = False #if BACK_KEY is pressed we want to 'pause' the game

        
        #font stuff
        self.font_name = '04B_19__.ttf'

        self.game_font = pygame.font.Font(self.font_name,40)

        #BG image
        self.bg_surface = pygame.image.load('assets/background-day.png').convert() #intial temp background, convert makes it easier for pygame to run
        self.bg_surface = pygame.transform.scale2x(self.bg_surface) #doubles the size of the asset

        #floor
        self.floor_surface = pygame.image.load('assets/base.png').convert()
        self.floor_surface = pygame.transform.scale2x(self.floor_surface)
        self.floor_x_pos = 0

        #bird
        self.bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
        self.bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
        self.bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
        self.bird_frames = [self.bird_downflap,self.bird_midflap,self.bird_upflap] #we make a system such that it iterates through each sprite at appriate time
        self.bird_index = 0 #current animation index
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center = (100,512))
        self.rotated_bird = self.bird_surface
        #bird animation
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, 200) #200 ms


        #pipes
        self.pipe_surface = pygame.image.load('assets\pipe-green.png').convert()
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)
        self.pipe_list = []
        self.SPAWNPIPE = pygame.USEREVENT #event triggered by a timer and not user input
                             #full uppercase letters implies it is a custom trigger event
        pygame.time.set_timer(self.SPAWNPIPE,1200) #in ms so every 1.2 seconds, call SPAWNPIPE
        self.pipe_height = [400,600,800] #possible heights that a pipe can spawn at 

        #game variables
        self.gravity = 0.25
        self.bird_movement = 0
        #game over
        self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets\message.png').convert_alpha())
        self.game_over_rect = self.game_over_surface.get_rect(center = (288,512))
        #sond fx
        self.flap_sound = pygame.mixer.Sound('sounds\sound_sfx_wing.wav')
        self.death_sound = pygame.mixer.Sound('sounds\sound_sfx_hit.wav') #for pipe
        self.score_sound = pygame.mixer.Sound('sounds\sound_sfx_point.wav')



    '''
    def get_bg(self,is_day):
        print('yessir')
        if is_day:
            bg_surface = pygame.image.load('assets/background-day.png').convert() #intial temp background, convert makes it easier for pygame to run
            bg_surface = pygame.transform.scale2x(bg_surface) #doubles the size of the asset
        return bg_surface
    

    def draw_text(self,text, size, x, y):
        fo
    '''
    #menu methods
    
    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                pygame.quit()
                sys.exit()
                #self.curr_menu.run_display = False
            if event.type == self.BIRDFLAP:
                if self.menu_index < 5:
                    self.menu_index += 1
                else:
                    self.menu_index = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                    return True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                    return True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                    return True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                    return True
        return False
                

    #self.is_(the option)
    def draw_text(self,text,x,y,color):
        text_surface = self.game_font.render(text,True,color)
        text_rect = text_surface.get_rect(center = (x,y))

        self.screen.blit(text_surface,text_rect)
        

    #potentially add the 
    def reset_keys(self):
        self.UP_KEY,self.DOWN_KEY,self.START_KEY,self.BACK_KEY = False, False, False, False


    '''
    def main_menu_render(self):
        while True:
            self.screen.blit(self.bg_surface,(0,0))
            self.floor_x_pos -= 1
            self.draw_floor()
            if self.floor_x_pos <= -576:
                self.floor_x_pos = 0
            if self.menu_events():
                break
    '''


    def score_display(self,game_state):
        if game_state == 'main_game':
            score_surface = self.game_font.render(f'Score: {int(self.score)}',True,(255,255,255))
            score_rect = score_surface.get_rect(center = (288,100))
            self.screen.blit(score_surface,score_rect)
        if game_state == 'game_over':
            score_surface = self.game_font.render(f'Score: {int(self.score)}',True,(255,255,255))
            score_rect = score_surface.get_rect(center = (288,100))
            self.screen.blit(score_surface,score_rect)

            high_score_surface = self.game_font.render(f'High score: {int(self.high_score)}',True,(255,255,255))
            high_score_rect = score_surface.get_rect(center = (240,850))
            self.screen.blit(high_score_surface,high_score_rect)

    def update_score(self):
        self.high_score = max(self.score,self.high_score)

    
    #draws each option in the main menu
    def draw_buttons(self):
        self.draw_text("Start Game",288,350,self.is_start)
        self.draw_text("Other game modes", 288, 400, self.is_other)
        self.draw_text("Options", 288, 450, self.is_options)
        self.draw_text("Credits", 288, 500, self.is_credits)

        '''
        start_surface = self.game_font.render("Start Game",True,self.is_start)
        start_rect = start_surface.get_rect(center = (288,300))
        
        other_surface = self.game_font.render("Other game modes",True,self.is_other)
        other_rect = other_surface.get_rect(center = (288,350))

        #put on the screen
        self.screen.blit(start_surface,start_rect)
        self.screen.blit(other_surface,other_rect)
        '''


    def show_menu(self):
        while True:
            self.screen.blit(self.bg_surface,(0,0))
            
            menu_surface = self.game_font.render("Main Menu",True,self.WHITE)
            main_menu_rect = menu_surface.get_rect(center = (288,150))
            self.screen.blit(menu_surface,main_menu_rect)
            self.draw_buttons()
            self.draw_floor()
            self.floor_x_pos -= 1
            if self.floor_x_pos <= -576:
                self.floor_x_pos = 0
                #print('debug')
                
                #update game
            pygame.display.update()
            self.clock.tick(120)
            closer = self.menu_events()
            if closer:
                print('debug')
                self.reset_keys()
                break

        

    def game_loop(self):

        '''
        while self.running:
            self.show_menu()
        '''
        while self.is_playing:
            self.check_events()


        #load bg
            self.screen.blit(self.bg_surface,(0,0))
            
            if self.game_active:
            #bird movement
                self.bird_movement += self.gravity
                #rotated_bird = rotate_bird(self.bird_surface)
                self.rotated_bird = roto(self.bird_surface,self.bird_movement)
                self.bird_rect.centery += self.bird_movement
                self.screen.blit(self.rotated_bird,self.bird_rect)

                #pipe movement
                self.pipe_list = self.move_pipes(self.pipe_list)
                self.draw_pipes(self.pipe_list)

                self.score += 0.01
                self.score_display('main_game')
                self.game_active = self.check_collision(self.pipe_list)
            else:
                self.screen.blit(self.game_over_surface,self.game_over_rect)
                self.update_score()
                self.score_display('game_over')
            
            #floor movement

            
            self.draw_floor()
            self.floor_x_pos -= 1
            if self.floor_x_pos <= -576:
                self.floor_x_pos = 0
            #print('debug')
            
            #update game
            pygame.display.update()
            self.clock.tick(120)

    #bad function
    def rotate_bird(self,bird):
        new_bird = pygame.transform.rotozoom(bird,-self.bird_movement*3,1)
        return new_bird

    

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running, self.is_playing = False, False
                pygame.quit()
                sys.exit()
            #for menu movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True    
            #when you are in the game loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.bird_movement = 0
                    self.bird_movement -= 8 #bird goes up
                    self.flap_sound.play()
            
            #when you are dead and are trying to restart the game
            if event.type == pygame.KEYDOWN and self.game_active == False:
                self.game_active = True
                self.pipe_list.clear()
                self.bird_rect.center = (100,512)
                self.bird_movement = 0
                self.score = 0
                
            if event.type == self.SPAWNPIPE:
                self.pipe_list.extend(self.create_pipe())

            if event.type == self.BIRDFLAP:
                if self.bird_index < 2: #prevents overflow
                    self.bird_index += 1
                else:
                    self.bird_index = 0 #sdasd
                self.bird_surface, self.bird_rect = self.bird_animation()
                    
            if event.type == pygame.K_BACKSPACE: #when we want to exit to the main menu/pause
                self.BACK_KEY = True

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop = (700,random_pipe_pos)) 
        top_pipe = self.pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))#render the rect in the exact middle of the screen
        return bottom_pipe, top_pipe

    def move_pipes(self,pipes):
        for pipe in pipes:
            pipe.centerx -= 5
        return pipes

    #flying animation (vertical)
    def bird_animation(self):
        new_bird = self.bird_frames[self.bird_index]
        new_bird_rect = new_bird.get_rect(center = (100,self.bird_rect.centery))
        return new_bird,new_bird_rect

    #FIND SOME WAY TO DELETE THE FIRST PIPE IN pipe_list to improve performance
    def draw_pipes(self,pipes):
        for pipe in pipes:
            if pipe.bottom >= 1024:
                self.screen.blit(self.pipe_surface,pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface,False,True)
                self.screen.blit(flip_pipe,pipe)
        

    #collision checking
    def check_collision(self,pipes):
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe):
                self.death_sound.play()

                return False
        if self.bird_rect.top <= -100 or self.bird_rect.bottom >= 900:
            self.death_sound.play()
            return False

        return True

    def draw_floor(self):
        self.screen.blit(self.floor_surface,(self.floor_x_pos,900))
        self.screen.blit(self.floor_surface,(self.floor_x_pos + 576,900))

#external functions
def roto(bird,movement):
    new = pygame.transform.rotozoom(bird,-movement*3,1)
    return new