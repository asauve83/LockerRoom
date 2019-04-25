from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from LockerRoomDbSetup import Teams, Base, Players

engine = create_engine('sqlite:///LockerRoom.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Add Teams to the LockerRoom
'''class Teams(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    player_id = Column(Integer, ForeignKey('players.id'))
    player = reltionship(Players)'''

team = Teams(id=1, name="Yellow Snow", user_id=1)

session.add(team)
session.commit()

team = Teams(id=2, name="Team Skittle", user_id=1)

session.add(team)
session.commit()

team = Teams(id=3, name="Team Snuggle", user_id=1)

session.add(team)
session.commit()

team = Teams(id=4, name="Team America", user_id=1)

session.add(team)
session.commit()

team = Teams(id=5, name="Farley Athletics", user_id=1)

session.add(team)
session.commit()

team = Teams(id=6, name="North Stars", user_id=1)

session.add(team)
session.commit()

print "Added some teams!"
