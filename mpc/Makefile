# MPCR Makefile for generating config data

all: clean config p3

config:
	python ~/viff/apps/generate-config-files.py localhost:4001 localhost:4002 localhost:4003
	python ~/viff/apps/generate-certificates.py	

p3:
	python point_in_poly.py player-3.ini --file player-3.json
p2:
	python point_in_poly.py player-2.ini --file player-2.json
p1:
	python point_in_poly.py player-1.ini --file player-1.json


clean:
	-rm *.ini *.key *.cert

