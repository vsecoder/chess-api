from . import Base
from sqlalchemy import Column, Integer, String
from db import session

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    games_win = Column(Integer)
    games_lose = Column(Integer)

    @classmethod
    def create(cls, token, name):
        profile = cls(token=token, name=name, games_win=0, games_lose=0)
        session.add(profile)
        session.commit()
        return profile
    
    @classmethod
    def get(cls, id):
        return session.query(Users).filter_by(id=id).first()

    def delete(self):
        session.delete(self)
        session.commit()

    def to_dict(self):
        if type(self) == list:
            return [user.to_dict() for user in self]
        return {
            'id': self.id,
            'token': self.token,
            'name': self.name,
            'games_win': self.games_win,
            'games_lose': self.games_lose
        }

    def __repr__(self):
        return f'{self.name}'

    def __init__(self, name, token, games_win, games_lose):
        self.name = name
        self.token = token
        self.games_win = games_win
        self.games_lose = games_lose

    def getGames(self):
        pass

    def createGame(self, name, description, date, time, is_public):
        pass