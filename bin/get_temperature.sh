#!/bin/bash


# rsync -ravpP pi:.temperature.neon.log  ~/.temperature.neon.log

rsync -ravpP xenon:.temperature.xenon.log  ~/
