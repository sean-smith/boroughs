#!/usr/bin/env python

# Sean Smith 2016
# Based on viff divide.py
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

def bits_to_val(bits):
    return sum([2**i * b for (i, b) in enumerate(reversed(bits))])

def x(lnglat):
  return lnglat[0]

def y(lnglat):
  return lnglat[1]

def convert_to_int(num):
  return int(num * 10**13)

def point_in_poly(lat, lng, Zp, runtime):
  for feature in geo['features']:
    polygon = feature["geometry"]["coordinates"]
    is_multipolygon = feature["geometry"]["type"] == "MultiPolygon"
  
    for coord in polygon:
      print("one")
      if is_multipolygon:
        coord = coord[0]
      c = False
      j = len(coord) - 1;
      print("two")
      for i in range(len(coord)):
        px = lng
        py = lat
        print("three")
        print(runtime.id)

        x_i = convert_to_int(coord[i][0])
        y_i = convert_to_int(coord[i][1])
        x_j = convert_to_int(coord[j][0])
        y_j = convert_to_int(coord[j][1])
        

        print "(%d, %d) -> (%d, %d)" % (x_i, y_i, x_i, y_i)

        print("four")
        # First Equality, check if is in x
        r1 = (y_i<py) != (y_j>py)

        print("five")
        # Get left and right side for division
        left = (x_j-x_i) * (py-y_i)
        right = ((y_j-y_i) + x_i) 
        
        print("six")
        # divide left and right
        bits = []
        l = 10
        for m in range(l, -1, -1):
          t = 2**m * right
          cmp = t <= left
          bits.append(cmp)
          left = left - t * cmp
        div = bits_to_val(bits)

        print("seven")
        # Second Equality
        r2 = px < div

        print("eight")
        print(r1)
        print(r2)
        # Change Parity
        if (r1 == r2):
          c = not c
        print("nine")
      if c:
        return feature["properties"]['BoroCode']

  return 6


with open('../nyc_simple.json') as datafile:
  geo = json.load(datafile)


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
      start_lat = convert_to_int(data['start_lat'])
      start_long = convert_to_int(data['start_long'])
      end_lat = convert_to_int(data['end_lat'])
      end_long = convert_to_int(data['end_long'])
      print "(%d, %d) -> (%d, %d)" % (start_lat, start_long, end_lat, end_long)

      runtime_class = make_runtime_class(mixins=[ComparisonToft07Mixin, ProbabilisticEqualityMixin])
      pre_runtime = create_runtime(id, players, 1, options, runtime_class)

      def run(runtime):
          print "Connected."

          a_start_lat, b_start_lat, c_start_lat = runtime.shamir_share([1, 2, 3], Zp, start_lat)
          a_start_long, b_start_long, c_start_long = runtime.shamir_share([1, 2, 3], Zp, start_long)
          a_end_lat, b_end_lat, c_end_lat = runtime.shamir_share([1, 2, 3], Zp, end_lat)
          a_end_long, b_end_long, c_end_long = runtime.shamir_share([1, 2, 3], Zp, end_long)

          # Point in Polygon Algorithm
          result = point_in_poly(a_start_lat, b_start_long, Zp, runtime)

          print(5)

          # Now open the result so we can see it.
          dprint("The output is: %s", runtime.open(result))

          result.addCallback(lambda _: runtime.shutdown())

      pre_runtime.addCallback(run)

      # Start the Twisted event loop.
      reactor.run()

if __name__ == "__main__":
    main()
