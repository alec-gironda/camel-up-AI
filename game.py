from learn import *
import random
import time

board_state, camel_spots = shuffle_start()
bets_left = {1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]}
dice_left = set([1,2,3,4,5])

state = GameStateNode(board_state,dice_left,bets_left,camel_spots)

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
p2 = SmartPlayer("./new_model0")

players = [p1,p2]

which_camel = {"red":1,"yellow":2,"green":3,"blue":4,"white":5}
which_color = {1:"red",2:"yellow",3:"green",4:"blue",5:"white"}

start = time.time()

def draw_board():

    screen.fill((242,205,107))


while True:

    screen.fill((242,205,107))

    complete = state.is_complete() #check if game is complete
    if not complete[0]:


        #could maybe be a bit off on the grids
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

        bottom_map = {9:4,10:3,11:2,12:1,13:0}
        right_map = {6:2.2,7:3.4,8:4.7}
        left_map = {14:4.7,15:3.4,16:2.2}

        if state.camel_spots[which_camel["yellow"]][0]<6:
            screen.blit(yellow,(screen_width//11 + (state.camel_spots[which_camel["yellow"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["yellow"]][1]*stack_height))
        elif 5 < state.camel_spots[which_camel["yellow"]][0] <9:
            screen.blit(yellow,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["yellow"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["yellow"]][1]-1)*stack_height))
        elif 8 < state.camel_spots[which_camel["yellow"]][0] <14:
            screen.blit(yellow,(screen_width//11 + bottom_map[state.camel_spots[which_camel["yellow"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["yellow"]][1]*stack_height))
        else:
            screen.blit(yellow,(screen_width//11, left_map[state.camel_spots[which_camel["yellow"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["yellow"]][1]-1)*stack_height))

        if state.camel_spots[which_camel["green"]][0]<6:
            screen.blit(green,(screen_width//11 + (state.camel_spots[which_camel["green"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["green"]][1]*stack_height))
        elif 5 < state.camel_spots[which_camel["green"]][0] <9:
            screen.blit(green,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["green"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["green"]][1]-1)*stack_height))
        elif 8 < state.camel_spots[which_camel["green"]][0] <14:
            screen.blit(green,(screen_width//11 + bottom_map[state.camel_spots[which_camel["green"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["green"]][1]*stack_height))
        else:
            screen.blit(green,(screen_width//11, left_map[state.camel_spots[which_camel["green"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["green"]][1]-1)*stack_height))

        if state.camel_spots[which_camel["blue"]][0]<6:
            screen.blit(blue,(screen_width//11 + (state.camel_spots[which_camel["blue"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["blue"]][1]*stack_height))
        elif 5 < state.camel_spots[which_camel["blue"]][0] <9:
            screen.blit(blue,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["blue"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["blue"]][1]-1)*stack_height))
        elif 8 < state.camel_spots[which_camel["blue"]][0] <14:
            screen.blit(blue,(screen_width//11 + bottom_map[state.camel_spots[which_camel["blue"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["blue"]][1]*stack_height))
        else:
            screen.blit(blue,(screen_width//11, left_map[state.camel_spots[which_camel["blue"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["yellow"]][1]-1)*stack_height))

        if state.camel_spots[which_camel["red"]][0]<6:
            screen.blit(red,(screen_width//11 + (state.camel_spots[which_camel["red"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["red"]][1]*stack_height))
        elif 5 < state.camel_spots[which_camel["red"]][0] <9:
            screen.blit(red,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["red"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["red"]][1]-1)*stack_height))
        elif 8 < state.camel_spots[which_camel["red"]][0] <14:
            screen.blit(red,(screen_width//11 + bottom_map[state.camel_spots[which_camel["red"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["red"]][1]*stack_height))
        else:
            screen.blit(red,(screen_width//11, left_map[state.camel_spots[which_camel["red"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["red"]][1]-1)*stack_height))

        if state.camel_spots[which_camel["white"]][0]<6:
            screen.blit(white,(screen_width//11 + (state.camel_spots[which_camel["white"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["white"]][1]*stack_height))
        elif 5 < state.camel_spots[which_camel["white"]][0] <9:
            screen.blit(white,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["white"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["white"]][1]-1)*stack_height))
        elif 8 < state.camel_spots[which_camel["white"]][0] <14:
            screen.blit(white,(screen_width//11 + bottom_map[state.camel_spots[which_camel["white"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["white"]][1]*stack_height))
        else:
            screen.blit(white,(screen_width//11, left_map[state.camel_spots[which_camel["white"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["white"]][1]-1)*stack_height))


        roll_button_w = 100
        roll_button_h = 50
        roll_button_x = screen_width//2 - roll_button_w//2
        roll_button_y = screen_height//2 -roll_button_h//2

        roll_button = pygame.Rect(roll_button_x,roll_button_y,roll_button_w,roll_button_h)
        pygame.draw.rect(screen,(207,166,117),roll_button)
        smallfont = pygame.font.SysFont('bahnschrift',35)
        roll_button_text = smallfont.render('DICE' , True , (231,231,231))
        screen.blit(roll_button_text,(roll_button_x + roll_button_w//5,roll_button_y + roll_button_h//4))

        color_dict = {"green":(68,134,46),"white":(231,231,231),"blue":(20,55,232),"yellow":(240,224,74),"red":(222,62,35)}

        if display_red_die:

            red_die = pygame.Rect(1.3*screen_width//5,screen_height-2*screen_height//5,50,50)
            pygame.draw.rect(screen,color_dict["red"],red_die)
            red_dice_text = smallfont.render(str(red_die_number) , True , (0,0,0))
            screen.blit(red_dice_text,(1.4*screen_width//5,screen_height-1.9*screen_height//5))

        if display_blue_die:

            blue_die = pygame.Rect(1.8*screen_width//5,screen_height-2*screen_height//5,50,50)
            pygame.draw.rect(screen,color_dict["blue"],blue_die)
            blue_dice_text = smallfont.render(str(blue_die_number) , True , (0,0,0))
            screen.blit(blue_dice_text,(1.9*screen_width//5,screen_height-1.9*screen_height//5))

        if display_green_die:

            green_die = pygame.Rect(2.3*screen_width//5,screen_height-2*screen_height//5,50,50)
            pygame.draw.rect(screen,color_dict["green"],green_die)
            green_dice_text = smallfont.render(str(green_die_number) , True , (0,0,0))
            screen.blit(green_dice_text,(2.4*screen_width//5,screen_height-1.9*screen_height//5))

        if display_yellow_die:

            yellow_die = pygame.Rect(2.8*screen_width//5,screen_height-2*screen_height//5,50,50)
            pygame.draw.rect(screen,color_dict["yellow"],yellow_die)
            yellow_dice_text = smallfont.render(str(yellow_die_number) , True , (0,0,0))
            screen.blit(yellow_dice_text,(2.9*screen_width//5,screen_height-1.9*screen_height//5))

        if display_white_die:

            white_die = pygame.Rect(3.3*screen_width//5,screen_height-2*screen_height//5,50,50)
            pygame.draw.rect(screen,color_dict["white"],white_die)
            white_dice_text = smallfont.render(str(white_die_number) , True , (0,0,0))
            screen.blit(white_dice_text,(3.4*screen_width//5,screen_height-1.9*screen_height//5))


        red_betting_card = pygame.Rect(1.3*screen_width//5,screen_height-2*screen_height//3,50,50)
        pygame.draw.rect(screen,color_dict["red"],red_betting_card)
        red_betting_number = 3
        red_card_text = smallfont.render(str(red_betting_number) , True , (0,0,0))
        screen.blit(red_card_text,(1.4*screen_width//5,screen_height-1.95*screen_height//3))

        blue_betting_card = pygame.Rect(1.8*screen_width//5,screen_height-2*screen_height//3,50,50)
        pygame.draw.rect(screen,color_dict["blue"],blue_betting_card)
        blue_betting_number = 3
        blue_card_text = smallfont.render(str(blue_betting_number) , True , (0,0,0))
        screen.blit(blue_card_text,(1.9*screen_width//5,screen_height-1.95*screen_height//3))

        green_betting_card = pygame.Rect(2.3*screen_width//5,screen_height-2*screen_height//3,50,50)
        pygame.draw.rect(screen,color_dict["green"],green_betting_card)
        green_betting_number = 3
        green_card_text = smallfont.render(str(green_betting_number) , True , (0,0,0))
        screen.blit(green_card_text,(2.4*screen_width//5,screen_height-1.95*screen_height//3))

        yellow_betting_card = pygame.Rect(2.8*screen_width//5,screen_height-2*screen_height//3,50,50)
        pygame.draw.rect(screen,color_dict["yellow"],yellow_betting_card)
        yellow_betting_number = 3
        yellow_card_text = smallfont.render(str(yellow_betting_number) , True , (0,0,0))
        screen.blit(yellow_card_text,(2.9*screen_width//5,screen_height-1.95*screen_height//3))

        white_betting_die = pygame.Rect(3.3*screen_width//5,screen_height-2*screen_height//3,50,50)
        pygame.draw.rect(screen,color_dict["white"],white_betting_die)
        white_betting_number = 3
        white_card_text = smallfont.render(str(white_betting_number) , True , (0,0,0))
        screen.blit(white_card_text,(3.4*screen_width//5,screen_height-1.95*screen_height//3))

        p1_score = p1.money
        p1_score_text = smallfont.render("p1 score: " + str(p1_score) , True , (0,0,0))
        screen.blit(p1_score_text,(1.2*screen_width//5,screen_height//2))

        p2_score = p2.money
        p2_score_text = smallfont.render("p2 score: " + str(p2_score) , True , (0,0,0))
        screen.blit(p2_score_text,(3*screen_width//5,screen_height//2))

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


                    state = GameStateNode(new_board_state,new_dice_left,state.bets_left,new_camel_spots)

                    state.die = die
                    state.die_roll = die_roll

                    p1.money += 1

                    p1_turn = False


            if event.type == pygame.KEYDOWN:
                break


        elif time.time()-start > 1:
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

            red_die = pygame.Rect(1.3*screen_width//5,screen_height-2*screen_height//5,50,50)
            pygame.draw.rect(screen,color_dict["red"],red_die)
            red_dice_text = smallfont.render(str(red_die_number) , True , (0,0,0))
            screen.blit(red_dice_text,(1.4*screen_width//5,screen_height-1.9*screen_height//5))

            blue_die = pygame.Rect(1.8*screen_width//5,screen_height-2*screen_height//5,50,50)
            pygame.draw.rect(screen,color_dict["blue"],blue_die)
            blue_dice_text = smallfont.render(str(blue_die_number) , True , (0,0,0))
            screen.blit(blue_dice_text,(1.9*screen_width//5,screen_height-1.9*screen_height//5))

            green_die = pygame.Rect(2.3*screen_width//5,screen_height-2*screen_height//5,50,50)
            pygame.draw.rect(screen,color_dict["green"],green_die)
            green_dice_text = smallfont.render(str(green_die_number) , True , (0,0,0))
            screen.blit(green_dice_text,(2.4*screen_width//5,screen_height-1.9*screen_height//5))

            yellow_die = pygame.Rect(2.8*screen_width//5,screen_height-2*screen_height//5,50,50)
            pygame.draw.rect(screen,color_dict["yellow"],yellow_die)
            yellow_dice_text = smallfont.render(str(yellow_die_number) , True , (0,0,0))
            screen.blit(yellow_dice_text,(2.9*screen_width//5,screen_height-1.9*screen_height//5))

            white_die = pygame.Rect(3.3*screen_width//5,screen_height-2*screen_height//5,50,50)
            pygame.draw.rect(screen,color_dict["white"],white_die)
            white_dice_text = smallfont.render(str(white_die_number) , True , (0,0,0))
            screen.blit(white_dice_text,(3.4*screen_width//5,screen_height-1.9*screen_height//5))

            if state.camel_spots[which_camel["yellow"]][0]<6:
                screen.blit(yellow,(screen_width//11 + (state.camel_spots[which_camel["yellow"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["yellow"]][1]*stack_height))
            elif 5 < state.camel_spots[which_camel["yellow"]][0] <9:
                screen.blit(yellow,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["yellow"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["yellow"]][1]-1)*stack_height))
            elif 8 < state.camel_spots[which_camel["yellow"]][0] <14:
                screen.blit(yellow,(screen_width//11 + bottom_map[state.camel_spots[which_camel["yellow"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["yellow"]][1]*stack_height))
            else:
                screen.blit(yellow,(screen_width//11, left_map[state.camel_spots[which_camel["yellow"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["yellow"]][1]-1)*stack_height))

            if state.camel_spots[which_camel["green"]][0]<6:
                screen.blit(green,(screen_width//11 + (state.camel_spots[which_camel["green"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["green"]][1]*stack_height))
            elif 5 < state.camel_spots[which_camel["green"]][0] <9:
                screen.blit(green,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["green"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["green"]][1]-1)*stack_height))
            elif 8 < state.camel_spots[which_camel["green"]][0] <14:
                screen.blit(green,(screen_width//11 + bottom_map[state.camel_spots[which_camel["green"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["green"]][1]*stack_height))
            else:
                screen.blit(green,(screen_width//11, left_map[state.camel_spots[which_camel["green"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["green"]][1]-1)*stack_height))

            if state.camel_spots[which_camel["blue"]][0]<6:
                screen.blit(blue,(screen_width//11 + (state.camel_spots[which_camel["blue"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["blue"]][1]*stack_height))
            elif 5 < state.camel_spots[which_camel["blue"]][0] <9:
                screen.blit(blue,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["blue"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["blue"]][1]-1)*stack_height))
            elif 8 < state.camel_spots[which_camel["blue"]][0] <14:
                screen.blit(blue,(screen_width//11 + bottom_map[state.camel_spots[which_camel["blue"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["blue"]][1]*stack_height))
            else:
                screen.blit(blue,(screen_width//11, left_map[state.camel_spots[which_camel["blue"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["yellow"]][1]-1)*stack_height))

            if state.camel_spots[which_camel["red"]][0]<6:
                screen.blit(red,(screen_width//11 + (state.camel_spots[which_camel["red"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["red"]][1]*stack_height))
            elif 5 < state.camel_spots[which_camel["red"]][0] <9:
                screen.blit(red,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["red"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["red"]][1]-1)*stack_height))
            elif 8 < state.camel_spots[which_camel["red"]][0] <14:
                screen.blit(red,(screen_width//11 + bottom_map[state.camel_spots[which_camel["red"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["red"]][1]*stack_height))
            else:
                screen.blit(red,(screen_width//11, left_map[state.camel_spots[which_camel["red"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["red"]][1]-1)*stack_height))

            if state.camel_spots[which_camel["white"]][0]<6:
                screen.blit(white,(screen_width//11 + (state.camel_spots[which_camel["white"]][0]-1)*screen_width//5,screen_height//6.5 - state.camel_spots[which_camel["white"]][1]*stack_height))
            elif 5 < state.camel_spots[which_camel["white"]][0] <9:
                screen.blit(white,(screen_width//11 + 4*screen_width//5, right_map[state.camel_spots[which_camel["white"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["white"]][1]-1)*stack_height))
            elif 8 < state.camel_spots[which_camel["white"]][0] <14:
                screen.blit(white,(screen_width//11 + bottom_map[state.camel_spots[which_camel["white"]][0]]*screen_width//5,screen_height//6.5 + 3.8*screen_height//5 - state.camel_spots[which_camel["white"]][1]*stack_height))
            else:
                screen.blit(white,(screen_width//11, left_map[state.camel_spots[which_camel["white"]][0]]*screen_height//6.5 - (state.camel_spots[which_camel["white"]][1]-1)*stack_height))


            pygame.display.update()

            pygame.time.wait(2000)

            front_camel_indx = 0
            for i in range(len(state.board_state)-1,-1,-1):
                if len(state.board_state[i])>0:
                    front_camel_indx = i
                    break
            for p in players:
                p.money += p.get_payout(state,front_camel_indx)

            state = GameStateNode(state.board_state,set([1,2,3,4,5]),{1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]},state.camel_spots)

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

    else:

        for p in players:
            p.money += p.get_payout(state,complete[1])

        sim = Simulate()
        result = sim.get_winner(players)
        if result == 3:
            print("Tie!")
        else:
            print(f"player{result} won!")

        print(f"player 1 made {p1.money} coins")
        print(f"player 2 made {p2.money} coins")
        print(state.camel_spots)


        break


    pygame.display.update()

pygame.quit()
