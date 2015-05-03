from random import choice
from random import randint
import sqlalchemy
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from test_data import all_models, integer_type_mappings
from test_helpers import Benchmark, fill_data
from test_models import StringType
from test_models import IntegerType
from test_models import Base
import sys

print sqlalchemy.__version__

object_count = 100
batch_rows = 100
insert_repeat = 100
repeat = 10000

engine = create_engine(
    "mysql+mysqldb://root:root@localhost/ggrcdev", echo=False)

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

Base.metadata.create_all(engine)

fill_data(engine=engine, object_count=object_count,
          batch_rows=batch_rows, repeat=insert_repeat)

with Benchmark("all"):
  found = 0
  for i in xrange(repeat):
    sys.stdout.write("running queries: {:>5} / {:>5}\r".format(i, repeat))
    sys.stdout.flush()
    with Benchmark("random object"):
      obj_id = randint(1, object_count)
      obj_name = choice(all_models)
      obj_type_id = integer_type_mappings[obj_name]
    with Benchmark("find integer_type query"):
      found += session.query(IntegerType).filter(and_(
          IntegerType.source_id == obj_id,
          IntegerType.source_type_id == obj_type_id,
      )).count()
    with Benchmark("find string_type query"):
      found += session.query(StringType).filter(and_(
          StringType.source_id == obj_id,
          StringType.source_name == obj_name,
      )).count()
  print "running queries: {:>5} / {:>5}".format(repeat, repeat)
  print "found: {}".format(found)

Benchmark.print_times(repeat)

print session.query(StringType).count()
