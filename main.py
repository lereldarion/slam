#!/usr/bin/env python2
'''
Daemon to manage multi monitors

Wanted features:
* Automatically use monitor on connection
    * First : basic system, just put it on right or left in default mode
    * After : Use EDID to match configs
        * First plug in : add it on right or left, then save config based on current state
        * After : select a config according to set of EDID in the system
    * Config : output tree, primary + right/up/left/bottom, alignement to parent monitor
* Manual adjustement dbus calls
    * For now guess from current config
* Backlight management
    * Manage backlight values (scaling log/lin, ...) of every monitor with backlight (> config)
    * Dbus calls to increase/decrease backlight
    * Dbus calls to set again hardware values to soft ones (and call that from ACPI handler after lid button or power cord change, because this is sometimes messed up)
* Background image management based on config

* Config: set_of_edid + set_of_flags (train, work, ...)
'''

import sys, os, select

import xclient, config

# Commands
class StdinCmd (object):
    """ Very simple command line testing tool """
    def __init__ (self, xclient):
        self.xclient = xclient
    def fileno (self): return sys.stdin.fileno ()
    def activate (self):
        """ Pick one line a time, and check for keywords """
        line = sys.stdin.readline ()
        if "info" in line: self.xclient.state_info ()
        if "test" in line: self.xclient.move_down ()
        if "exit" in line: return False
        return True

# Main event loop
def event_loop (object_list):
    """
    Use select to wait for objects representing FD ressources.
    Requires for each object:
        int fileno () method
        bool activate () method : returning False stops the loop
    """
    while True:
        activated, _, _ = select.select (object_list, [], [])
        for obj in activated:
            if not obj.activate (): return

# Entry point
if __name__ == "__main__":
    config_manager = config.ConfigManager ()
    x_client = xclient.Client ()
    cmd = StdinCmd (x_client)
    try:
        event_loop ([x_client, cmd])
    finally:
        x_client.cleanup ()
    sys.exit (0)
