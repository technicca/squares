import pygame
import chess
from stockfish import Stockfish

# initialize our pygame module 
pygame.init()

# setting up our display screen
screen = pygame.display.set_mode((600, 600))

# setting up the stockfish engine
stockfish = Stockfish()

# Chess board using python-chess library
board = chess.Board()

# Ask player to choose their side
side = input("Choose your side (white/black): ")

# If player chooses black, let Stockfish make the first move
if side.lower() == "black":
    result = stockfish.get_best_move()
    board.push_uci(result)

# Main game loop
clock = pygame.time.Clock()   # Initialize the clock
run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Printing the result on the pygame window
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 50)

    for i in range(8):
        for j in range(8):
            if board.piece_at(chess.square(j, 7 - i)):
                piece = str(board.piece_at(chess.square(j, 7 - i)))
                text = font.render(piece, True, (0, 128, 0))
                screen.blit(text, pygame.draw.rect(screen, (255, 255, 255), [j * 75, i * 75, 75, 75]))

    pygame.display.flip()

    # Player makes a move
    move = input("Enter move: ")
    if chess.Move.from_uci(move) in board.legal_moves:
        board.push_uci(move)
        # Update Stockfish with the current board state
        stockfish.set_position(board.move_stack)
        # Stockfish makes a move
        result = stockfish.get_best_move()
        board.push_uci(result)
    else:
        print("Illegal move! Try again...")

pygame.quit()
