#!/bin/bash
# dont use hw acc
export LIBGL_ALWAYS_SOFTWARE=1
rm -rf /output/*
/usr/local/blender/blender-softwaregl --background --python /usr/bin/mixamo_to_blender.py
chmod -R 777 /output/
rm -rf /output/*.blend1
mvn exec:java -Dexec.mainClass="com.massisframework.makehuman.BlenderConverter" -Dmassis3.workingDir="/output"
