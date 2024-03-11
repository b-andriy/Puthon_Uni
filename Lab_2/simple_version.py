from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI()

board = [[None for i in range(3)] for j in range(3)]

def check_for_winer(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_board(board):
    for row in board:
        if None in row:
            return False
    return True

def move(row: int, col: int, player: str):
    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] is None:
        board[row][col] = player
        return True
    return False

@app.post("/move")
async def move_1(row: int, col: int, player: str):
    if player not in ['x', 'o']:
        return {"message": "Invalid player. Player must be 'x' or 'o'."}

    if move(row, col, player):
        if check_for_winer(board, player):
            return {"message": f"Player {player} is winner!"}
        elif check_board(board):
            return {"message": "Tie!!!!"}
        else:
            return {"message": "Move sucsesfull!"}
    else:
        return {"message": "This row col is ocupated!!"}

@app.get("/board")
async def get_board():
    return {"board": board}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080 )