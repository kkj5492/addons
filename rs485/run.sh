#!/bin/sh

SHARE_DIR=/share

if [ ! -f $SHARE_DIR/rs485.py ]; then
	mkdir $SHARE_DIR
	mv /rs485.py $SHARE_DIR
fi
/makeconf.sh

echo "[Info] RS485 To MQTT Controller"
cd $SHARE_DIR
python3 $SHARE_DIR/rs485.py

