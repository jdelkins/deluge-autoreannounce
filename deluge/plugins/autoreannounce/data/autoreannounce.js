/*
Script: autoreannounce.js
    The client-side javascript code for the AutoReannounce plugin.

Copyright:
    (C) Joel Elkins 2016 <joel@elkins.com>

    This file is part of AutoReannounce and is licensed under GNU General Public License 3.0, or later, with
    the additional special exception to link portions of this program with the OpenSSL library.
    See LICENSE for more details.
*/

AutoReannouncePlugin = Ext.extend(Deluge.Plugin, {
    constructor: function(config) {
        config = Ext.apply({
            name: "AutoReannounce"
        }, config);
        AutoReannouncePlugin.superclass.constructor.call(this, config);
    },

    onDisable: function() {

    },

    onEnable: function() {

    }
});
new AutoReannouncePlugin();
