import pygame

# Initialize PyGame
# Fix sound latency issue
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()

# Color palette
blue = (78, 140, 243)
light_blue = (100, 100, 255)
red = (242, 89, 97)
light_red = (255, 100, 100)
dark_grey = (85, 85, 85)
light_grey = (100, 100, 100)
background_color = (225, 225, 225)

# Images
pvp_button = pygame.image.load("images/pvp.png")
pvp_button_rect = pvp_button.get_rect()
pvp_button_rect.center = (150, 156)
pvai_button = pygame.image.load("images/pvai.png")
pvai_button_rect = pvai_button.get_rect()
pvai_button_rect.center = (150, 236)
logo = pygame.image.load("images/logo.png")
cross_img = pygame.image.load("images/cross.png")
circle_img = pygame.image.load("images/circle.png")
preview_cross_img = pygame.image.load("images/preview_cross.png")
preview_circle_img = pygame.image.load("images/preview_circle.png")
restart_img = pygame.image.load("images/restart.png")
restart_hovered_img = pygame.image.load("images/restart_hovered.png")
X_score_img = pygame.image.load("images/X_score.png")
O_score_img = pygame.image.load("images/O_score.png")

# Create window
screen = pygame.display.set_mode((300, 350))
pygame.display.set_caption("Tic Tac Toe")

# Board
board = [["", "", ""],
         ["", "", ""],
         ["", "", ""]]

# Scoreboard
score = {"X": 0, "O": 0}
font = pygame.font.Font("freesansbold.ttf", 32)

def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

def draw_board():
    # Draw tiles
    for row in range(3):
        for col in range(3):
            pos = (row * 100 + 6, col * 100 + 6)
            if board[row][col] == "X":
                screen.blit(cross_img, pos)
            elif board[row][col] == "O":
                screen.blit(circle_img, pos)

    # Draw lines
    width = 10
    pygame.draw.line(screen, dark_grey, (100, 0), (100, 300), width)
    pygame.draw.line(screen, dark_grey, (200, 0), (200, 300), width)
    pygame.draw.line(screen, dark_grey, (0, 100), (300, 100), width)
    pygame.draw.line(screen, dark_grey, (0, 200), (300, 200), width)

def update_player(player):
    if player == "X":
        next_player = "O"
        preview_img = preview_circle_img
    elif player == "O":
        next_player = "X"
        preview_img = preview_cross_img
    return next_player, preview_img

def draw_bottom_menu(mouse):
    pygame.draw.rect(screen, dark_grey, (0, 300, 300, 50))
    pygame.draw.rect(screen, light_grey, (5, 305, 290, 40))
    screen.blit(restart_img, (250, 310))

    if 250 < mouse[0] < 282 and 310 < mouse[1] < 342:
        screen.blit(restart_hovered_img, (248, 308))

    screen.blit(X_score_img, (40, 310))
    screen.blit(O_score_img, (190, 310))
    scoreboard = font.render(": %d x %d :" % (score["X"], score["O"]), True, background_color, light_grey)
    screen.blit(scoreboard, (72, 310))

def visualize_move(row, col, preview_img):
    if board[row][col] == "":
        screen.blit(preview_img, (row * 100 + 6, col * 100 + 6))

def is_board_full():
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                return False
    return True

def reset_board():
    for row in range(3):
        for col in range(3):
            board[row][col] = ""

def is_winner(player):
    return ((board[0][0] == player and board[0][1] == player and board[0][2] == player) or
            (board[1][0] == player and board[1][1] == player and board[1][2] == player) or
            (board[2][0] == player and board[2][1] == player and board[2][2] == player) or
            (board[0][0] == player and board[1][0] == player and board[2][0] == player) or
            (board[0][1] == player and board[1][1] == player and board[2][1] == player) or
            (board[0][2] == player and board[1][2] == player and board[2][2] == player) or
            (board[0][0] == player and board[1][1] == player and board[2][2] == player) or
            (board[0][2] == player and board[1][1] == player and board[2][0] == player))

def verify_winner(player):
    if is_winner(player):
        play_sound("sounds/reset_sound.wav")
        score[player] += 1
        pygame.time.wait(500)
        reset_board()

def reset_game():
    reset_board()
    score["X"] = 0
    score["O"] = 0

def game(mode):
    pygame.mouse.set_pos(150, 175)
    player = "X"
    preview_img = preview_cross_img

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        row, col = int(mouse[0] / 100), int(mouse[1] / 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reset_game()
                running = False
            elif is_board_full():
                reset_board()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if row < 3 and col < 3 and board[row][col] == "":
                    board[row][col] = player
                    verify_winner(player)
                    player, preview_img = update_player(player)
                elif 250 < mouse[0] < 282 and 310 < mouse[1] < 342:
                    reset_game()

        screen.fill(background_color)
        draw_board()
        draw_bottom_menu(mouse)

        if row < 3 and col < 3 and mode == 0:
            visualize_move(row, col, preview_img)

        pygame.display.update()

def menu():
    running = True
    while running:
        screen.fill(background_color)
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pvp_button_rect.collidepoint((mx, my)):
                    play_sound("sounds/button_sound.wav")
                    game(0)
                # elif pvai_button_rect.collidepoint((mx, my)):
                    # play_sound("sounds/button_sound.wav")
                    # game(1)

        screen.blit(logo, (8, 25))
        pygame.draw.rect(screen, dark_grey, (45, 120, 210, 73))
        screen.blit(pvp_button, (50, 125))
        # pygame.draw.rect(screen, dark_grey, (45, 200, 210, 73))
        # screen.blit(pvai_button, (50, 205))
        pygame.display.update()

if __name__ == "__main__":
    menu()
