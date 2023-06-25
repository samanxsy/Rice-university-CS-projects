"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
# do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0   # Score for squares played by the current player
SCORE_OTHER = 1.0     # Score for squares played by the other player


def mc_trial(board, player):
    """
    Plays a single game
    """
    winner = None
    player_x = player

    while not winner:
        row = random.randrange(board.get_dim())
        col = random.randrange(board.get_dim())

        if board.square(row, col) == provided.EMPTY:
            board.move(row, col, player_x)
            winner = board.check_win()
            player_x = provided.switch_player(player_x)


def mc_update_scores(scores, board, player):
    """
    The function scores the completed board and updates the scores grid
    """
    winner = board.check_win()
    if winner == player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] += SCORE_CURRENT
                if board.square(row, col) == provided.switch_player(player):
                    scores[row][col] -= SCORE_OTHER

    if winner == provided.switch_player(player):
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] -= SCORE_CURRENT
                if board.square(row, col) == provided.switch_player(player):
                    scores[row][col] += SCORE_OTHER


def get_best_move(board, scores):
    """
    Finds all of the empty squares with the maximum score
    and randomly returns one of them as a (row,column) tuple
    """
    score_list = board.get_empty_squares()
    max_score_list = []

    if len(score_list) > 0:
        top_square = score_list[0]

        for square in score_list:
            if scores[square[0]][square[1]] > scores[top_square[0]][top_square[1]]:
                top_square = square
                max_score_list = []
            if scores[square[0]][square[1]] == scores[top_square[0]][top_square[1]]:
                top_square = square

            max_score_list.append(top_square)

        return random.choice(max_score_list)


def mc_move(board, player, trials):
    """
    Monte carlo simulation chooses the best_move
    """
    scores = [[0 for dummycol in range(board.get_dim())] for dummyrow in range(board.get_dim())]

    for _ in range(trials):
        current_board = board.clone()
        mc_trial(current_board, player)
        mc_update_scores(scores, current_board, player)

    return get_best_move(board, scores)


# provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
