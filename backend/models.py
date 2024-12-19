from sqlalchemy import Integer, String, ForeignKey, Text, Enum, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __target_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    requests = relationship("Request", back_populates="user")


class Operator(Base):
    __tablename__ = 'operators'
    __target_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    requests = relationship("Request", back_populates="operator")


class Request(Base):
    __tablename__ = 'requests'
    __target_args__ = {"extend_existing": True}

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum(
            'init',
            'in_progress',
            'closed',
            name="request_status"
        ),
        nullable=False,
        default='init'
    )
    date_create: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.datetime.now())

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    operator_id: Mapped[int] = mapped_column(Integer, ForeignKey('operators.id'), nullable=True)

    user = relationship("User", back_populates="requests")
    operator = relationship("Operator", back_populates="requests")
