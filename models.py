"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb

class UserMessage(messages.Message):
    desired_name = messages.StringField(1)

class User(ndb.Model):
    """User profile"""
    player_id = ndb.StringProperty(required=True)
    player_name =ndb.StringProperty()


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
