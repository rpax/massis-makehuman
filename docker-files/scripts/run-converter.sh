#!/bin/bash
# dont use hw acc
export LIBGL_ALWAYS_SOFTWARE=1

if [[ "$1" != "" ]]; then
    nThreads="$1"
else
    nThreads=1
fi

rm -rf /output/*
find /input -name "*.mhx2" \
| xargs realpath \
| xargs -n 1 -P "$nThreads" /usr/local/blender/blender-softwaregl --background --python /usr/bin/mixamo_to_blender.py
chmod -R 777 /output/
mvn exec:java -Dexec.mainClass="com.massisframework.makehuman.BlenderConverter" -Dmassis3.workingDir="/output"
