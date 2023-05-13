from sqlalchemy import DECIMAL, INTEGER, TIMESTAMP, VARCHAR, Column, ForeignKey, FLOAT
from sqlalchemy.dialects.mysql import TEXT, TINYINT, VARCHAR
from sqlalchemy.dialects.mysql.types import TINYTEXT
from sqlalchemy.ext.declarative import declarative_base

# generated with sqlacodegen
Base = declarative_base()
metadata = Base.metadata


# class Registration(Base):
#     __tablename__ = "registration"

#     user_id = Column(INTEGER, primary_key=True)
#     email = Column(VARCHAR(320))  # max email length
#     password = Column(TINYTEXT)
#     timestamp_created = Column(
#         TIMESTAMP,
#     )
#     phone = Column(TINYTEXT)
#     first_name = Column(TINYTEXT)
#     last_name = Column(TINYTEXT)
#     birthdate = Column(TIMESTAMP)
#     about_you = Column(TEXT)
#     gender = Column(TINYINT)
#     account_type = Column(TINYINT)
#     facebook = Column(TINYINT)
#     instagram = Column(TINYINT)
#     timestamp_edited = Column(TIMESTAMP)


class PokerStats(Base):
    __tablename__ = "poker_stats"

    id = Column(INTEGER, primary_key=True)
    name = Column(TINYTEXT)
    winnings = Column(INTEGER)
    date_played = Column(
        TIMESTAMP,
    )