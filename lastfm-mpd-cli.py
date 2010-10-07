#!/usr/bin/python

"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

#Author: Kyle Racette (kracette@gmail.com)

import baker
import pylast
import os.path
import sys
import socket
import subprocess
import string

API_KEY = "ea5e9fdda870bb07563f2413ae445619"
API_SECRET = "72256346b12bfd976452670ef2b39071"
API_ROOT_URL = "http://ws.audioscrobbler.com/2.0/"

HOME = os.environ['HOME']
LOCAL_CONFIG_PATH = os.path.join(HOME, ".lastfm-mpd-cli.rc")
GLOBAL_CONFIG_PATH = os.path.join("/etc", "lastfm-mpd-cli.rc")

""" Throws an error message to stdout """
def error(msg):
    print msg
    exit(1)

""" Get the currently playing track from mpd.  
    Returns (ARTIST, TRACKNAME) """
def mpd_get_current():
    mpc = subprocess.Popen(["mpc", "current"], shell=False, stdout=subprocess.PIPE)
    mpc.wait()
    result = mpc.communicate()
    track = result[0]
    track = track.split('-')
    artist = track[0].strip()
    name = track[1].strip()
    return (artist, name)

def lastfm_connect(lastfm_username, lastfm_password):
    conn = pylast.get_lastfm_network(api_key = API_KEY, api_secret = API_SECRET, username = lastfm_username, password_hash = lastfm_password)
    return conn

def lastfm_get_track(conn, (artist, trackname)):
    return conn.get_track(artist, trackname)

def lastfm_love_track(track):
    track.love()

def read_config(fd):
    lastfmusername = None
    lastfmpassword = None
    mpdpassword = None
    mpdhostname = None
    mpdport = None

    line = fd.readline()
    while line != '':
        if not lastfmusername and 0 == string.find(line, 'lastfmusername'):
            lastfmusername = line
        elif not lastfmpassword and 0 == string.find(line, 'lastfmpassword'):
            lastfmpassword = line
        elif not mpdpassword and 0 == string.find(line, 'mpdpassword'):
            mpdpassword = line
        elif not mpdhostname and 0 == string.find(line, 'mpdhostname'):
            mpdhostname = line
        elif not mpdport and 0 == string.find(line, 'mpdport'):
            mpdport = line
        line = fd.readline()

    if lastfmusername: lastfmusername = lastfmusername.split('=')[1].strip()
    if lastfmpassword: lastfmpassword = lastfmpassword.split('=')[1].strip()
    if mpdpassword: mpdpassword = mpdpassword.split('=')[1].strip()
    if mpdhostname: mpdhostname = mpdhostname.split('=')[1].strip()
    if mpdport: mpdport = int(mpdport.split('=')[1].strip())
    
    return (lastfmusername, lastfmpassword, mpdpassword, mpdhostname, mpdport)

""" Loads the configuration file"""
def load_config():
    lastfmusername = None
    lastfmpassword = None
    mpdpassword = None
    mpdhostname = 'localhost'
    mpdport = 6600

    # Local overwrites global
    try:
        fd = open(LOCAL_CONFIG_PATH, 'r')
        lastfmusername, lastfmpassword, mpdpassword, mpdhostname, mpdport = read_config(fd)
        fd.close()
    except IOError as (errno, strerror):

        try:
            fd = open(GLOBAL_CONFIG_PATH, 'r')
            lastfmusername, lastfmpassword, mpdpassword, mpdhostname, mpdport = read_config(fd)
            fd.close()
        except IOError as (errno, strerror):
            pass

    return (lastfmusername, lastfmpassword, mpdpassword, mpdhostname, mpdport)

""" Checks for errors in any of our data """
def check_errors(lastfm_username, lastfm_password, mpd_password, mpd_hostname, mpd_port):

    if not lastfm_username:
        error("Must supply a last.fm username")
    if not lastfm_password:
        error("Must supply a last.fm password")
    if len(lastfm_password) != 32:
        error("Last.fm password MUST be md5 hash")

@baker.command
def md5(password):
    "Takes the md5sum of the supplied password"
    print pylast.md5(password)

@baker.command()
def love(lastfmusername = None, lastfmpassword = None, mpdpassword = None, 
        mpdport = None, mpdhostname = None):
    """Loves the currently playing mpd track. \n
     lastfmusername: The username you use to log into last.fm. \n
     lastfmpassword: The md5 hash of the password you use to log into last.fm.\n
     mpdpassword: The mpd password.\n
     mpdport: The mpd port.\n
     mpdhost: The mpd host."""
    lastfm_username = None
    lastfm_password = None
    mpd_password = None
    mpd_hostname = 'localhost'
    mpd_port = 6600

    (lastfm_username, lastfm_password, mpd_password, mpd_hostname, mpd_port) = load_config()

    if lastfmusername:
        lastfm_username = lastfmusername
    if lastfmpassword != None:
        lastfm_password = lastfmpassword
    if mpdpassword and mpdpassword != mpd_password:
        mpd_password = mpdpassword
    if mpdport and int(mpdport) != mpd_port:
        mpd_port = int(mpdport)
    if mpdhostname and mpdhostname != mpd_hostname:
        mpd_hostname = mpdhostname

    check_errors(lastfm_username, lastfm_password, mpd_password, mpd_hostname, mpd_port)
    lastfmconn = lastfm_connect(lastfm_username, lastfm_password)
    if lastfmconn == None:
        error("Could not connect to last.fm")

    track = mpd_get_current()
    if track == None:
        error("Could not get track data from mpd")
    lastfm_track = lastfm_get_track(lastfmconn, track)
    lastfm_track.love()

baker.run()

