from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from LockerRoomDbSetup import Teams, Base, Players, User

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


# Add Players to Teams
'''class Players(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    age = Column(Integer)
    phone = Column(String(13))
    homeAddress = Column(String(80))
    emailAddress = Column(String(80))
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship(Teams)'''

player = Players(id=1, name="Mark", team_id=1, user_id=1)

session.add(player)
session.commit()

player = Players(id=2, name="Mo", team_id=2, user_id=1)

session.add(player)
session.commit()

player = Players(id=3, name="Jay", team_id=3, user_id=1)

session.add(player)
session.commit()

player = Players(id=4, name="Brian", team_id=4, user_id=1)

session.add(player)
session.commit()

player = Players(id=5, name="Robin", team_id=5, user_id=1)

session.add(player)
session.commit()

player = Players(id=6, name="Luke", team_id=6, user_id=1)

session.add(player)
session.commit()

user = User(id=1, name="Anthony", email="anthonyfsauve@gmail.com")

session.add(user)
session.commit()

print "Added some players!"
