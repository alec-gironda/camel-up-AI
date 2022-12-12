from learn import *
import random
import time
import pygame
import copy as cp

board_state, camel_spots = shuffle_start()
bets_left = {1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]}
winner_bets_left = [8,5,3,2,1]
loser_bets_left = [8,5,3,2,1]
dice_left = set([1,2,3,4,5])

state = GameStateNode(board_state,dice_left,bets_left,camel_spots, winner_bets_left, loser_bets_left)

pygame.init()
screen_width  = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))

display_red_die = False
display_blue_die = False
display_green_die = False
display_yellow_die = False
display_white_die = False

red_die_number = -1
green_die_number = -1
blue_die_number = -1
white_die_number = -1
yellow_die_number = -1

p1_turn = True

p1 = Player()
perms = set_perms()
p2 = SmartPlayer("./new_model0",perms)
# p2 = MaxPlayer(perms)

players = [p1,p2]

which_camel = {"red":1,"yellow":2,"green":3,"blue":4,"white":5}
which_color = {1:"red",2:"yellow",3:"green",4:"blue",5:"white"}

yellow = pygame.image.load("./camel_pics/yellow.png")
yellow = pygame.transform.scale(yellow,(42,30))

red = pygame.image.load("./camel_pics/red.png")
red = pygame.transform.scale(red,(42,30))

green = pygame.image.load("./camel_pics/green.png")
green = pygame.transform.scale(green,(42,30))

blue = pygame.image.load("./camel_pics/blue.png")
blue = pygame.transform.scale(blue,(42,30))

white = pygame.image.load("./camel_pics/white.png")
white = pygame.transform.scale(white,(42,30))

roll_button_w = 100
roll_button_h = 50
roll_button_x = screen_width//2 - roll_button_w//2
roll_button_y = 2.5*screen_height//4

betting_card_w = 50
betting_card_h = 50
betting_card_y = screen_height//4.2

red_betting_card_x = 1.8*screen_width//5

blue_betting_card_x = 2.2*screen_width//5

yellow_betting_card_x = 2.6*screen_width//5

white_betting_card_x = 3*screen_width//5

green_betting_card_x = 3.4*screen_width//5

roll_button = pygame.Rect(roll_button_x,roll_button_y,roll_button_w,roll_button_h)

red_betting_card = pygame.Rect(red_betting_card_x,betting_card_y,betting_card_w,betting_card_h)
blue_betting_card = pygame.Rect(blue_betting_card_x,betting_card_y,betting_card_w,betting_card_h)
green_betting_card = pygame.Rect(green_betting_card_x,betting_card_y,betting_card_w,betting_card_h)
yellow_betting_card = pygame.Rect(yellow_betting_card_x,betting_card_y,betting_card_w,betting_card_h)
white_betting_card = pygame.Rect(white_betting_card_x,betting_card_y,betting_card_w,betting_card_h)

red_total_Wx = 1.8*screen_width//5
red_total_Lx = 1.8*screen_width//5

blue_total_Wx = 2.2*screen_width//5
blue_total_Lx = 2.2*screen_width//5

yellow_total_Wx = 2.6*screen_width//5
yellow_total_Lx = 2.6*screen_width//5

white_total_Wx = 3*screen_width//5
white_total_Lx = 3*screen_width//5

green_total_Wx = 3.4*screen_width//5
green_total_Lx = 3.4*screen_width//5

total_Wy = screen_height//3.1
total_Ly = screen_height//2.7

total_w = 50
total_h = 25

total_red_W = pygame.Rect(red_total_Wx,total_Wy,total_w,total_h)
total_red_L = pygame.Rect(red_total_Lx,total_Ly,total_w,total_h)

total_blue_W = pygame.Rect(blue_total_Wx,total_Wy,total_w,total_h)
total_blue_L = pygame.Rect(blue_total_Lx,total_Ly,total_w,total_h)

total_green_W = pygame.Rect(green_total_Wx,total_Wy,total_w,total_h)
total_green_L = pygame.Rect(green_total_Lx,total_Ly,total_w,total_h)

total_yellow_W = pygame.Rect(yellow_total_Wx,total_Wy,total_w,total_h)
total_yellow_L = pygame.Rect(yellow_total_Lx,total_Ly,total_w,total_h)

total_white_W = pygame.Rect(white_total_Wx,total_Wy,total_w,total_h)
total_white_L = pygame.Rect(white_total_Lx,total_Ly,total_w,total_h)

smallfont = pygame.font.SysFont('bahnschrift',35)
roll_button_text = smallfont.render('DICE' , True , (231,231,231))

start = time.time()

