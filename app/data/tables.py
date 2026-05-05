import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Table(SerializerMixin, SqlAlchemyBase):
    __tablename__ = "tables"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String)

    trainings = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)

    food = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)

    deals = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    user = orm.relationship('User')
