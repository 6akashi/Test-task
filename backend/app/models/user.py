from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import relationship
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    secondname = Column(String, nullable=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)

    role = relationship("Role", back_populates='users')

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', surname='{self.surname}', secondname='{self.secondname}', email='{self.email}')>"
