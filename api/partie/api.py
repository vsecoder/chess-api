from sanic.response import json
from sanic import blueprints
from components.Users import Users
from components.Parties import Parties
from sanic import exceptions

import chess

def get_board(board):
    if not board:
        board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    return chess.Board(board)

def is_legal_move(board, move):
    return move in board.legal_moves

def convert(fen):
    fen = fen.split(' ')[0]
    fen = fen.split('/')
    fen = [list(x) for x in fen]
    for i in range(len(fen)):
        for j in range(len(fen[i])):
            if fen[i][j].isdigit():
                fen[i][j] = int(fen[i][j])
    return fen

api = blueprints.Blueprint('partie_api', url_prefix='/partie')

@api.route('/ping')
async def ping(request):
    return json({'ping': 'pong'})

@api.route('/get/<id:int>')
async def get_user_partie(request, id: int):
    """
    Get a chess game

    :param id: partie id
    :type id: int
    :return: json
    :rtype: json
    """
    partie = Parties.get(id)
    if partie:
        return json(partie.to_dict())
    else:
        raise exceptions.NotFound('Partie not found')

@api.route('/create', methods=['POST'])
async def create_partie(request):
    """
    Create a new chess game

    :return: json
    :rtype: json

    :Example:
    data = {
        'white': 123,
        'black': 456,
    }
    """
    data = request.json
    if not 'white' in request.json or not 'black' in request.json:
        return json({'error': 'Missing data'})
    if data['white'] == data['black']:
        return json({'error': 'White and black are the same'})
    white = Users.get(data['white'])
    black = Users.get(data['black'])
    if not white or not black:
        return json({'error': 'User not found'})

    partie = Parties.createGame(
        white=data['white'],
        black=data['black']
    )
    return json(partie.to_dict())

@api.route('/move/<id:int>', methods=['POST'])
async def move_partie(request, id: int):
    """
    Make a move in a chess game

    :return: json
    :rtype: json

    :Example:
    data = {
        'id': 123,
        'move': 'e2e4'
    }
    """
    try:
        data = request.json
        if not 'id' in request.json or not 'move' in request.json:
            return json({'error': 'Missing data'})

        partie = Parties.get(id)
        
        if not partie:
            return json({'error': 'Partie not found'})
        partie_json = partie.to_dict()

        user = Users.get(data['id'])

        if not user:
            return json({'error': 'User not found'})
        user = user.to_dict()
        
        state = ''
        if int(partie_json['white']) == user['id']:
            state = 'white'
        elif int(partie_json['black']) == user['id']:
            state = 'black'
        else:
            return json({'error': 'User not in this game'})

        partie_json = partie.to_dict()
        board = get_board(partie_json['board'])

        move_str = data['move']
        move = chess.Move.from_uci(move_str)
        if board.is_game_over():
            return json({'error': 'Game is over\nWinner: ' + board.result()})
        if is_legal_move(board, move):
            if state == 'white' and board.turn == chess.BLACK:
                return json({'error': 'Not your turn'})
            elif state == 'black' and board.turn == chess.WHITE:
                return json({'error': 'Not your turn'})
            board.push(move)
            #print(board)
            partie.move(move_str, board.fen())
        else:
            #print(board)
            return json({'error': 'Illegal move'})

        return json({'board': convert(board.fen())})
    except Exception as e:
        return json({'error': str(e)})

@api.route('/get_moves/<id:int>')
async def get_moves_partie(request, id: int):
    """
    Get moves of a chess game

    :param id: partie id
    :type id: int
    :return: json
    :rtype: json
    """
    partie = Parties.get(id)
    if partie:
        return json(partie.to_dict()['moves'])
    else:
        raise exceptions.NotFound('Partie not found')