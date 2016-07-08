#!/bin/bash

INPUT="/ramstorage-ram/data/git/massis3/massis3-assets/makehuman-assets/src/main/makehuman/exports"
OUTPUT="/ramstorage-ram/data/git/massis3/massis3-assets/makehuman-assets/src/main/resources"

rm -rf "/ramstorage-ram/data/git/massis3/massis3-assets/makehuman-assets/src/main/resources/Models"


cd /home/rpax/git/massis3/
mvn clean install
cd /home/rpax/git/massis3/massis3-assets/makehuman-assets
mvn clean install exec:java -Dexec.mainClass="com.massisframework.massis3.assets.makehuman.CompileMHX2" -Dmassis3.inputFolder="$INPUT" -Dmassis3.outputFolder="$OUTPUT"
