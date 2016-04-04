from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Catalog(Base):
	__tablename__ = 'catalog'

	name = Column(String(50), nullable = False)
	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return {
			'name':			self.name,
			'id':			self.id
		}

class Item(Base):
	__tablename__ = 'item'

	name = Column(String(250), nullable = False)
	description = Column(String)
	picture_url = Column(String)
	homepage_url = Column(String)
	id = Column(Integer, primary_key = True)
	catalog_id = Column(Integer, ForeignKey('catalog.id'))
	catalog = relationship(Catalog)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return {
			'name':			self.name,
			'description':	self.description,
			'picture_url':	self.picture_url,
			'homepage_url':	self.homepage_url,
			'id':			self.id
		}

engine = create_engine('sqlite:///items_in_kyoto.db')
Base.metadata.create_all(engine)