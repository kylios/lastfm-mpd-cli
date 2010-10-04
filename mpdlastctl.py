#!/usr/bin/python

import baker
import pylast
import os.path
import sys
import socket
import subprocess

API_KEY = "ea5e9fdda870bb07563f2413ae445619"
API_SECRET = "72256346b12bfd976452670ef2b39071"
API_ROOT_URL = "http://ws.audioscrobbler.com/2.0/"

LOCAL_CONFIG_PATH = "~/.mpdlastctl/mpdlastctl.rc"
GLOBAL_CONFIG_PATH = "/etc/mpdlastctl.rc"


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
    #print("api_key: " + API_KEY)
    #print("api_secret: " + API_SECRET)
    #print("username: " + lastfm_username)
    #print("password_hash: " + lastfm_password)
    conn = pylast.get_lastfm_network(api_key = API_KEY, api_secret = API_SECRET, username = lastfm_username, password_hash = pylast.md5(lastfm_password))
    return conn

def lastfm_get_track(conn, (artist, trackname)):
    return conn.get_track(artist, trackname)

def lastfm_love_track(track):
    track.love()

def read_config(fd):
    line = fd.readline()
    while line != '':
        print line
        line = fd.readline()
    return (None, None, None, None, 'localhost', 6600)

""" Loads the configuration file"""
def load_config():
    lastfm_username = None
    lastfm_password = None
    mpd_username = None
    mpd_password = None
    mpd_hostname = 'localhost'
    mpd_port = 6600

    try:
        fd = open(GLOBAL_CONFIG_PATH, 'r')
        print "reading " + GLOBAL_CONFIG_PATH
        lastfm_username, lastfm_password, mpd_password, mpd_hostname, mpd_port = read_config(fd)
        close(fd)
    except IOError as (errno, strerror):
        pass
    try:
        fd = open(LOCAL_CONFIG_PATH, 'r')
        print "reading " + LOCAL_CONFIG_PATH
        lastfm_username, lastfm_password, mpd_password, mpd_hostname, mpd_port = read_config(fd)
        close(fd)
    except IOError as (errno, strerror):
        pass

    return (None, None, None, None, 'localhost', 6600)

""" Checks for errors in any of our data """
def check_errors(lastfm_username, lastfm_password, mpd_username, mpd_password, mpd_hostname, mpd_port):

    if not lastfm_username:
        error("Must supply a last.fm username")
    if not lastfm_password:
        error("Must supply a last.fm password")
    #if len(lastfm_password) != 32:
    #    error("Last.fm password MUST be md5 hash")

@baker.command
def love(lastfmusername = None, lastfmpassword = None, mpdusername = None,
        mpdpassword = None, mpdport = None, mpdhostname = None):
    """Loves the currently playing mpd track.

    :param lastfmusername: The username you use to log into last.fm.
    :param lastfmpassword: The md5 hash of the password you use to log into last.fm.
    :param mpdusername: The mpd user.
    :param mpdpassword: The mpd password.
    :param mpdport: The mpd port.
    :param mpdhost: The mpd host.
    """
    lastfm_username = None
    lastfm_password = None
    mpd_username = None
    mpd_password = None
    mpd_hostname = 'localhost'
    mpd_port = 6600

    lastfm_username, lastfm_password, mpd_username, mpd_password, mpd_hostname, mpd_port = load_config()

    if lastfmusername:
        lastfm_username = lastfmusername
    if lastfmpassword != None:
        lastfm_password = lastfmpassword
    if mpdusername and mpdusername != mpd_username:
        mpd_username = mpdusername
    if mpdpassword and mpdpassword != mpd_password:
        mpd_password = mpdpassword
    if mpdport and int(mpdport) != mpd_port:
        mpd_port = int(mpdport)
    if mpdhostname and mpdhostname != mpd_hostname:
        mpd_hostname = mpdhostname

    check_errors(lastfm_username, lastfm_password, mpd_username, mpd_password, mpd_hostname, mpd_port)
    lastfmconn = lastfm_connect(lastfm_username, lastfm_password)
    if lastfmconn == None:
        error("Could not connect to last.fm")

    track = mpd_get_current()
    if track == None:
        error("Could not get track data from mpd")
    print track
    lastfm_track = lastfm_get_track(lastfmconn, track)
    lastfm_track.love()

baker.run()

