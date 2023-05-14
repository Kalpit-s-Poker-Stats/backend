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

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TINYTEXT)
    biggest_win = Column(INTEGER)
    biggest_loss = Column(INTEGER)
    date_of_biggest_win = Column(DATE)
    date_of_biggest_loss = Column(DATE)
    average_all_time_win_or_loss = Column(INTEGER)
    positive_percentage = Column(INTEGER)
    negative_percentage = Column(INTEGER)
    number_of_sessions_positive = Column(INTEGER)
    number_of_sessions_negative = Column(INTEGER)
    total_sessions_played = Column(INTEGER)


class Session(Base):
    __tablename__ = "session"

    id = Column(INTEGER, primary_key=True)
    winnings = Column(INTEGER)
    buy_in_amount = Column(INTEGER)
    buy_out_amount = Column(INTEGER)
    location = Column(TINYTEXT)
    date = Column(DATE)