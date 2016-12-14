# MPCR Makefile for generating config data

all: clean config p3

config:
	python ~/viff/apps/generate-config-files.py localhost:4001 localhost:4002 localhost:4003
	python ~/viff/apps/generate-certificates.py	

p3:
	python sum_matrix.py player-3.ini --file ../static/data/test1/trip-matrix.json
p2:
	python sum_matrix.py player-2.ini --file ../static/data/test2/trip-matrix.json
p1:
	python sum_matrix.py player-1.ini --file ../static/data/test3/trip-matrix.json


clean:
	-rm *.ini *.key *.cert

