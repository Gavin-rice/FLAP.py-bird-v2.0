import pygame, sys, random
from menu import *
from time import sleep

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
        self.playing = False
        self.BLACK, self.WHITE, self.RED = (0, 0, 0), (255, 255, 255), (255,0,0)

        #menu inputs
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY = False, False, False, False, False
        
        #menu state
        self.menu_state = 'Start'

        #score variables
        self.show_scores = False

        self.is_high_score, self.is_quit = self.WHITE,self.WHITE

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
        #Main menu start point

        self.main_menu = Main_menu(self)



        #challenge game mode set up
        self.is_challenge, self.is_challenge_running = False, False

        
        #load the coin sprites
        self.front_coin = pygame.transform.scale((pygame.image.load('assets/coin-front.png').convert_alpha()),(100,100))
        self.coin_tilt_1 = pygame.transform.scale((pygame.image.load('assets/coin-tilt-1.png').convert_alpha()),(100,100))
        self.coin_tilt_2 = pygame.transform.scale((pygame.image.load('assets/coin-tilt-2.png').convert_alpha()),(100,100))
        self.coin_side = pygame.transform.scale((pygame.image.load('assets/coin-side.png').convert_alpha()),(100,100))

        #blank png of for coin
        self.no_coin = pygame.transform.scale((pygame.image.load('assets/BLANK.png').convert_alpha()),(100,100))
        self.is_coin = True


        self.coin_frames = [self.front_coin,self.coin_tilt_1,self.coin_tilt_2,self.coin_side]

        self.coin_index = 0
        self.coin_surface = self.coin_frames[self.coin_index]


        # Challenge mode score
        self.challenge_score = 0
        self.challenge_hs = 0
        self.is_challenge_hs = self.WHITE

        #coin mechanics
        self.coin_list = []
        self.coin_heights = [450,475,500,600]

        #menu controls
        self.BACK_KEY = False #if BACK_KEY is pressed we want to 'pause' the game

        #Other menus
        self.other = Other_games_menu(self)
        self.options = Options_menu(self)
        self.credits = Credits(self)
        self.curr_menu = self.main_menu
        #font stuff
        self.font_name = '04B_19__.ttf'
        #credit font
        self.credit_name = 'EightBitDragon-anqx.ttf'
        self.credit_font = pygame.font.Font(self.credit_name,36) 
        self.credit_mini_font = pygame.font.Font(self.credit_name,18)
        self.game_font = pygame.font.Font(self.font_name,40)
        self.Menu_font = pygame.font.Font(self.font_name,76)

        #BG image
        self.bg_day_surface = pygame.image.load('assets/background-day.png').convert() #intial temp background, convert makes it easier for pygame to run
        self.bg_day_surface = pygame.transform.scale2x(self.bg_day_surface) #doubles the size of the asset
        self.bg_surface = self.bg_day_surface
        self.bg_night_surface = pygame.image.load('assets/background-night.png')
        self.bg_night_surface = pygame.transform.scale2x(self.bg_night_surface)
        #floor
        self.floor_surface = pygame.image.load('assets/base.png').convert()
        self.floor_surface = pygame.transform.scale2x(self.floor_surface)
        self.floor_x_pos = 0

        #bird
        self.bird_colour = 'BLUE'

        #BLUE BIRD
        self.bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
        self.bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
        self.bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
        #RED BIRD
        self.red_bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-downflap.png').convert_alpha())
        self.red_bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-midflap.png').convert_alpha())
        self.red_bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-upflap.png').convert_alpha())
        
        self.BLUE_frames = [self.bird_downflap,self.bird_midflap,self.bird_upflap]
        
        self.RED_frames = [self.red_bird_downflap,self.red_bird_midflap,self.red_bird_upflap]
        
        
        self.bird_frames = [self.bird_downflap,self.bird_midflap,self.bird_upflap] #we make a system such that it iterates through each sprite at appriate time
        self.bird_index = 0 #current animation index
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center = (100,512))
        self.rotated_bird = self.bird_surface



        #pipes
        self.pipe_surface = pygame.image.load('assets\pipe-green.png').convert()
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)
        self.pipe_list = []
        self.SPAWNPIPE = pygame.USEREVENT #event triggered by a timer and not user input
                             #full uppercase letters implies it is a custom trigger event
        pygame.time.set_timer(self.SPAWNPIPE,1200) #in ms so every 1.2 seconds, call SPAWNPIPE
        self.pipe_height = [400,600,800] #possible heights that a pipe can spawn at 

                #bird animation
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, 200) #200 ms

        #game variables
        self.gravity = 0.25
        self.bird_movement = 0
        #game over
        self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets\message.png').convert_alpha())
        self.game_over_rect = self.game_over_surface.get_rect(center = (288,474))
        #sond fx
        self.flap_sound = pygame.mixer.Sound('sounds\sound_sfx_wing.wav')
        self.death_sound = pygame.mixer.Sound('sounds\sound_sfx_hit.wav') #for pipe
        self.score_sound = pygame.mixer.Sound('sounds\sound_sfx_point.wav')
        self.coin_sound = pygame.mixer.Sound('sounds\sound_sfx_coin.wav')

        self.menu_bird_index = 0
        self.menu_bird_surface = self.bird_frames[self.menu_bird_index]
        self.menu_bird_rect = self.menu_bird_surface.get_rect(center = (480,115))

                #coin animation
        self.SPAWNCOIN = pygame.USEREVENT + 2
        self.ROTATECOIN = pygame.USEREVENT + 3
        pygame.time.set_timer(self.ROTATECOIN,300)
        pygame.time.set_timer(self.SPAWNCOIN, 5000)

   



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
                
                if self.menu_bird_index < 2:
                    self.menu_bird_index += 1
                if self.menu_bird_index >= 2:
                    self.menu_bird_index = 0
                
                if self.menu_index < 5:
                    self.menu_index += 1
                else:
                    self.menu_index = 0

            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_SPACE:
                    self.SPACE_KEY = True
                    return True
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                    #return True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                    #return True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                    #return True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                    #return True
                return True
                
        return False
                

    #self.is_(the option)
    def draw_text(self,text,x,y,color):
        text_surface = self.game_font.render(text,True,color)
        text_rect = text_surface.get_rect(center = (x,y))

        self.screen.blit(text_surface,text_rect)
        
    def draw_creds(self,text,x,y,color):
        text_surface = self.credit_font.render(text,True,color)
        text_rect = text_surface.get_rect(center = (x,y))

        self.screen.blit(text_surface,text_rect)        
    #potentially add the 
    def reset_keys(self):
        self.UP_KEY,self.DOWN_KEY,self.START_KEY,self.BACK_KEY,self.SPACE_KEY = False, False, False, False, False


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


        if game_state == 'start':
            score_surface = self.game_font.render(f'Score: {int(self.score)}',True,(255,255,255))
            score_rect = score_surface.get_rect(center = (288,100))
            self.screen.blit(score_surface,score_rect)
        if game_state == 'main_game':
            score_surface = self.game_font.render(f'Score: {int(self.score)}',True,(255,255,255))
            score_rect = score_surface.get_rect(center = (288,100))
            self.screen.blit(score_surface,score_rect)
        if game_state == 'game_over' and self.show_scores:
            score_surface = self.game_font.render(f'Score: {int(self.score)}',True,(255,255,255))
            score_rect = score_surface.get_rect(center = (288,100))
            self.screen.blit(score_surface,score_rect)
            self.draw_text("Space bar to restart",288,780,self.WHITE)

            if self.score == self.high_score:
                high_score_surface = self.game_font.render(f'New High score!: {int(self.high_score)}',True,self.is_high_score)
                high_score_rect = score_surface.get_rect(center = (220,880))
                self.screen.blit(high_score_surface,high_score_rect)                
            else:
                high_score_surface = self.game_font.render(f'High score: {int(self.high_score)}',True,self.is_high_score)
                high_score_rect = score_surface.get_rect(center = (240,880))
                self.screen.blit(high_score_surface,high_score_rect)


    def challenge_score_display(self,game_state):
    

        if game_state == 'start':
            score_surface = self.game_font.render(f'Score: {int(self.challenge_score)}',True,(255,255,255))
            score_rect = score_surface.get_rect(center = (288,100))
            self.screen.blit(score_surface,score_rect)
        if game_state == 'main_game':
            score_surface = self.game_font.render(f'Score: {int(self.challenge_score)}',True,(255,255,255))
            score_rect = score_surface.get_rect(center = (288,100))
            self.screen.blit(score_surface,score_rect)
        if game_state == 'game_over' and self.show_scores:
            score_surface = self.game_font.render(f'Score: {int(self.challenge_score)}',True,(255,255,255))
            score_rect = score_surface.get_rect(center = (288,100))
            self.screen.blit(score_surface,score_rect)
            self.draw_text("Space bar to restart",288,780,self.WHITE)

            if self.score == self.high_score:
                high_score_surface = self.game_font.render(f'New High score!: {int(self.challenge_hs)}',True,self.is_challenge_hs)
                high_score_rect = score_surface.get_rect(center = (220,880))
                self.screen.blit(high_score_surface,high_score_rect)                
            else:
                high_score_surface = self.game_font.render(f'High score: {int(self.challenge_hs)}',True,self.is_challenge_hs)
                high_score_rect = score_surface.get_rect(center = (240,880))
                self.screen.blit(high_score_surface,high_score_rect)

    def update_score(self):
        self.high_score = max(self.score,self.high_score)
        if self.high_score == self.score:
            self.is_high_score = self.RED



    def update_score_challenge(self):
        self.challenge_hs = max(self.challenge_hs,self.challenge_score)
        if self.challenge_hs == self.challenge_score:
            self.is_challenge_hs = self.RED
    
    #draws each option in the main menu



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
        while self.playing:
            self.check_events()


        #load bg
            self.screen.blit(self.bg_surface,(0,0))
            
            #self.score_display('start')
            if self.game_active:
            #bird movement

                self.bird_movement += self.gravity
                #rotated_bird = rotate_bird(self.bird_surface)
                self.rotated_bird = roto(self.bird_surface,self.bird_movement)
                self.bird_rect.centery += self.bird_movement
                self.screen.blit(self.rotated_bird,self.bird_rect)

                #pipe movement
                self.pipe_list = self.move_pipes(self.pipe_list)

                #create a similair function for the coins

                self.draw_pipes(self.pipe_list)

                self.score += 0.01
                self.show_scores = False
                self.score_display('main_game')
                self.game_active = self.check_collision(self.pipe_list)
            else:
                self.screen.blit(self.game_over_surface,self.game_over_rect)
                self.update_score()
                self.show_scores = True
                self.score_display('game_over')
                self.show_scores = False
                

            
            #floor movement

            self.is_high_score = self.WHITE
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
            if event.type == pygame.KEYDOWN and self.playing:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True  
                if event.key == pygame.K_SPACE:
                    self.SPACE_KEY = True  
            #when you are in the game loop
            if event.type == pygame.KEYDOWN and self.playing:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.bird_movement = 0
                    self.bird_movement -= 8 #bird goes up
                    self.flap_sound.play()
                    self.SPACE_KEY = True
            
            #when you are dead and are trying to restart the game
            if event.type == pygame.KEYDOWN and self.game_active == False:
                if event.key == pygame.K_RETURN:
                    #self.game_over_surface = None
                    self.curr_menu.run_display = True
                    self.playing = False
                    #self.game_active = False
                    #self.curr_menu = self.main_menu
                    #print("hit")
                    
                    
                    self.curr_menu.display_menu()
                    self.reset_keys()
                    #self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets\message.png').convert_alpha())

                if event.key == pygame.K_SPACE:
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


    def check_events_challenge(self):
        #print('icy')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running, self.is_playing = False, False
                pygame.quit()
                sys.exit()
            #for menu movement
            if event.type == pygame.KEYDOWN and self.is_challenge_running: #changed from self.playing to is_challenge_running
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True  
                if event.key == pygame.K_SPACE:
                    self.SPACE_KEY = True  
            #when you are in the game loop
            if event.type == pygame.KEYDOWN and self.is_challenge_running:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.bird_movement = 0
                    self.bird_movement -= 8 #bird goes up
                    self.flap_sound.play()
                    self.SPACE_KEY = True
            
            #when you are dead and are trying to restart the game
            if event.type == pygame.KEYDOWN and self.game_active == False:
                if event.key == pygame.K_RETURN:
                    #self.game_over_surface = None
                    self.curr_menu.run_display = True
                    self.is_challenge_running = False
                    #self.game_active = False
                    #self.curr_menu = self.main_menu
                    #print("hit")
                    
                    
                    self.curr_menu.display_menu()
                    self.reset_keys()
                    #self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets\message.png').convert_alpha())

                if event.key == pygame.K_SPACE:
                    self.game_active = True
                    self.pipe_list.clear()
                    self.coin_list.clear()
                    self.bird_rect.center = (100,512)
                    self.bird_movement = 0
                    self.score = 0
                
            if event.type == self.SPAWNPIPE:
                if random.random() > 0.8:
                    pass
                self.pipe_list.extend(self.create_pipe())

            if event.type == self.ROTATECOIN:
                self.animate_coins()

            
            if event.type == self.SPAWNCOIN:
                if not self.is_coin:
                    self.is_coin = True
                    self.coin_surface = self.coin_frames[self.coin_index]
                self.coin_list.append(self.create_coins())

            if event.type == self.BIRDFLAP:
                if self.bird_index < 2: #prevents overflow
                    self.bird_index += 1
                else:
                    self.bird_index = 0 #sdasd
                self.bird_surface, self.bird_rect = self.bird_animation()
                    
            if event.type == pygame.K_BACKSPACE: #when we want to exit to the main menu/pause
                self.BACK_KEY = True

        


    def game_loop_challenge(self):
        while self.is_challenge_running:
            self.check_events_challenge()


        #load bg
            self.screen.blit(self.bg_surface,(0,0))
            #self.animate_coins()
            #self.score_display('start')
            if self.game_active:
            #bird movement

                self.bird_movement += self.gravity
                #rotated_bird = rotate_bird(self.bird_surface)
                self.rotated_bird = roto(self.bird_surface,self.bird_movement)
                self.bird_rect.centery += self.bird_movement
                self.screen.blit(self.rotated_bird,self.bird_rect)

                #pipe movement
                self.pipe_list = self.move_pipes(self.pipe_list)
                self.coin_list = self.move_coins(self.coin_list)
                #create a similair function for the coins

                self.draw_pipes(self.pipe_list)
                self.draw_coins(self.coin_list)

                self.challenge_score += 0.01
                self.show_scores = False
                self.challenge_score_display('main_game')
                self.check_collision_coin(self.coin_list)
                self.game_active = self.check_collision(self.pipe_list)
            else:
                self.screen.blit(self.game_over_surface,self.game_over_rect)
                self.update_score_challenge()
                self.show_scores = True
                self.challenge_score_display('game_over')
                self.show_scores = False
                

            
            #floor movement

            self.is_high_score = self.WHITE
            self.draw_floor()
            self.floor_x_pos -= 1
            if self.floor_x_pos <= -576:
                self.floor_x_pos = 0
            #print('debug')
            
            #update game
            pygame.display.update()
            self.clock.tick(120)   



    def create_coins(self):
        rand_coin_pos = random.choice(self.coin_heights)
        coin_sprite = self.coin_surface.get_rect(midtop = (700,rand_coin_pos))
        return coin_sprite

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop = (700,random_pipe_pos)) 
        top_pipe = self.pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))#render the rect in the exact middle of the screen
        return bottom_pipe, top_pipe


    def create_red_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop = (700,random_pipe_pos)) 
        top_pipe = self.pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 200))#render the rect in the exact middle of the screen
        return bottom_pipe, top_pipe

    def move_coins(self,coins):
        for coin in coins:
            coin.centerx -= 5
        return coins

    def move_pipes(self,pipes):
        #print(pipes)
        for pipe in pipes:
            #print(pipe.centerx)
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


    def draw_coins(self,coins):
        for coin in coins:
            
            self.screen.blit(self.coin_surface,coin)
        
    def check_collision_coin(self,coins):
        #print(coins)
        for coin in coins:
            if self.bird_rect.colliderect(coin):
                coin.centerx = -50 #remove the coin from ever touching thr bird again
                self.challenge_score += 5
                self.coin_sound.play()
                self.is_coin = False
                self.coin_surface = self.no_coin
                
                return
        
    def animate_coins(self):
        if self.coin_index >= (len(self.coin_frames) - 1):
            self.coin_index = 0
        self.coin_index += 1
        self.coin_surface = self.coin_frames[self.coin_index]
            

        

    #collision checking
    def check_collision(self,pipes):
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe):
                self.death_sound.play()

                return True #change to True to become invincible
        #if the player hits the ground or exits the screen -> game over
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