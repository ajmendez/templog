#!/bin/bash
# gets some temperature data.

if [ -e "/usr/local/bin/osx-cpu-temp" ]; then
    echo "$(date +%s) | $(date) | $(/usr/local/bin/osx-cpu-temp)"
else
    echo "$(date +%s) | $(date) | $(cat /sys/class/thermal/thermal_zone0/temp) | $(/opt/vc/bin/vcgencmd measure_temp)"
fi
