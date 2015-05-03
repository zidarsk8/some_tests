
from test_data import all_models
from test_data import integer_type_mappings
from random import choice
from random import randint
from collections import defaultdict
from test_models import StringType
from test_models import IntegerType
import time
import sys


class Benchmark(object):
  times = defaultdict(int)
  call_counts = defaultdict(int)

  def __init__(self, name, repeat=1):
    self.name = name
    self.repeat = repeat

  def __enter__(self):
    self.start = time.time()

  def __exit__(self, exc_type, exc_value, exc_trace):
    end = time.time()
    self.times[self.name] += end - self.start
    self.call_counts[self.name] += 1

  @classmethod
  def print_times(cls, repeat=1):
    for name, total_time in sorted(cls.times.items()):
      count = cls.call_counts[name]
      print("{:>30}: {:>9.5f} - {:>9.5f} - repeated {}".format(
          name, total_time, total_time / count, count))


def fill_data(engine=None, object_count=1000, batch_rows=1000, repeat=1):
  with Benchmark("fill data ({},{})".format(batch_rows, repeat)):
    for i in xrange(repeat):
      sys.stdout.write("inserting data: {:>5} / {:>5}\r".format(i, repeat))
      sys.stdout.flush()
      with Benchmark("generate single batch"):
        seed_str_dict = {}
        seed_int_dict = {}
        for _ in xrange(batch_rows):
          source_id = randint(1, object_count)
          source_name = choice(all_models)
          dest_id = randint(1, object_count)
          dest_name = choice(all_models)
          seed_str_dict[source_id, source_name, dest_id, dest_name] = {
              "source_id": source_id,
              "source_name": source_name,
              "dest_id": dest_id,
              "dest_name": dest_name,
          }
          seed_int_dict[source_id, source_name, dest_id, dest_name] = {
              "source_id": source_id,
              "source_type_id": integer_type_mappings[source_name],
              "dest_id": dest_id,
              "dest_type_id": integer_type_mappings[dest_name],
          }
        seed_str_data = seed_str_dict.values()
        seed_int_data = seed_int_dict.values()

        with Benchmark("insert integer_type data query"):
          try:
            insert_query = IntegerType.__table__.insert().values(seed_int_data)
            engine.execute(insert_query)
          except:
            pass

        with Benchmark("insert string_type data query"):
          try:
            insert_query = StringType.__table__.insert().values(seed_str_data)
            engine.execute(insert_query)
          except:
            pass
  print "inserting data: {:>5} / {:>5}".format(repeat, repeat)
