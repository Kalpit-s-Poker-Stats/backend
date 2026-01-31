from sqlalchemy import DECIMAL, INTEGER, TIMESTAMP, VARCHAR, Column, ForeignKey, FLOAT, DATE
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


class Profile(Base):
    __tablename__ = "profile"

    discord_id = Column(VARCHAR(256))
    creation_timestamp = Column(TIMESTAMP)
    last_updated_timestamp = Column(TIMESTAMP)
    pn_id = Column(VARCHAR(256), primary_key=True)
    splitwise_id = Column(INTEGER)
    discord_username = Column(VARCHAR(256))
    name = Column(TINYTEXT)
    all_time_total = Column(FLOAT)
    biggest_win = Column(FLOAT)
    biggest_loss = Column(FLOAT)
    date_of_biggest_win = Column(DATE)
    date_of_biggest_loss = Column(DATE)
    average_all_time_win_or_loss = Column(FLOAT)
    positive_percentage = Column(FLOAT)
    negative_percentage = Column(FLOAT)
    number_of_sessions_positive = Column(INTEGER)
    number_of_sessions_negative = Column(INTEGER)
    total_sessions_played = Column(INTEGER)
    acknowledgment_accepted = Column(INTEGER)


class Session(Base):
    __tablename__ = "session"

    entry_number = Column(INTEGER, primary_key=True, autoincrement=True)
    hashId = Column(VARCHAR(250))
    date_entered = Column(TIMESTAMP)
    pn_id = Column(TINYTEXT)
    winnings = Column(FLOAT)
    buy_in_amount = Column(FLOAT)
    buy_out_amount = Column(FLOAT)
    location = Column(VARCHAR(256))
    date = Column(DATE)


class Leaderboard(Base):
    __tablename__ = ""

    pn_id = Column(TINYTEXT, primary_key=True)
