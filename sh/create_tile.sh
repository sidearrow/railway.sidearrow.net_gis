#!/bin/bash

rm -rf ./data/tiles/line

tippecanoe \
  --no-tile-compression \
  --minimum-zoom 7 \
  --maximum-zoom 14 \
  --output-to-directory ./data/tiles/line \
  ./data/geojson/line.geojson