def draw_board(screen,screen_width,screen_height,display_red_die,display_blue_die,
               display_green_die, display_white_die,display_yellow_die,red_die_number,
               green_die_number,blue_die_number,white_die_number,yellow_die_number,
               state,yellow,red,green,blue,white,p1,p2,roll_button_x,roll_button_y,
               roll_button_w,roll_button_h,roll_button,smallfont,roll_button_text,
               red_betting_card_x,blue_betting_card_x,yellow_betting_card_x,green_betting_card_x,
               white_betting_card_x,betting_card_y,betting_card_w,betting_card_h,red_betting_card,
               blue_betting_card,yellow_betting_card,green_betting_card,white_betting_card,
               total_red_W,total_red_L,total_blue_W,total_blue_L,total_green_W,total_green_L,
               total_white_W,total_white_L,total_yellow_W,total_yellow_L):

    screen.fill((242,205,107))

    edge_top_out = pygame.Rect(0,0,screen_width,2*screen_height//80)
    edge_top_in = pygame.Rect(0,screen_height//5,screen_width,screen_height//80)
    edge_top_in2 = pygame.Rect(0,2*screen_height//5,screen_width,screen_height//80)
    edge_top_in3 = pygame.Rect(0,3*screen_height//5,screen_width,screen_height//80)
    edge_bottom_out = pygame.Rect(0,screen_height-2*screen_height//80,screen_width,2*screen_height//80)
    edge_bottom_in = pygame.Rect(0,screen_height-screen_height//80-screen_height//5,screen_width,screen_height//80)
    edge_left_out = pygame.Rect(0,0,2*screen_width//80,screen_height)
    edge_left_in = pygame.Rect(screen_width//5,0,screen_width//80,screen_height)
    edge_left_in2 = pygame.Rect(2*screen_width//5,0,screen_width//80,screen_height)
    edge_left_in3 = pygame.Rect(3*screen_width//5,0,screen_width//80,screen_height)
    edge_right_out = pygame.Rect(screen_width-2*screen_width//80,0,2*screen_width//80,screen_height)
    edge_right_in = pygame.Rect(screen_width-screen_width//80-screen_width//5,0,screen_width//80,screen_height)
    middle = pygame.Rect(screen_width//5+screen_height//80,screen_height//5 + screen_height//80,3*screen_width//5 -2*screen_width//80,3*screen_height//5 -2*screen_height//80)


    pygame.draw.rect(screen,(134,100,68),edge_top_out)
    pygame.draw.rect(screen,(134,100,68),edge_top_in)
    pygame.draw.rect(screen,(134,100,68),edge_top_in2)
    pygame.draw.rect(screen,(134,100,68),edge_top_in3)
    pygame.draw.rect(screen,(134,100,68),edge_bottom_out)
    pygame.draw.rect(screen,(134,100,68),edge_bottom_in)
    pygame.draw.rect(screen,(134,100,68),edge_left_out)
    pygame.draw.rect(screen,(134,100,68),edge_left_in)
    pygame.draw.rect(screen,(134,100,68),edge_left_in2)
    pygame.draw.rect(screen,(134,100,68),edge_left_in3)
    pygame.draw.rect(screen,(134,100,68),edge_right_out)
    pygame.draw.rect(screen,(134,100,68),edge_right_in)
    pygame.draw.rect(screen,(242,205,107),middle)


    stack_height = screen_height//40

    bottom_map = {9:4,10:3,11:2,12:1,13:0}
    right_map = {6:2.2,7:3.4,8:4.7}
    left_map = {14:4.7,15:3.4,16:2.2,16:2.2}
    finish_map = {17:0,18:1,19:2,20:3}

    if state.camel_spots[which_camel["yellow"]][0]<6:
        screen.blit(yellow,(screen_width//11 + (state.camel_spots[which_camel["yellow"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["yellow"]][1]*stack_height))
    elif 5 < state.camel_spots[which_camel["yellow"]][0] <9:
        screen.blit(yellow,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["yellow"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["yellow"]][1]-1)*stack_height))
    elif 8 < state.camel_spots[which_camel["yellow"]][0] <14:
        screen.blit(yellow,(screen_width//11 + bottom_map[state.camel_spots[which_camel["yellow"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["yellow"]][1]*stack_height))
    elif 13 < state.camel_spots[which_camel["yellow"]][0] <17:
        screen.blit(yellow,(screen_width//11, left_map[state.camel_spots[which_camel["yellow"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["yellow"]][1]-1)*stack_height))
    else:
        screen.blit(yellow,(screen_width//11 + finish_map[state.camel_spots[which_camel["yellow"]][0]]*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["yellow"]][1]*stack_height))


    if state.camel_spots[which_camel["white"]][0]<6:
        screen.blit(white,(screen_width//11 + (state.camel_spots[which_camel["white"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["white"]][1]*stack_height))
    elif 5 < state.camel_spots[which_camel["white"]][0] <9:
        screen.blit(white,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["white"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["white"]][1]-1)*stack_height))
    elif 8 < state.camel_spots[which_camel["white"]][0] <14:
        screen.blit(white,(screen_width//11 + bottom_map[state.camel_spots[which_camel["white"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["white"]][1]*stack_height))
    elif 13 < state.camel_spots[which_camel["white"]][0] <17:
        screen.blit(white,(screen_width//11, left_map[state.camel_spots[which_camel["white"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["white"]][1]-1)*stack_height))
    else:
        screen.blit(white,(screen_width//11 + finish_map[state.camel_spots[which_camel["white"]][0]]*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["white"]][1]*stack_height))

    if state.camel_spots[which_camel["blue"]][0]<6:
        screen.blit(blue,(screen_width//11 + (state.camel_spots[which_camel["blue"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["blue"]][1]*stack_height))
    elif 5 < state.camel_spots[which_camel["blue"]][0] <9:
        screen.blit(blue,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["blue"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["blue"]][1]-1)*stack_height))
    elif 8 < state.camel_spots[which_camel["blue"]][0] <14:
        screen.blit(blue,(screen_width//11 + bottom_map[state.camel_spots[which_camel["blue"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["blue"]][1]*stack_height))
    elif 13 < state.camel_spots[which_camel["blue"]][0] <17:
        screen.blit(blue,(screen_width//11, left_map[state.camel_spots[which_camel["blue"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["blue"]][1]-1)*stack_height))
    else:
        screen.blit(blue,(screen_width//11 + finish_map[state.camel_spots[which_camel["blue"]][0]]*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["blue"]][1]*stack_height))

    if state.camel_spots[which_camel["green"]][0]<6:
        screen.blit(green,(screen_width//11 + (state.camel_spots[which_camel["green"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["green"]][1]*stack_height))
    elif 5 < state.camel_spots[which_camel["green"]][0] <9:
        screen.blit(green,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["green"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["green"]][1]-1)*stack_height))
    elif 8 < state.camel_spots[which_camel["green"]][0] <14:
        screen.blit(green,(screen_width//11 + bottom_map[state.camel_spots[which_camel["green"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["green"]][1]*stack_height))
    elif 13 < state.camel_spots[which_camel["green"]][0] <17:
        screen.blit(green,(screen_width//11, left_map[state.camel_spots[which_camel["green"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["green"]][1]-1)*stack_height))
    else:
        screen.blit(green,(screen_width//11 + finish_map[state.camel_spots[which_camel["green"]][0]]*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["green"]][1]*stack_height))

    if state.camel_spots[which_camel["red"]][0]<6:
        screen.blit(red,(screen_width//11 + (state.camel_spots[which_camel["red"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["red"]][1]*stack_height))
    elif 5 < state.camel_spots[which_camel["red"]][0] <9:
        screen.blit(red,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["red"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["red"]][1]-1)*stack_height))
    elif 8 < state.camel_spots[which_camel["red"]][0] <14:
        screen.blit(red,(screen_width//11 + bottom_map[state.camel_spots[which_camel["red"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["red"]][1]*stack_height))
    elif 13 < state.camel_spots[which_camel["red"]][0] <17:
        screen.blit(red,(screen_width//11, left_map[state.camel_spots[which_camel["red"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["red"]][1]-1)*stack_height))
    else:
        screen.blit(red,(screen_width//11 + finish_map[state.camel_spots[which_camel["red"]][0]]*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["red"]][1]*stack_height))

    pygame.draw.rect(screen,(207,166,117),roll_button)
    screen.blit(roll_button_text,(roll_button_x + roll_button_w//5,roll_button_y + roll_button_h//4))

    color_dict = {"green":(68,134,46),"white":(231,231,231),"blue":(20,55,232),"yellow":(240,224,74),"red":(222,62,35)}

    if display_red_die:

        red_die = pygame.Rect(1.3*screen_width//5,screen_height-1.4*screen_height//5,50,50)
        pygame.draw.rect(screen,color_dict["red"],red_die)
        red_dice_text = smallfont.render(str(red_die_number) , True , (0,0,0))
        screen.blit(red_dice_text,(1.4*screen_width//5,screen_height-1.3*screen_height//5))

    if display_blue_die:

        blue_die = pygame.Rect(1.8*screen_width//5,screen_height-1.4*screen_height//5,50,50)
        pygame.draw.rect(screen,color_dict["blue"],blue_die)
        blue_dice_text = smallfont.render(str(blue_die_number) , True , (0,0,0))
        screen.blit(blue_dice_text,(1.9*screen_width//5,screen_height-1.3*screen_height//5))

    if display_green_die:

        green_die = pygame.Rect(2.3*screen_width//5,screen_height-1.4*screen_height//5,50,50)
        pygame.draw.rect(screen,color_dict["green"],green_die)
        green_dice_text = smallfont.render(str(green_die_number) , True , (0,0,0))
        screen.blit(green_dice_text,(2.4*screen_width//5,screen_height-1.3*screen_height//5))

    if display_yellow_die:

        yellow_die = pygame.Rect(2.8*screen_width//5,screen_height-1.4*screen_height//5,50,50)
        pygame.draw.rect(screen,color_dict["yellow"],yellow_die)
        yellow_dice_text = smallfont.render(str(yellow_die_number) , True , (0,0,0))
        screen.blit(yellow_dice_text,(2.9*screen_width//5,screen_height-1.3*screen_height//5))

    if display_white_die:

        white_die = pygame.Rect(3.3*screen_width//5,screen_height-1.4*screen_height//5,50,50)
        pygame.draw.rect(screen,color_dict["white"],white_die)
        white_dice_text = smallfont.render(str(white_die_number) , True , (0,0,0))
        screen.blit(white_dice_text,(3.4*screen_width//5,screen_height-1.3*screen_height//5))

    if which_camel["red"] in state.bets_left:

        pygame.draw.rect(screen,color_dict["red"],red_betting_card)
        red_betting_number = state.bets_left[which_camel["red"]][-1]
        red_card_text = smallfont.render(str(red_betting_number) , True , (0,0,0))
        screen.blit(red_card_text,(red_betting_card_x + betting_card_w//3,betting_card_y+ betting_card_h//3))

    if which_camel["blue"] in state.bets_left:

        pygame.draw.rect(screen,color_dict["blue"],blue_betting_card)
        blue_betting_number = state.bets_left[which_camel["blue"]][-1]
        blue_card_text = smallfont.render(str(blue_betting_number) , True , (0,0,0))
        screen.blit(blue_card_text,(blue_betting_card_x + betting_card_w//3,betting_card_y+ betting_card_h//3))

    if which_camel["green"] in state.bets_left:

        pygame.draw.rect(screen,color_dict["green"],green_betting_card)
        green_betting_number = state.bets_left[which_camel["green"]][-1]
        green_card_text = smallfont.render(str(green_betting_number) , True , (0,0,0))
        screen.blit(green_card_text,(green_betting_card_x + betting_card_w//3,betting_card_y+ betting_card_h//3))

    if which_camel["yellow"] in state.bets_left:

        pygame.draw.rect(screen,color_dict["yellow"],yellow_betting_card)
        yellow_betting_number = state.bets_left[which_camel["yellow"]][-1]
        yellow_card_text = smallfont.render(str(yellow_betting_number) , True , (0,0,0))
        screen.blit(yellow_card_text,(yellow_betting_card_x + betting_card_w//3,betting_card_y+ betting_card_h//3))

    if which_camel["white"] in state.bets_left:

        pygame.draw.rect(screen,color_dict["white"],white_betting_card)
        white_betting_number = state.bets_left[which_camel["white"]][-1]
        white_card_text = smallfont.render(str(white_betting_number) , True , (0,0,0))
        screen.blit(white_card_text,(white_betting_card_x + betting_card_w//3,betting_card_y+ betting_card_h//3))


    p1_score = p1.money
    p1_score_text = smallfont.render("p1 score: " + str(p1_score) , True , (0,0,0))
    screen.blit(p1_score_text,(1.2*screen_width//5,2.65*screen_height//4))

    p2_score = p2.money
    p2_score_text = smallfont.render("p2 score: " + str(p2_score) , True , (0,0,0))
    screen.blit(p2_score_text,(3*screen_width//5,2.65*screen_height//4))

    leg_bets_text = smallfont.render("leg bets:" , True , (0,0,0))
    screen.blit(leg_bets_text,(1.1*screen_width//5,screen_height//4))

    total_bets_text = smallfont.render("ovr. bets:" , True , (0,0,0))
    screen.blit(total_bets_text,(1.1*screen_width//5,screen_height//3))

    W_txt = smallfont.render("W" , True , (0,0,0))
    L_txt = smallfont.render("L" , True , (0,0,0))

    pygame.draw.rect(screen,color_dict["red"],total_red_W)
    screen.blit(W_txt,(red_total_Wx + total_w//3,total_Wy))
    pygame.draw.rect(screen,color_dict["red"],total_red_L)
    screen.blit(L_txt,(red_total_Lx + total_w//3,total_Ly))

    pygame.draw.rect(screen,color_dict["white"],total_white_W)
    screen.blit(W_txt,(white_total_Wx + total_w//3,total_Wy))
    pygame.draw.rect(screen,color_dict["white"],total_white_L)
    screen.blit(L_txt,(white_total_Lx + total_w//3,total_Ly))

    pygame.draw.rect(screen,color_dict["blue"],total_blue_W)
    screen.blit(W_txt,(blue_total_Wx + total_w//3,total_Wy))
    pygame.draw.rect(screen,color_dict["blue"],total_blue_L)
    screen.blit(L_txt,(blue_total_Lx + total_w//3,total_Ly))

    pygame.draw.rect(screen,color_dict["green"],total_green_W)
    screen.blit(W_txt,(green_total_Wx + total_w//3,total_Wy))
    pygame.draw.rect(screen,color_dict["green"],total_green_L)
    screen.blit(L_txt,(green_total_Lx + total_w//3,total_Ly))

    pygame.draw.rect(screen,color_dict["yellow"],total_yellow_W)
    screen.blit(W_txt,(yellow_total_Wx + total_w//3,total_Wy))
    pygame.draw.rect(screen,color_dict["yellow"],total_yellow_L)
    screen.blit(L_txt,(yellow_total_Lx + total_w//3,total_Ly))

    p1_bets_text = smallfont.render("p1 bets", True , (0,0,0))
    screen.blit(p1_bets_text,(1.3*screen_width//5,screen_height//2.4))

    p2_bets_text = smallfont.render("p2 bets", True , (0,0,0))
    screen.blit(p2_bets_text,(3.1*screen_width//5,screen_height//2.4))

    p1_red_bets_made = smallfont.render(f"{p1.bets_made[which_camel['red']]}", True , color_dict["red"])
    screen.blit(p1_red_bets_made,(screen_width//4.2,screen_height//2.2))

    p1_blue_bets_made = smallfont.render(f"{p1.bets_made[which_camel['blue']]}", True , color_dict["blue"])
    screen.blit(p1_blue_bets_made,(screen_width//4.2,screen_height//2.05))

    p1_green_bets_made = smallfont.render(f"{p1.bets_made[which_camel['green']]}", True , color_dict["green"])
    screen.blit(p1_green_bets_made,(screen_width//4.2,screen_height//1.92))

    p1_yellow_bets_made = smallfont.render(f"{p1.bets_made[which_camel['yellow']]}", True , color_dict["yellow"])
    screen.blit(p1_yellow_bets_made,(screen_width//4.2,screen_height//1.8))

    p1_white_bets_made = smallfont.render(f"{p1.bets_made[which_camel['white']]}", True , color_dict["white"])
    screen.blit(p1_white_bets_made,(screen_width//4.2,screen_height//1.7))

    p2_red_bets_made = smallfont.render(f"{p2.bets_made[which_camel['red']]}", True , color_dict["red"])
    screen.blit(p2_red_bets_made,(2.5*screen_width//4.2,screen_height//2.2))

    p2_blue_bets_made = smallfont.render(f"{p2.bets_made[which_camel['blue']]}", True , color_dict["blue"])
    screen.blit(p2_blue_bets_made,(2.5*screen_width//4.2,screen_height//2.05))

    p2_green_bets_made = smallfont.render(f"{p2.bets_made[which_camel['green']]}", True , color_dict["green"])
    screen.blit(p2_green_bets_made,(2.5*screen_width//4.2,screen_height//1.92))

    p2_yellow_bets_made = smallfont.render(f"{p2.bets_made[which_camel['yellow']]}", True , color_dict["yellow"])
    screen.blit(p2_yellow_bets_made,(2.5*screen_width//4.2,screen_height//1.8))

    p2_white_bets_made = smallfont.render(f"{p2.bets_made[which_camel['white']]}", True , color_dict["white"])
    screen.blit(p2_white_bets_made,(2.5*screen_width//4.2,screen_height//1.7))




while True:

    draw_board(screen,screen_width,screen_height,display_red_die,display_blue_die,
               display_green_die, display_white_die,display_yellow_die,red_die_number,
               green_die_number,blue_die_number,white_die_number,yellow_die_number,
               state,yellow,red,green,blue,white,p1,p2,roll_button_x,roll_button_y,
               roll_button_w,roll_button_h,roll_button,smallfont,roll_button_text,
               red_betting_card_x,blue_betting_card_x,yellow_betting_card_x,green_betting_card_x,
               white_betting_card_x,betting_card_y,betting_card_w,betting_card_h,red_betting_card,
               blue_betting_card,yellow_betting_card,green_betting_card,white_betting_card,
               total_red_W,total_red_L,total_blue_W,total_blue_L,total_green_W,total_green_L,
               total_white_W,total_white_L,total_yellow_W,total_yellow_L)

    complete = state.is_complete() #check if game is complete
    if not complete[0]:


        #if it is the human's move
        if p1_turn:

            start = time.time()

            mouse = pygame.mouse.get_pos()
            event = pygame.event.poll()



            if (roll_button_x < mouse[0] < roll_button_x + roll_button_w) and (roll_button_y < mouse[1] < roll_button_y + roll_button_h):
                pygame.draw.rect(screen,(134,100,68),roll_button)
                screen.blit(roll_button_text,(roll_button_x + roll_button_w//5,roll_button_y + roll_button_h//4))

                if event.type == pygame.MOUSEBUTTONDOWN:

                    #roll die
                    dice_list = list(state.dice_left)
                    die_num = -1
                    if len(dice_list) == 1:
                        die_num = 1
                    else:
                        die_num = random.randint(1,len(dice_list))
                    die = dice_list[die_num-1]
                    new_dice_left = cp.deepcopy(state.dice_left)
                    new_dice_left.remove(die)
                    die_roll = random.randint(1,3)
                    new_camel_spots = cp.deepcopy(state.camel_spots)
                    new_board_state = cp.deepcopy(state.board_state)
                    #update the position of camel # die
                    for camel in state.board_state[state.camel_spots[die][0]]:
                        if state.camel_spots[camel][1] >= state.camel_spots[die][1]:
                            new_board_state[state.camel_spots[camel][0]].remove(camel)
                            new_camel_spots[camel][0] += die_roll
                            new_camel_spots[camel][1] = len(new_board_state[new_camel_spots[camel][0]])
                            new_board_state[new_camel_spots[camel][0]].append(camel)


                    state = GameStateNode(new_board_state,new_dice_left,state.bets_left, new_camel_spots, state.winner_bets_left, state.loser_bets_left)

                    state.die = die
                    state.die_roll = die_roll

                    p1.money += 1

                    p1_turn = False

            if which_camel["red"] in state.bets_left:

                if (red_betting_card_x < mouse[0] < red_betting_card_x + betting_card_w) and (betting_card_y < mouse[1] < betting_card_y + betting_card_h):
                    pygame.draw.rect(screen,(134,100,68),red_betting_card)
                    red_betting_number = state.bets_left[which_camel["red"]][-1]
                    red_card_text = smallfont.render(str(red_betting_number) , True , (0,0,0))
                    screen.blit(red_card_text,(red_betting_card_x + betting_card_w//3,betting_card_y+ betting_card_h//3))

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        new_bets_left = cp.deepcopy(state.bets_left)
                        payout = new_bets_left[which_camel["red"]].pop()
                        if len(new_bets_left[which_camel["red"]])==0:
                            del new_bets_left[which_camel["red"]]

                        p1.bets_made[which_camel["red"]].append(payout)

                        state = GameStateNode(state.board_state,state.dice_left,new_bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

            if which_camel["blue"] in state.bets_left:

                if (blue_betting_card_x < mouse[0] < blue_betting_card_x + betting_card_w) and (betting_card_y < mouse[1] < betting_card_y + betting_card_h):
                    pygame.draw.rect(screen,(134,100,68),blue_betting_card)
                    blue_betting_number = state.bets_left[which_camel["blue"]][-1]
                    blue_card_text = smallfont.render(str(blue_betting_number) , True , (0,0,0))
                    screen.blit(blue_card_text,(blue_betting_card_x + betting_card_w//3,betting_card_y+ betting_card_h//3))

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        new_bets_left = cp.deepcopy(state.bets_left)
                        payout = new_bets_left[which_camel["blue"]].pop()
                        if len(new_bets_left[which_camel["blue"]])==0:
                            del new_bets_left[which_camel["blue"]]

                        p1.bets_made[which_camel["blue"]].append(payout)

                        state = GameStateNode(state.board_state,state.dice_left,new_bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

            if which_camel["green"] in state.bets_left:

                if (green_betting_card_x < mouse[0] < green_betting_card_x + betting_card_w) and (betting_card_y < mouse[1] < betting_card_y + betting_card_h):
                    pygame.draw.rect(screen,(134,100,68),green_betting_card)
                    green_betting_number = state.bets_left[which_camel["green"]][-1]
                    green_card_text = smallfont.render(str(green_betting_number) , True , (0,0,0))
                    screen.blit(green_card_text,(green_betting_card_x + betting_card_w//3,betting_card_y+ betting_card_h//3))

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        new_bets_left = cp.deepcopy(state.bets_left)
                        payout = new_bets_left[which_camel["green"]].pop()
                        if len(new_bets_left[which_camel["green"]])==0:
                            del new_bets_left[which_camel["green"]]

                        p1.bets_made[which_camel["green"]].append(payout)

                        state = GameStateNode(state.board_state,state.dice_left,new_bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

            if which_camel["white"] in state.bets_left:

                if (white_betting_card_x < mouse[0] < white_betting_card_x + betting_card_w) and (betting_card_y < mouse[1] < betting_card_y + betting_card_h):
                    pygame.draw.rect(screen,(134,100,68),white_betting_card)
                    white_betting_number = state.bets_left[which_camel["white"]][-1]
                    white_card_text = smallfont.render(str(white_betting_number) , True , (0,0,0))
                    screen.blit(white_card_text,(white_betting_card_x + betting_card_w//3,betting_card_y+ betting_card_h//3))

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        new_bets_left = cp.deepcopy(state.bets_left)
                        payout = new_bets_left[which_camel["white"]].pop()
                        if len(new_bets_left[which_camel["white"]])==0:
                            del new_bets_left[which_camel["white"]]

                        p1.bets_made[which_camel["white"]].append(payout)

                        state = GameStateNode(state.board_state,state.dice_left,new_bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

            if which_camel["yellow"] in state.bets_left:

                if (yellow_betting_card_x < mouse[0] < yellow_betting_card_x + betting_card_w) and (betting_card_y < mouse[1] < betting_card_y + betting_card_h):
                    pygame.draw.rect(screen,(134,100,68),yellow_betting_card)
                    yellow_betting_number = state.bets_left[which_camel["yellow"]][-1]
                    yellow_card_text = smallfont.render(str(yellow_betting_number) , True , (0,0,0))
                    screen.blit(yellow_card_text,(yellow_betting_card_x + betting_card_w//3,betting_card_y+ betting_card_h//3))

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        new_bets_left = cp.deepcopy(state.bets_left)
                        payout = new_bets_left[which_camel["yellow"]].pop()
                        if len(new_bets_left[which_camel["yellow"]])==0:
                            del new_bets_left[which_camel["yellow"]]

                        p1.bets_made[which_camel["yellow"]].append(payout)

                        state = GameStateNode(state.board_state,state.dice_left,new_bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

            if not p1.finalWinner:

                if (red_total_Wx < mouse[0] < red_total_Wx + total_w) and (total_Wy < mouse[1] < total_Wy + total_h):
                    pygame.draw.rect(screen,(134,100,68),total_red_W)
                    W_txt = smallfont.render("W" , True , (0,0,0))
                    screen.blit(W_txt,(red_total_Wx + total_w//3,total_Wy))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        payout = state.winner_bets_left.pop(0)
                        p1.finalWinner = (which_camel["red"],payout)
                        state = GameStateNode(state.board_state,state.dice_left,state.bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

                elif (yellow_total_Wx < mouse[0] < yellow_total_Wx + total_w) and (total_Wy < mouse[1] < total_Wy + total_h):
                    pygame.draw.rect(screen,(134,100,68),total_yellow_W)
                    W_txt = smallfont.render("W" , True , (0,0,0))
                    screen.blit(W_txt,(yellow_total_Wx + total_w//3,total_Wy))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        payout = state.winner_bets_left.pop(0)
                        p1.finalWinner = (which_camel["yellow"],payout)
                        state = GameStateNode(state.board_state,state.dice_left,state.bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

                elif (blue_total_Wx < mouse[0] < blue_total_Wx + total_w) and (total_Wy < mouse[1] < total_Wy + total_h):
                    pygame.draw.rect(screen,(134,100,68),total_blue_W)
                    W_txt = smallfont.render("W" , True , (0,0,0))
                    screen.blit(W_txt,(blue_total_Wx + total_w//3,total_Wy))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        payout = state.winner_bets_left.pop(0)
                        p1.finalWinner = (which_camel["blue"],payout)
                        state = GameStateNode(state.board_state,state.dice_left,state.bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

                elif (green_total_Wx < mouse[0] < green_total_Wx + total_w) and (total_Wy < mouse[1] < total_Wy + total_h):
                    pygame.draw.rect(screen,(134,100,68),total_green_W)
                    W_txt = smallfont.render("W" , True , (0,0,0))
                    screen.blit(W_txt,(green_total_Wx + total_w//3,total_Wy))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        payout = state.winner_bets_left.pop(0)
                        p1.finalWinner = (which_camel["green"],payout)
                        state = GameStateNode(state.board_state,state.dice_left,state.bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

                elif (white_total_Wx < mouse[0] < white_total_Wx + total_w) and (total_Wy < mouse[1] < total_Wy + total_h):
                    pygame.draw.rect(screen,(134,100,68),total_white_W)
                    W_txt = smallfont.render("W" , True , (0,0,0))
                    screen.blit(W_txt,(white_total_Wx + total_w//3,total_Wy))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        payout = state.winner_bets_left.pop(0)
                        p1.finalWinner = (which_camel["white"],payout)
                        state = GameStateNode(state.board_state,state.dice_left,state.bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

            if not p1.finalLoser:

                if (red_total_Lx < mouse[0] < red_total_Lx + total_w) and (total_Ly < mouse[1] < total_Ly + total_h):
                    pygame.draw.rect(screen,(134,100,68),total_red_L)
                    L_txt = smallfont.render("L" , True , (0,0,0))
                    screen.blit(L_txt,(red_total_Lx + total_w//3,total_Ly))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        payout = state.loser_bets_left.pop(0)
                        p1.finalLoser = (which_camel["red"],payout)
                        state = GameStateNode(state.board_state,state.dice_left,state.bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

                elif (yellow_total_Lx < mouse[0] < yellow_total_Lx + total_w) and (total_Ly < mouse[1] < total_Ly + total_h):
                    pygame.draw.rect(screen,(134,100,68),total_yellow_L)
                    L_txt = smallfont.render("L" , True , (0,0,0))
                    screen.blit(L_txt,(yellow_total_Lx + total_w//3,total_Ly))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        payout = state.loser_bets_left.pop(0)
                        p1.finalLoser = (which_camel["yellow"],payout)
                        state = GameStateNode(state.board_state,state.dice_left,state.bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

                elif (blue_total_Lx < mouse[0] < blue_total_Lx + total_w) and (total_Ly < mouse[1] < total_Ly + total_h):
                    pygame.draw.rect(screen,(134,100,68),total_blue_L)
                    L_txt = smallfont.render("L" , True , (0,0,0))
                    screen.blit(L_txt,(blue_total_Lx + total_w//3,total_Ly))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        payout = state.loser_bets_left.pop(0)
                        p1.finalLoser = (which_camel["blue"],payout)
                        state = GameStateNode(state.board_state,state.dice_left,state.bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

                elif (green_total_Lx < mouse[0] < green_total_Lx + total_w) and (total_Ly < mouse[1] < total_Ly + total_h):
                    pygame.draw.rect(screen,(134,100,68),total_green_L)
                    L_txt = smallfont.render("L" , True , (0,0,0))
                    screen.blit(L_txt,(green_total_Lx + total_w//3,total_Ly))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        payout = state.loser_bets_left.pop(0)
                        p1.finalLoser = (which_camel["green"],payout)
                        state = GameStateNode(state.board_state,state.dice_left,state.bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

                elif (white_total_Lx < mouse[0] < white_total_Lx + total_w) and (total_Ly < mouse[1] < total_Ly + total_h):
                    pygame.draw.rect(screen,(134,100,68),total_white_L)
                    L_txt = smallfont.render("L" , True , (0,0,0))
                    screen.blit(L_txt,(white_total_Lx + total_w//3,total_Ly))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        payout = state.loser_bets_left.pop(0)
                        p1.finalLoser = (which_camel["white"],payout)
                        state = GameStateNode(state.board_state,state.dice_left,state.bets_left,state.camel_spots, state.winner_bets_left, state.loser_bets_left)

                        p1_turn = False

            if event.type == pygame.KEYDOWN:
                print(state.winner_bets_left,"win")
                print(state.loser_bets_left,"lose")
                print("\n")
                print(p1.finalWinner, "winner")
                print(p2.finalWinner, "winner")
                print(p1.finalLoser, "loser")
                print(p2.finalLoser, "loser")


        elif time.time()-start > 0.01:
            state = p2.make_move(state)

            p1_turn = True

        if state.die != -1: #if we rolled

            if which_color[state.die] == "green":
                display_green_die = True
                green_die_number = state.die_roll

            elif which_color[state.die] == "red":
                display_red_die = True
                red_die_number = state.die_roll

            elif which_color[state.die] == "yellow":
                display_yellow_die = True
                yellow_die_number = state.die_roll

            elif which_color[state.die] == "blue":
                display_blue_die = True
                blue_die_number = state.die_roll

            elif which_color[state.die] == "white":
                display_white_die = True
                white_die_number = state.die_roll

        #reset leg
        if len(state.dice_left) == 0:

            front_camel_indx = 0
            for i in range(len(state.board_state)-1,-1,-1):
                if len(state.board_state[i])>0:
                    front_camel_indx = i
                    break

            for p in players:
                p.money += p.get_payout(state,front_camel_indx)


            state = GameStateNode(state.board_state,set([1,2,3,4,5]),{1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]},state.camel_spots,winner_bets_left,loser_bets_left)

            draw_board(screen,screen_width,screen_height,display_red_die,display_blue_die,
                       display_green_die, display_white_die,display_yellow_die,red_die_number,
                       green_die_number,blue_die_number,white_die_number,yellow_die_number,
                       state,yellow,red,green,blue,white,p1,p2,roll_button_x,roll_button_y,
                       roll_button_w,roll_button_h,roll_button,smallfont,roll_button_text,
                       red_betting_card_x,blue_betting_card_x,yellow_betting_card_x,green_betting_card_x,
                       white_betting_card_x,betting_card_y,betting_card_w,betting_card_h,red_betting_card,
                       blue_betting_card,yellow_betting_card,green_betting_card,white_betting_card,
                       total_red_W,total_red_L,total_blue_W,total_blue_L,total_green_W,total_green_L,
                       total_white_W,total_white_L,total_yellow_W,total_yellow_L)


            pygame.display.update()

            display_red_die = False
            display_blue_die = False
            display_green_die = False
            display_yellow_die = False
            display_white_die = False

            red_die_number = -1
            green_die_number = -1
            blue_die_number = -1
            white_die_number = -1
            yellow_die_number = -1

            pygame.time.wait(2000)

            draw_board(screen,screen_width,screen_height,display_red_die,display_blue_die,
                       display_green_die, display_white_die,display_yellow_die,red_die_number,
                       green_die_number,blue_die_number,white_die_number,yellow_die_number,
                       state,yellow,red,green,blue,white,p1,p2,roll_button_x,roll_button_y,
                       roll_button_w,roll_button_h,roll_button,smallfont,roll_button_text,
                       red_betting_card_x,blue_betting_card_x,yellow_betting_card_x,green_betting_card_x,
                       white_betting_card_x,betting_card_y,betting_card_w,betting_card_h,red_betting_card,
                       blue_betting_card,yellow_betting_card,green_betting_card,white_betting_card,
                       total_red_W,total_red_L,total_blue_W,total_blue_L,total_green_W,total_green_L,
                       total_white_W,total_white_L,total_yellow_W,total_yellow_L)


            pygame.display.update()

    else:

        for p in players:
            p.get_final_payout(state,complete[1])

        draw_board(screen,screen_width,screen_height,display_red_die,display_blue_die,
                   display_green_die, display_white_die,display_yellow_die,red_die_number,
                   green_die_number,blue_die_number,white_die_number,yellow_die_number,
                   state,yellow,red,green,blue,white,p1,p2,roll_button_x,roll_button_y,
                   roll_button_w,roll_button_h,roll_button,smallfont,roll_button_text,
                   red_betting_card_x,blue_betting_card_x,yellow_betting_card_x,green_betting_card_x,
                   white_betting_card_x,betting_card_y,betting_card_w,betting_card_h,red_betting_card,
                   blue_betting_card,yellow_betting_card,green_betting_card,white_betting_card,
                   total_red_W,total_red_L,total_blue_W,total_blue_L,total_green_W,total_green_L,
                   total_white_W,total_white_L,total_yellow_W,total_yellow_L)


        pygame.display.update()

        sim = Simulate()
        result = sim.get_winner(players)
        if result == 3:
            print("Tie!")
        else:
            print(f"player{result} won!")

        print(f"player 1 made {p1.money} coins")
        print(f"player 2 made {p2.money} coins")
        print(state.camel_spots)

        pygame.time.wait(10000)

        break



    pygame.display.update()

pygame.quit()
