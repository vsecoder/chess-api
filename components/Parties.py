from . import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from datetime import datetime
from db import session

class Parties(Base):
    __tablename__ = 'parties'
    id = Column(Integer, primary_key=True, autoincrement=True)
    moves = Column(String)
    board = Column(String)
    white = Column(Integer, ForeignKey('users.id'))
    black = Column(Integer, ForeignKey('users.id'))
    date = Column(String)
    status = Column(Integer)
        
    @classmethod
    def get(cls, id):
        return session.query(cls).filter_by(id=id).first()

    def delete(self):
        session.delete(self)
        session.commit()
    
    def to_dict(self):
        if type(self) == list:
            return [event.to_dict() for event in self]
        return {
            'id': self.id,
            'moves': self.moves,
            'board': self.board,
            'white': self.white,
            'black': self.black,
            'date': self.date,
            'status': self.status
        }

    def __repr__(self):
        return "<Parties(name='%s', description='%s')>" % (self.title, self.text)

    def __init__(self, moves, board, white, black, date, status):
        self.moves = moves
        self.board = board
        self.white = white
        self.black = black
        self.date = date
        self.status = status

    @classmethod
    def create(cls, white, black, date):
        partie = cls(moves="", white=white, black=black, date=date, status=0, board="")
        session.add(partie)
        session.commit()
        return partie

    @classmethod
    def createGame(cls, white, black):
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        partie = cls.create(white, black, date)
        return partie

    def move(self, move, board):
        self.board = board
        self.moves = self.moves + " " + move
        session.commit()