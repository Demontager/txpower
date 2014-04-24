#!/bin/bash
#Purpose: Automatic txpower increase and/or starting monitor mode
#Author:demontager
#website:nixtalk.com

IFACE=`echo $2`
CH=`echo $3`
POWER=30dbm
MON=`iwconfig 2>/dev/null| awk '/^mon+/ {print $1}'`


check_root() {
if [[ ! $(whoami) = "root" ]]; then
echo "Please run script as root"
exit 1
fi
}

check_iface() {
iwconfig $IFACE 1>/dev/null
local CHECK=`echo $?`
if [[ "$CHECK" != 0 ]] ; then
exit 1
fi
}

msg_usage() {
clear	
echo "Automatic txpower increase on RTL8187 chip aka \"Alfa Awus036\" and/or starting monitor mode "
echo ""
echo "Usage: `basename $0` <power|start|stop|all> <interface> <channel>"
cat <<EOF

Options:
power :set $POWER
start :enable monitor mode and airodump-ng
stop :disable monitor mode
all :set $POWER, enable monitor mode and airodump-ng
channel :set desired channel 1-13 (optional)
EOF

}

power() {
check_root
check_iface
if [ `iwconfig $IFACE|awk '/Access/{print $4}'` = "Not-Associated" ]; then
ifconfig "$IFACE" down
local CHECK=`echo $?`
    if [ $CHECK = 0 ]; then
iw reg set BO
iwconfig $IFACE txpower $POWER
ifconfig $IFACE up
sleep 2
echo "`iwconfig $IFACE| awk '/Tx-Power/{print $5;}'|head -n 2`dbm"
    else
exit 1
    fi
else
echo "Disconnect from WiFi-AP first"
exit 1
fi
}

start() {
check_root
check_iface
if [ -z "$MON" ]; then
airmon-ng start $IFACE $CH 1>/dev/null
      echo `iwconfig 2>/dev/null| awk '/^mon+/ {print $4, $1}'|sed -ne 's/Mode:Monitor/Monitor mode enabled on/p'`
      echo "Starting airodump-ng...."
      sleep 3
     local MONIF=`iwconfig 2>/dev/null| awk '/^mon+/ {print $1}'`
     if [ -n "$CH" ]; then
airodump-ng -c $CH --ignore-negative-one $MONIF
     else
airodump-ng $MONIF
     fi
else
local MONIF=`iwconfig 2>/dev/null| awk '/^mon+/ {print $1}'`
       echo "Monitor mode already enabled on $MON"
       sleep 2
       echo "Starting airodump-ng...."
       sleep 2
      if [ -n "$CH" ]; then
airodump-ng -c $CH --ignore-negative-one $MONIF
     else
airodump-ng $MONIF
     fi
fi
}

stop() {
check_root
check_iface
  if [ -n "$MON" ]; then
for i in $MON
  do
airmon-ng stop $i
  done
else
echo "Monitor mode already stopped"
fi
}

case "$#" in
     2) case "$1" in
                 power)
                 power
                 ;;
                 start)
                 start
                 ;;
                 all)
                  power
                  start
                 ;;
                 stop)
                 stop
                 ;;
                    *)
                 msg_usage
         esac ;;
      3) case "$1" in
                 power)
                 power
                 ;;
                 start)
                 start
                 ;;
                 all)
                  power
                  start
                 ;;
                 stop)
                 stop
                 ;;
                    *)
                 msg_usage
        esac ;;
      *)
      msg_usage
esac
