import datetime
from typing import Optional
from uuid import uuid4
from sqlmodel import Relationship, SQLModel, Field


class User(SQLModel, table=True):
    id: str = Field(default=str(uuid4()), primary_key=True)
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    image: bytes
    cart: list["Item"] = Relationship(back_populates="user")
    comments: list["Comment"] = Relationship(back_populates="user")


class Item(SQLModel, table=True):
    id: str = Field(default=str(uuid4()), primary_key=True)
    category: str
    name: str = Field(unique=True)
    colors: str
    rating: int
    image: bytes
    sizes: str
    price: float
    comments: list["Comment"] = Relationship(back_populates="item")
    description: "Description" = Relationship(back_populates="item")
    user_id: Optional[str] = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="cart")


class Description(SQLModel, table=True):
    id: str = Field(default=str(uuid4()), primary_key=True)
    markdown: str
    item_id: str = Field(foreign_key="item.id")
    item: "Item" = Relationship(back_populates="description")


class Comment(SQLModel, table=True):
    id: str = Field(default=str(uuid4()), primary_key=True)
    variant: str
    date: datetime.datetime = Field(default=datetime.datetime.now())
    rating: int
    message: str
    name: str
    item_id: str = Field(foreign_key="item.id")
    user_id: str = Field(foreign_key="user.id")
    item: "Item" = Relationship(back_populates="comments")
    user: "User" = Relationship(back_populates="comments")
