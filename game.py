from learn import *

board_state, camel_spots = shuffle_start()
bets_left = {1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]}
dice_left = set([1,2,3,4,5])

state = GameStateNode(board_state,dice_left,bets_left,camel_spots)

pygame.init()
screen_width  = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))

display = False
p1_turn = True

p2 = SmartPlayer("./new_model13")

which_camel = {"red":1,"yellow":2,"green":3,"blue":4,"white":5}

while True:

    screen.fill((242,205,107))

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

    screen.blit(yellow,(screen_width//11 + (camel_spots[which_camel["yellow"]][0]-1)*screen_width//5,screen_height//6.5 - camel_spots[which_camel["yellow"]][1]*stack_height))
    screen.blit(red,(screen_width//11,screen_height//6.5 - stack_height))
    screen.blit(blue,(screen_width//11,screen_height//6.5 - 2*stack_height))
    screen.blit(green,(screen_width//11,screen_height//6.5 - 3*stack_height))
    screen.blit(white,(screen_width//11,screen_height//6.5 - 4*stack_height))

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

    if display:

        red_die = pygame.Rect(1.3*screen_width//5,screen_height-2*screen_height//5,50,50)
        pygame.draw.rect(screen,color_dict["red"],red_die)
        red_number = 1
        red_dice_text = smallfont.render(str(red_number) , True , (0,0,0))
        screen.blit(red_dice_text,(1.4*screen_width//5,screen_height-1.9*screen_height//5))

        blue_die = pygame.Rect(1.8*screen_width//5,screen_height-2*screen_height//5,50,50)
        pygame.draw.rect(screen,color_dict["blue"],blue_die)
        blue_number = 1
        blue_dice_text = smallfont.render(str(blue_number) , True , (0,0,0))
        screen.blit(blue_dice_text,(1.9*screen_width//5,screen_height-1.9*screen_height//5))

        green_die = pygame.Rect(2.3*screen_width//5,screen_height-2*screen_height//5,50,50)
        pygame.draw.rect(screen,color_dict["green"],green_die)
        green_number = 1
        green_dice_text = smallfont.render(str(green_number) , True , (0,0,0))
        screen.blit(green_dice_text,(2.4*screen_width//5,screen_height-1.9*screen_height//5))

        yellow_die = pygame.Rect(2.8*screen_width//5,screen_height-2*screen_height//5,50,50)
        pygame.draw.rect(screen,color_dict["yellow"],yellow_die)
        yellow_number = 1
        yellow_dice_text = smallfont.render(str(yellow_number) , True , (0,0,0))
        screen.blit(yellow_dice_text,(2.9*screen_width//5,screen_height-1.9*screen_height//5))

        white_die = pygame.Rect(3.3*screen_width//5,screen_height-2*screen_height//5,50,50)
        pygame.draw.rect(screen,color_dict["white"],white_die)
        white_number = 3
        white_dice_text = smallfont.render(str(white_number) , True , (0,0,0))
        screen.blit(white_dice_text,(3.4*screen_width//5,screen_height-1.9*screen_height//5))

    event = pygame.event.poll()
    mouse = pygame.mouse.get_pos()

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

    p1_score = 0
    p1_score_text = smallfont.render("p1 score: " + str(p1_score) , True , (0,0,0))
    screen.blit(p1_score_text,(1.2*screen_width//5,screen_height//2))

    p2_score = 0
    p2_score_text = smallfont.render("p2 score: " + str(p2_score) , True , (0,0,0))
    screen.blit(p2_score_text,(3*screen_width//5,screen_height//2))

    #if it is the human's move
    if p1_turn:


        if (roll_button_x < mouse[0] < roll_button_x + roll_button_w) and (roll_button_y < mouse[1] < roll_button_y + roll_button_h):
            pygame.draw.rect(screen,(134,100,68),roll_button)
            screen.blit(roll_button_text,(roll_button_x + roll_button_w//5,roll_button_y + roll_button_h//4))

            if event.type == pygame.MOUSEBUTTONDOWN:
                #roll die
                display = True



        if event.type == pygame.KEYDOWN:
            #quit
            break

        p1_turn = False

    else:
        state = p2.make_move(state)

        p1_turn = True

    # rolled_die = state.die
    # rolled_die_number = state.die_roll
    # board_state = state.board_state
    # dice_left = state.dice_left
    # bets_left = state.bets_left
    # camel_spots = state.camel_spots






    pygame.display.update()

pygame.quit()
