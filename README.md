txpower.sh
=======

Overview
========
Automatic txpower increase on RTL8187 chip aka "Alfa Awus036" and/or starting monitor mode
Txpower solving the problem on Alfa Awus036 when it has no full power output e.g. 30 dbm. It's power limited to 15-17 dbm by default. Core problem that some countries regulations do not allow setting high wifi power output and few of them allow. So txpower get this advantage at set proper coutry where high power allowed.
Also script has option to put wifi card into monitor mode after increasing power. Another option is to monitor defined channel (above two options useful for wifi pentesting)

**Usage:**
1. Download script and make it executable chmod +x txpower.sh
2. Run it without arguments to see the list of available options

power    :set $POWER
start    :enable monitor mode and airodump-ng
stop     :disable monitor mode
all      :set $POWER, enable monitor mode and airodump-ng
channel  :set desired channel 1-13 (optional)

*Optional*
3. Set required power limit in script body.
