from sqlalchemy import Column, ForeighKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Catalog(Base):
	__tablename__ = 'catalog'

	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)

	@property
	def serialize(self):
		""" Return object data in serializable format """
		return {
			'name':	self.name,
			'id':	self.id
		}

class Item(Base):
	__tablename__ = 'item'

	name = Column(String(250), nullable=False)
	id = Column(Integer, primary_key=True)
	description = Column(String)
	picture = Column(String)
	homepage = Column(String)
	catalog_id = Column(Integer, ForeighKey('catalog.id'))
	catalog = relationship(Catalog)

	@property
	def serialize(self):
	   	""" Return object data in serializable format """
		return {
			'name':			self.name,
			'id':			self.id,
			'description':	self.description,
			'picture':		self.picture,
			'homepage':		self.homepage
		}
	
engine = create_engie('sqlite:///items_in_kyoto.db')

Base.metadata.create_all(engine)
