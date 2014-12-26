templog
=======

raspberry pi temperature log


crontab:
--------

crontab -l
HOME=/home/pi

# m h  dom mon dow   command
  * *    *   *   *   $HOME/dev/templog/bin/run_uptime.sh >> $HOME/.uptime.xenon.log 2>&1
  * *    *   *   *   $HOME/dev/templog/bin/run_temperature.sh >> $HOME/.temperature.xenon.log 2>&1
