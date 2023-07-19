#  Rice University - Computer Science
#
#  Mini-max Tic-Tac-Toe Player
#
#  Written for Python 2
#
#  Student: Saman Saybani

import poc_ttt_gui
import poc_ttt_provided as provided
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES
SCORES = {
    provided.PLAYERX: 1,
    provided.DRAW: 0,
    provided.PLAYERO: -1
    }


def mm_move(board, player):
    ''' Makes a move on the board '''
    if board.check_win() != None:
        return SCORES[board.check_win()], (-1,-1)

    else:
        top_score = -1
        top_square = (-1,-1)

        for square in board.get_empty_squares():
            cloned_board = board.clone()
            cloned_board.move(square[0], square[1], player)
            square_result = mm_move(cloned_board, provided.switch_player(player))
            current_score = square_result[0] * SCORES[player]

            if current_score == 1:
                return square_result[0], square

            if current_score >= top_score:
                top_score = current_score
                top_square = square

        return top_score * SCORES[player], top_square


def move_wrapper(board, player):
    ''' Wrapper to allow the use of the same infrastructure that was used for Monte Carlo Tic-Tac-Toe '''
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Run the GUI
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
