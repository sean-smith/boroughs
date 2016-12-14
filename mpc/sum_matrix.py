#!/usr/bin/env python

# Sean Smith 2016
# Sums a NxN matrix as supplied by --file
# To run:
# swsmith@bu.edu

from optparse import OptionParser
import viff.reactor
viff.reactor.install()
from twisted.internet import reactor

from viff.field import GF, GF256
from viff.runtime import Runtime, create_runtime, make_runtime_class, Share
from viff.comparison import ComparisonToft07Mixin
from viff.equality import ProbabilisticEqualityMixin
from viff.config import load_config
from viff.util import find_prime, dprint
import json
import pprint



def sum_matrix(m1, m2, m3, Zp, runtime):

  print "Summing matrixes"

  for i in range(len(m1)):
    m1[i] = m1[i] + m2[i] + m3[i]

  return m1



def main():
     # Parse command line arguments.
    parser = OptionParser(usage=__doc__)

    parser.add_option("--modulus",
                     help="lower limit for modulus (can be an expression)")
    parser.add_option("--file",
                     help="Input JSON file.")
    parser.set_defaults(modulus=2**65)
    Runtime.add_options(parser)
    options, args = parser.parse_args()

    if len(args) == 0:
        parser.error("you must specify a config file")

    Zp = GF(find_prime(options.modulus, blum=True))

    # Load configuration file.
    id, players = load_config(args[0])

    # load input JSON
    with open(options.file) as input_file:
      data = json.load(input_file)
      
      print "Input:"
      for i in data:
        print i

      runtime_class = make_runtime_class(mixins=[ComparisonToft07Mixin, ProbabilisticEqualityMixin])
      pre_runtime = create_runtime(id, players, 1, options, runtime_class)

      def run(runtime):
          print "Connected."

          # Secret Share matrixes
          m1 = []
          m2 = []
          m3 = []
          for row in data:
            for item in row:
              a, b, c = runtime.shamir_share([1, 2, 3], Zp, item)
              m1.append(a)
              m2.append(b)
              m3.append(c)
          
          # Point in Polygon Algorithm
          result = sum_matrix(m1, m2, m3, Zp, runtime)

          # Now open the result so we can see it.
          print "result:"
          for i in range(0, 38025, 195):
              dprint("[%d, %d, %d, %d, %d]", runtime.open(result[i]), runtime.open(result[i+1]), runtime.open(result[i+2]), runtime.open(result[i+3]), runtime.open(result[i+4]))
          exit()

          result.addCallback(lambda _: runtime.shutdown())

      pre_runtime.addCallback(run)

      # Start the Twisted event loop.
      reactor.run()

if __name__ == "__main__":
    main()
