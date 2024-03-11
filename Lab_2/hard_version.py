import random
from fastapi import FastAPI, HTTPException

app = FastAPI()

game_board = [[None for i in range(3)] for j in range(3)]
player_symbols = {}

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

@app.post("/start-game")
async def start_game():
    global player_symbols, game_board

    if len(player_symbols) != 2:
        raise HTTPException(status_code=400, detail="Need exactly 2 players to start the game")

    game_board = [[' ' for _ in range(3)] for _ in range(3)]

    players = list(player_symbols.keys())
    random.shuffle(players)
    player_symbols[players[0]] = 'X'
    player_symbols[players[1]] = 'O'

    return {"message": "Game started!", "player_symbols": player_symbols}

@app.post("/play-turn/{player_id}")
async def play_turn(player_id: str, x: int, y: int):
    global player_symbols, game_board

    if player_id not in player_symbols:
        raise HTTPException(status_code=404, detail="Player not found")

    winner = check_winner(game_board)
    if winner:
        return {"message": f"Game is already finished! Winner is {winner}"}

    if 0 <= x <= 2 and 0 <= y <= 2 and game_board[x][y] == ' ':

        game_board[x][y] = player_symbols[player_id]

        winner = check_winner(game_board)
        if winner:
            return {"message": f"Player {winner} wins!"}
        return {"message": "Move recorded", "game_board": game_board}
    else:
        raise HTTPException(status_code=400, detail="Invalid move")


@app.post("/register-player/{player_id}")
async def register_player(player_id: str):
    global player_symbols

    if len(player_symbols) >= 2 or player_id in player_symbols:
        raise HTTPException(status_code=400, detail="Player already registered or maximum players reached")

    player_symbols[player_id] = None
    return {"message": f"Player {player_id} registered"}


@app.get("/game-status")
async def game_status():
    global player_symbols, game_board
    return {"game_board": game_board, "player_symbols": player_symbols, "winner": check_winner(game_board)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)