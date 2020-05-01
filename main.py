import pygame
import random

'''
3x3 grid in the middle of the screen
random computer actions
'''

pygame.font.init()

# GLOBAL VARIABLES
SC_WIDTH = 700
SC_HEIGHT = 500
TET_WIDTH = 240
TET_HEIGHT = 240
CUBE_SIZE = 80

TOP_LEFT_X = (SC_WIDTH - TET_WIDTH) // 2
TOP_LEFT_Y = (SC_HEIGHT - TET_HEIGHT) // 2

BOARD = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]]


def computer_move(grid):
    # determine empty box
    empty = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                empty.append([i, j])
    # randomly make a move
    pos = random.choice(empty)
    grid[pos[0]][pos[1]] = 2
    return grid


def check_win(grid):
    needs_to_be_checked = []
    # horizontal board
    for row in grid:
        needs_to_be_checked.append(row)
    # vertical board
    for col in zip(*grid):
        needs_to_be_checked.append(list(col))
    # diagonal board
    diagonal1 = []
    diagonal2 = []
    for i in range(len(grid)):
        diagonal1.append(grid[i][i])
        diagonal2.append(grid[i][2 - i])
    needs_to_be_checked.append(diagonal1)
    needs_to_be_checked.append(diagonal2)
    # check if 3 of the same value exist
    for value in needs_to_be_checked:
        if set(value) == {1}:
            return 1
        elif set(value) == {2}:
            return 2


# not doing the score for now
# def draw_score(surface, p_score, c_score):
#     font = pygame.font.SysFont("comicsans", 30)
#     player_score_lbl = font.render(f"Player: {p_score}", 1, (255, 255, 255))
#     enemy_score_lbl = font.render(f"Computer: {c_score}", 1, (255, 255, 255))
#     surface.blit(player_score_lbl, (100 - player_score_lbl.get_width() // 2,
#                                     SC_HEIGHT // 2 - player_score_lbl.get_height() // 2 - 100))
#     surface.blit(enemy_score_lbl, (SC_WIDTH - 100 - enemy_score_lbl.get_width() // 2,
#                                    SC_HEIGHT // 2 - enemy_score_lbl.get_height() // 2 - 100))


def draw_moves(surface, grid):
    font = pygame.font.SysFont("comicsans", 90)
    for i in range(len(grid)):
        for j, k in enumerate(grid[i]):
            # if O
            if k == 1:
                lbl = font.render("O", 1, [255, 255, 0])
                surface.blit(lbl, (TOP_LEFT_X + j * CUBE_SIZE + (CUBE_SIZE / 2 - lbl.get_width() / 2),
                                   TOP_LEFT_Y + i * CUBE_SIZE + (CUBE_SIZE / 2 - lbl.get_height() / 2)))
            # if X
            if k == 2:
                lbl = font.render("X", 1, [255, 255, 0])
                surface.blit(lbl, (TOP_LEFT_X + j * CUBE_SIZE + (CUBE_SIZE / 2 - lbl.get_width() / 2),
                                   TOP_LEFT_Y + i * CUBE_SIZE + (CUBE_SIZE / 2 - lbl.get_height() / 2)))
    pygame.display.update()


def draw_grid(surface, grid):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y

    grids = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            g = pygame.Rect(sx + i * CUBE_SIZE, sy + j * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
            grids.append(g)

    for g in grids:
        pygame.draw.rect(surface, (255, 255, 255), g, 4)

    return grids


def draw_window(surface):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont("comicsans", 70)
    title_lbl = font.render("Tic Tac Toe", 1, (255, 255, 255))
    surface.blit(title_lbl, (TOP_LEFT_X + TET_WIDTH // 2 - title_lbl.get_width() // 2, 50))

    grids = draw_grid(surface, BOARD)
    return grids


def main(win):
    pygame.init()
    run = True
    board = BOARD
    font = pygame.font.SysFont("comicsans", 90)
    clock = pygame.time.Clock()
    grids = draw_window(win)

    while run:
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            # detect input
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, grid in enumerate(grids):
                    if grid.collidepoint(event.pos):
                        if i <= 2:
                            y = 0
                        elif 2 < i <= 5:
                            y = 1
                        elif 5 < i <= 8:
                            y = 2
                        x = i % 3
                        # draw player move
                        board[x][y] = 1
                        draw_moves(win, board)
                        if check_win(board) == 1:
                            lbl = font.render("You won! PogChamp", 1, (255, 0, 0), (0, 0, 0))
                            win.blit(lbl,
                                     (SC_WIDTH // 2 - lbl.get_width() // 2, SC_HEIGHT // 2 - lbl.get_height() // 2))
                            break
                        pygame.time.delay(1000)
                        # draw computer move
                        board = computer_move(board)
                        draw_moves(win, board)
                        if check_win(board) == 2:
                            lbl = font.render("You lost! LUL", 1, (255, 0, 0), (0, 0, 0))
                            win.blit(lbl,
                                     (SC_WIDTH // 2 - lbl.get_width() // 2, SC_HEIGHT // 2 - lbl.get_height() // 2))
                            break
        pygame.display.update()


def main_menu(win):
    run = True
    font = pygame.font.SysFont("comicsans", 90)
    lbl = font.render("Press any key to play", 1, (255, 255, 255))
    while run:
        win.fill((0, 0, 0))
        win.blit(lbl, (SC_WIDTH // 2 - lbl.get_width() // 2, SC_HEIGHT // 2 - lbl.get_height() // 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                main(win)
    pygame.display.quit()


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")
    main_menu(win)
