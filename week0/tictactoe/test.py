from tictactoe import read, player, actions, result, winner, terminal, utility
X = "X"
O = "O"
EMPTY = None
board = [[O, X, O],
        [O, X, X],
        [X, O, X]]
coords = read(board)
xcoords = coords[0]
ocoords = coords[1]
ecoords = coords[2]
print("xcoords:", xcoords, "number of X's", len(xcoords))
print("ocoords:", ocoords, "number of O's", len(ocoords))
print("ecoords:", ecoords, "number of EMPTY's", len(ecoords))

print(player(board))

print(actions(board))

#print(board)
#print(result(board,(1,1)))

print(terminal(board))
print(utility(board))
