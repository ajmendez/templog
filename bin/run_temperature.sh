#!/bin/bash
# gets some temperature data.

echo "$(date +%s) | $(date) | $(cat /sys/class/thermal/thermal_zone0/temp) | $(/opt/vc/bin/vcgencmd measure_temp)"
