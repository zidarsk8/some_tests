
from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.ext.declarative import declarative_base
from test_data import all_models

Base = declarative_base()

integer_type_mappings = {name: i for i, name in enumerate(all_models)}

class IntegerType(Base):
  __tablename__ = 'test_integer_type'

  id = Column(Integer, primary_key=True)

  source_id = Column(Integer, nullable=False)
  source_type_id = Column(Integer, nullable=False)
  dest_id = Column(Integer, nullable=False)
  dest_type_id = Column(Integer, nullable=False)

  def __repr__(self):
    return "{:>8} {:<15} --> {:>8} {:<15}".format(
        self.source_id,
        self.source_name,
        self.dest_id,
        self.dest_name)


class StringType(Base):
  __tablename__ = 'test_string_type'

  id = Column(Integer, primary_key=True)

  source_id = Column(Integer, nullable=False)
  source_name = Column(String(255), nullable=False)
  dest_id = Column(Integer, nullable=False)
  dest_name = Column(String(255), nullable=False)

  def __repr__(self):
    return "{:>8} {:<15} --> {:>8} {:<15}".format(
        self.source_id,
        self.source_name,
        self.dest_id,
        self.dest_name)


class ObjType(Base):
  __tablename__ = "test_object_types"
  id = Column(Integer, primary_key=True)
  object_name = Column(String(255), nullable=False)

  def __repr__(self):
    return self.object_name


Index('integer_type_source_index', IntegerType.source_id,
      IntegerType.source_type_id, unique=False)
Index('integer_type_dest_index', IntegerType.dest_id,
      IntegerType.dest_type_id, unique=False)
Index('integer_type_relationship', IntegerType.dest_id, IntegerType.dest_type_id,
      IntegerType.source_id, IntegerType.source_type_id, unique=True)


Index('string_type_source_index', StringType.source_id,
      StringType.source_name, unique=False)
Index('string_type_dest_index', StringType.dest_id,
      StringType.dest_name, unique=False)
Index('string_type_relationship', StringType.dest_id, StringType.dest_name,
      StringType.source_id, StringType.source_name, unique=True)
