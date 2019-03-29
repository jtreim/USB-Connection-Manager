#!/bin/bash

if [ "${ACTION}" = "add" ]
then
    echo "Don't turn off." >> /var/log/usbtrigger.log
    # source /home/girrowfe/code-proj/cs456/cs456env/bin/activate
    # python /home/girrowfe/code-proj/cs456/Auto-Steam-Streamer/app.py >> /var/log/usbtrigger.log & exit
fi
