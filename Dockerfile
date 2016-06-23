FROM ikester/blender:2.76b

# ------------------------------------------------------------------------------
# disable interactive functions
ENV DEBIAN_FRONTEND noninteractive

ENV ADDONS_FOLDER /usr/local/blender/$BLENDER_MAJOR/scripts/addons

RUN apt-get update
RUN apt-get -y install zip unzip

# Addons & Tools
RUN mkdir -p "$ADDONS_FOLDER"
RUN curl --remote-name https://bitbucket.org/rpax/mhx2-makehuman-exchange/get/tip.zip
RUN unzip tip.zip
RUN rm tip.zip
RUN mv rpax-mhx2-makehuman-exchange-5971f82e50f3/import_runtime_mhx2 "$ADDONS_FOLDER/import_runtime_mhx2"
RUN rm -rf rpax-mhx2-makehuman-exchange-5971f82e50f3

# makehuman blender tools
RUN curl --remote-name http://download.tuxfamily.org/makehuman/releases/1.1.0/blendertools-1.1.0-all.zip
RUN unzip blendertools-1.1.0-all.zip
RUN rm blendertools-1.1.0-all.zip
RUN mv blendertools/makeclothes "$ADDONS_FOLDER/makeclothes"
RUN mv blendertools/maketarget "$ADDONS_FOLDER/maketarget"
RUN mv blendertools/makewalk "$ADDONS_FOLDER/makewalk"
RUN rm -rf blendertools


COPY docker-files/mixamo_to_blender.py /usr/bin/mixamo_to_blender.py
RUN chmod +x /usr/bin/mixamo_to_blender.py

COPY docker-files/run-converter.sh /usr/bin/run-converter
RUN chmod +x /usr/bin/run-converter

VOLUME /media
ENTRYPOINT ["/bin/bash"]
