import numpy as np
import torch
from torch.utils.data import TensorDataset

import chess


class ChessConverter:
    def __init__(self):
        pass

    def convert_array(self, board):
        board_array = np.zeros((8, 8, 12), dtype=np.float32)
        piece_idx = {
            "p": 0,
            "P": 6,
            "n": 1,
            "N": 7,
            "b": 2,
            "B": 8,
            "r": 3,
            "R": 9,
            "q": 4,
            "Q": 10,
            "k": 5,
            "K": 11,
        }

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                rank, file = divmod(square, 8)
                board_array[7 - rank, file, piece_idx[piece.symbol()]] = 1.0
        return board_array

    def get_tensor_data(self, data, labels, stockfish_evals):
        data = torch.tensor(data).float()
        labels = torch.tensor(labels).float().view(-1, 1)
        stockfish_evals = torch.tensor(stockfish_evals).float().view(-1, 1)
        tensor_data = TensorDataset(data, labels, stockfish_evals)
        return tensor_data
