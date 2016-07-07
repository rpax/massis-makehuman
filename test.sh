#!/bin/bash

INPUT="/ramstorage-ram/data/git/massis3/massis3-assets/makehuman-assets/src/main/makehuman/exports"
OUTPUT="/ramstorage-ram/data/git/massis3/massis3-assets/makehuman-assets/src/main/resources"

rm -rf "/ramstorage-ram/data/git/massis3/massis3-assets/makehuman-assets/src/main/resources/Models"
docker build -t rpax/massis-makehuman2 .
docker run -it -v $INPUT:/input -v $OUTPUT:/output rpax/massis-makehuman2 /bin/run-converter

#mvn clean install
#mvn exec:java -Dexec.mainClass="com.massisframework.massis3.assets.makehuman.CompileMHX2" -Dmassis3.inputFolder="$INPUT" -Dmassis3.outputFolder
