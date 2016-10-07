#
# -*- coding: utf-8 -*-#

# Copyright (C) 2016 Joel Elkins <joel@elkins.com>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
# Copyright (C) 2010 Pedro Algarvio <pedro@algarvio.me>
#
# This file is part of AutoReannounce and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#

import logging
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export

import re

from twisted.internet import reactor
from twisted.internet.task import LoopingCall, deferLater

DEFAULT_PREFS = {
    'enabled': True,
    'interval': 10,
    'tracker_status_filter_re': '.*unregistered',
}

log = logging.getLogger(__name__)


class Core(CorePluginBase):
    def enable(self):
        log.debug('AutoReannounce: Enabled')
        self.config = deluge.configmanager.ConfigManager("autoreannounce.conf", DEFAULT_PREFS)
        self.config.save()
        self.looping_call = LoopingCall(self.do_error_check)
        deferLater(reactor, 10, self.start_looping)

    def disable(self):
        if self.looping_call.running:
            self.looping_call.stop()	

    def update(self):
        pass

    def start_looping(self):
        log.warning('AutoReannounce: check interval loop starting: {} secs'.format(self.config['interval']))
        self.looping_call.start(self.config['interval'])

    @export
    def set_config(self, config):
        """Sets the config dictionary"""
        for key in config.keys():
            self.config[key] = config[key]
        self.config.save()
        if self.looping_call.running:
    	    self.looping_call.stop()
        self.looping_call.start(self.config['interval'])

    @export
    def get_config(self):
        """Returns the config dictionary"""
        return self.config.config

    def do_error_check(self, *args, **kwargs):
        log.debug('AutoReannounce: do_error_check')

        torrentmanager = component.get('TorrentManager')
        torrent_ids = torrentmanager.get_torrent_list()
        log.debug('AutoReannounce: checking {} torrents'.format(len(torrent_ids)))

        try:
            pat = re.compile(self.config['tracker_status_filter_re'])
            for i in torrent_ids:
                t = torrentmanager.torrents.get(i, None)
                s = t.get_status(['name', 'tracker_status', 'state'])
                if s['state'] == 'Downloading':
                    log.debug('AutoReannounce: inspecting {} name: "{}" state "{}" tracker_status "{}"'.format(i, s['name'], s['state'], s['tracker_status']))
                    if pat.match(s['tracker_status']):
                        log.info('AutoReannounce: Torrent id {} a/k/a {}: tracker_status "{}" matches filter "{}". Forcing a reannounce.'.format(i, s['name'], s['tracker_status'], self.config['tracker_status_filter_re']))
                        t.force_reannounce()
        except Exception as e:
            log.warning('AutoReannounce: An error happened in do_error_check: {}'.format(e))
