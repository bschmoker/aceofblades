# -*- coding: utf-8 -*-`

# TODO - set rival in '/game'
# TODO - build data structure for card deck using random.shuffle()
# TODO - implement logic in /play for choosing and manipulating hand

# LATER - handle if opponent is none, can set later by hitting /game/challenge/rival_id
# LATER - send notification if rival_id is set

# LATER - sanitize user input using bleach and profanityfilter

import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import Player, PlayerMessage, Game, GameMessage
from models import StringMessage
from utils import get_by_urlsafe, uniq_id

PLAYER_REQUEST = endpoints.ResourceContainer(PlayerMessage)
GAME_REQUEST = endpoints.ResourceContainer(GameMessage)
GAME_LOOKUP_REQUEST = endpoints.ResourceContainer(game_id=messages.StringField(1, required=True ) )

@endpoints.api(name='aceofblades', version='v1')
class AceofBlades(remote.Service):
    """Game API"""
    @endpoints.method(request_message=PLAYER_REQUEST,
                      response_message=PlayerMessage,
                      path='player/new',
                      name='create_player',
                      http_method='POST' )
    def create_player(self, request):
        """Create a Player. Optionally set a (non)unique username"""
        
        player_name = None
        if request.desired_name is not None:
            player_name = request.desired_name
            
        player_id = uniq_id()
        
        player = Player(player_id = player_id, player_name=player_name)
        player.put()
        
        return player.to_message()

    @endpoints.method(request_message=GAME_REQUEST,
                      response_message=GameMessage,
                      path='game/new',
                      name='create_game',
                      http_method='POST' )
    def create_game(self, request):
        """create a new game """
        
        # look up initiating player
        slinger = Player.query(Player.player_id == request.player_id).get()
        
        if slinger is None:
            raise endpoints.BadRequestException('specified player_id not found')
            
        # generate new game 
        game_id = uniq_id()
        game = Game(game_id = game_id, slinger = slinger.key)
        game.put()
        
        return game.to_message()
                
    
    @endpoints.method(request_message=GAME_LOOKUP_REQUEST,
                      response_message=GameMessage,
                      path='game/{game_id}',
                      name='read_game',
                      http_method='GET' )
                      
    def read_game(self, request):
        """Get info about current game"""
        
        game = Game.query(Game.game_id == request.game_id).get()
        # note that primary key for Game is `game.key`
        if game is None:
            raise endpoints.BadRequestException('specified game_id not found')
            
            
        return game.to_message()
                
# --- RUN ---
api = endpoints.api_server([AceofBlades])