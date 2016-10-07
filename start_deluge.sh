#!/bin/bash

deluged -c /config -P /config/deluged.pid -l /config/deluged.log -p 22222
deluge-web -c /config -l /config/deluge-web.log -f --no-ssl
