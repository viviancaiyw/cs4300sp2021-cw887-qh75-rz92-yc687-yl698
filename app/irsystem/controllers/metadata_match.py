# num of players filtering, genres weighting
from app.irsystem.controllers import GENRE_KEY
from app.irsystem.models.movie import Movie
from app.irsystem.models.game import Game


def _gen_sql_query(raw_genre_list):
    """
    raw_genre_list: list of raw user genre input from the UI
    Returns: The sqlalchemy query for a give genre list to filter the game by    
    """
    genre_list = []
    if raw_genre_list is not None:
        for genre in raw_genre_list:
            genre_list.append(GENRE_KEY.get(genre, ''))
    query = "Game.query.filter(((Game.single_player == singleplayer) | (Game.multi_player == multiplayer)), ("
    for genre in genre_list:
        query = query + "Game.genre.like('%{}%')|".format(genre)
    if len(genre_list):
        query = query[:-1] + ')).all()'
    else:
        query = query[:-2] + ').all()'
    return query


def filter_games(singleplayer: bool, multiplayer: bool, raw_genre_list):
    """
    Returns: list of game ids filtered by number of players and list of input genre
    """
    query = _gen_sql_query(raw_genre_list)
    res_games = eval(query)
    res = [game.app_id for game in res_games]
    return res
