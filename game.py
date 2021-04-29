import pygame, sys, random

class Game():


    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(frequency = 44100,size = 16, channels = 1, buffer = 512) #pre-intitalize the mixer so othat there wont be any audio lag
        self.is_running = True
        self.is_playing = True
        self.width = 576
        self.height = 1024
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
        #game settings
        

        #score variables
        self.score = 0
        self.high_score = 0

        #font settings
        self.game_font = pygame.font.Font('04B_19__.ttf',40)

        #menu controls
        self.BACK_KEY = False #if BACK_KEY is pressed we want to 'pause' the game

        self.game_active = True
        print('Yoooooo')
        self.game_font = pygame.font.Font('04B_19__.ttf',40)

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
            high_score_rect = score_surface.get_rect(center = (288,850))
            self.screen.blit(high_score_surface,high_score_rect)

    def update_score(self):
        self.high_score = max(self.score,self.high_score)

    def game_loop(self):
        
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

            self.floor_x_pos -= 1
            self.draw_floor()
            if self.floor_x_pos <= -576:
                self.floor_x_pos = 0
            print('debug')
            
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.bird_movement = 0
                    self.bird_movement -= 8 #bird goes up
                    self.flap_sound.play()
            
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
                    
            if event.type == pygame.K_BACKSPACE:
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


def roto(bird,movement):
    new = pygame.transform.rotozoom(bird,-movement*3,1)
    return new