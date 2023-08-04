import pygame
import chess
from stockfish import Stockfish

# Dimensions for the game window
WIN_WIDTH, WIN_HEIGHT = 600, 600
# Dimension for the side choosing buttons
BUTTON_WIDTH, BUTTON_HEIGHT = 80, 30

# Load the images
pieces = {}
for piece in ['p', 'r', 'n', 'b', 'q', 'k', 'P', 'R', 'N', 'B', 'Q', 'K']:
    pieces[piece] = pygame.image.load(f'img/{piece}.png')

board = pygame.image.load('img/board.png')

# Initialize Pygame and set up the display window
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Set up the game clock
clock = pygame.time.Clock()

# Set up the Stockfish engine
stockfish = Stockfish()

# Creating buttons for side selection
font = pygame.font.Font(None, 32)
white_button = pygame.Rect(WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
black_button = pygame.Rect(WIN_WIDTH // 2 + 20, WIN_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)

# Side choosing loop
run = True
side_chosen = False
side = ''
while run and not side_chosen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position
            # checks if mouse position is over the button
            if white_button.collidepoint(mouse_pos):
                # prints current location of mouse
                side = 'white'
                side_chosen = True
            elif black_button.collidepoint(mouse_pos):
                side = 'black'
                side_chosen = True

    # Filling the background
    screen.fill((30, 30, 30))

    # Render side choosing buttons
    pygame.draw.rect(screen, (255, 255, 255), white_button)
    pygame.draw.rect(screen, (0, 0, 0), black_button)

    w_text = font.render('White', True, (0, 0, 0))
    screen.blit(w_text, (white_button.x + (white_button.w - w_text.get_width()) // 2, 
                         white_button.y + (white_button.h - w_text.get_height()) // 2))

    b_text = font.render('Black', True, (255, 255, 255))
    screen.blit(b_text, (black_button.x + (black_button.w - b_text.get_width()) // 2, 
                         black_button.y + (black_button.h - b_text.get_height()) // 2))

    pygame.display.flip()  # updates the screen

# Chess board: python-chess library
board = chess.Board()

# If player chooses black, then Stockfish makes the first move
if side.lower() == "black":
    result = stockfish.get_best_move()
    board.push_uci(result)

# Variables to store the selected piece and its square
selected_piece = None
selected_square = ''

# Main game loop
run = True
while run:
    clock.tick(64)  # 64 frames per second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if selected_piece is None:
                selected_square = chess.square(x // 75, 7 - y // 75)
                selected_piece = board.piece_at(selected_square)
            else:
                move = chess.Move(selected_square, chess.square(x // 75, 7 - y // 75))
                if move in board.legal_moves:
                    board.push(move)
                    stockfish.set_position(board.move_stack)
                    result = stockfish.get_best_move()
                    board.push_uci(result)
                else:
                    print('Illegal move')
                selected_piece = None
                
    # Drawing the chessboard
    screen.blit(board, (0, 0))

    # Drawing the pieces
    for i in range(8):
        for j in range(8):
            piece = board.piece_at(chess.square(i, j))
            if piece:
                screen.blit(pieces[str(piece)], (i*75, (7-j)*75))

    pygame.display.flip()  # updates the display

pygame.quit()
