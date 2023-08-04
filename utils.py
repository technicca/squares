import pygame
import chess
from stockfish import Stockfish

def load_pieces(PIECE_SIZE):
    pieces = {}
    for piece in ['p', 'r', 'n', 'b', 'q', 'k', 'P', 'R', 'N', 'B', 'Q', 'K']:
        piece_image = pygame.image.load(f'img/{piece}.png')
        pieces[piece] = pygame.transform.scale(piece_image, PIECE_SIZE)
    return pieces

def get_legal_moves(game_state, selected_square):
    return [move for move in game_state.legal_moves if move.from_square == selected_square]