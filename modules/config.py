# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from os.path import join, dirname, exists, expanduser
from os import mkdir
from  languages import *
import configparser
import locale

myfile = join(expanduser('~/.gscrabble'), 'gscrabble.cfg')
config = configparser.RawConfigParser()
config.read(myfile)
section = 'settings'

fg_pieces = 'rgb(32,74,135)'
fg_nbr = 'rgb(204,0,0)'
fg_cell = 'rgb(46,52,54)'
bg_pieces = 'rgb(253,253,215)'
bg_no_install = 'rgb(255,245,154)'
bg_last_word =  'rgb(221,245,125)'
sel_pieces = 'rgb(255,108,97)'
br_pieces = 'rgb(204,0,0)'
bg_area = 'rgb(186,189,182)'
bg_grid = 'rgb(242,204,145)'
br_grid = 'rgb(117,80,123)'
bg_lines = 'rgb(136,138,133)'
fg_msg = 'rgb(32,74,135)'
bg_hX2 = 'rgb(201,236,228)'
bg_hX3 = 'rgb(114,159,207)'
bg_kX2 = 'rgb(255,185,185)'
bg_kX3 = 'rgb(251,95,95)'
bg_start = 'rgb(252,233,79)'

def load():
    if not config.has_section(section):
        config.add_section(section)
    if not config.has_option(section, 'language_surface'):
        config.set(section, 'language_surface', '< System >')
    if not config.has_option(section, 'language_scrabble'):
        loc, enc = locale.getdefaultlocale()
        ln = loc[0:2]
        config.set(section, 'language_scrabble', DICT_LANGUAGES_NAME[ln])
    if not config.has_option(section, 'saved'):
        config.set(section, 'saved', 0)
    if not config.has_option(section, 'points_player'):
        config.set(section, 'points_player', 0)
    if not config.has_option(section, 'points_computer'):
        config.set(section, 'points_computer', 0)
    if not config.has_option(section, 'grade'):
        config.set(section, 'grade', 2)
    if not config.has_option(section, 'count_pieces'):
        config.set(section, 'count_pieces', 0)
    if not config.has_option(section, 'point_words'):
        config.set(section, 'point_words', 0)
    if not config.has_option(section, 'autohide_letters'):
        config.set(section, 'autohide_letters', 0)
    if not config.has_option(section, 'autohide_info'):
        config.set(section, 'autohide_info', 0)
    #-----------------------------------------------------
    if not config.has_option(section, 'font_pieces'):
        config.set(section, 'font_pieces', 'Sans 11')
    if not config.has_option(section, 'font_special'):
        config.set(section, 'font_special', 'Sans 15')
    if not config.has_option(section, 'font_msg'):
        config.set(section, 'font_msg', 'Sans 25')
    if not config.has_option(section, 'font_win'):
        config.set(section, 'font_win', 'Sans 15')
    #-----------------------------------------------------
    if not config.has_option(section, 'bg_hX2'):
        config.set(section, 'bg_hX2', bg_hX2)
    if not config.has_option(section, 'bg_hX3'):
        config.set(section, 'bg_hX3', bg_hX3)
    if not config.has_option(section, 'bg_kX2'):
        config.set(section, 'bg_kX2', bg_kX2)
    if not config.has_option(section, 'bg_kX3'):
        config.set(section, 'bg_kX3', bg_kX3)
    if not config.has_option(section, 'bg_start'):
        config.set(section, 'bg_start', bg_start)
    if not config.has_option(section, 'fg_pieces'):
        config.set(section, 'fg_pieces', fg_pieces)
    if not config.has_option(section, 'fg_nbr'):
        config.set(section, 'fg_nbr', fg_nbr)
    if not config.has_option(section, 'fg_cell'):
        config.set(section, 'fg_cell', fg_cell)
    if not config.has_option(section, 'bg_pieces'):
        config.set(section, 'bg_pieces', bg_pieces)
    if not config.has_option(section, 'bg_no_install'):
        config.set(section, 'bg_no_install', bg_no_install)
    if not config.has_option(section, 'bg_last_word'):
        config.set(section, 'bg_last_word', bg_last_word)
    if not config.has_option(section, 'br_pieces'):
        config.set(section, 'br_pieces', br_pieces)
    if not config.has_option(section, 'bg_area'):
        config.set(section, 'bg_area', bg_area)
    if not config.has_option(section, 'bg_grid'):
        config.set(section, 'bg_grid', bg_grid)
    if not config.has_option(section, 'br_grid'):
        config.set(section, 'br_grid', br_grid)
    if not config.has_option(section, 'bg_lines'):
        config.set(section, 'bg_lines', bg_lines)
    if not config.has_option(section, 'fg_msg'):
        config.set(section, 'fg_msg', fg_msg)
    if not config.has_option(section, 'br_thick'):
        config.set(section, 'br_thick', 1)
    #-----------------------------------------------------
    if not config.has_option(section, 'sound'):
        config.set(section, 'sound', 1)
    if not config.has_option(section, 'pipe_drop'):
        config.set(section, 'pipe_drop', 9000)
    if not config.has_option(section, 'pipe_ok'):
        config.set(section, 'pipe_ok', 5000)
    if not config.has_option(section, 'pipe_undo'):
        config.set(section, 'pipe_undo', 1300)
    if not config.has_option(section, 'pipe_add'):
        config.set(section, 'pipe_add', 9000)    
    if not config.has_option(section, 'pipe_drop_ms'):
        config.set(section, 'pipe_drop_ms', 20)
    if not config.has_option(section, 'pipe_ok_ms'):
        config.set(section, 'pipe_ok_ms', 20)
    if not config.has_option(section, 'pipe_undo_ms'):
        config.set(section, 'pipe_undo_ms', 20)
    if not config.has_option(section, 'pipe_add_ms'):
        config.set(section, 'pipe_add_ms', 20)
    with open(myfile, 'w') as configfile:
        config.write(configfile)

def setv(option, value):
    config.set(section, option, value)
    with open(myfile, 'w') as configfile:
        config.write(configfile)
   
def getv(option):
    value = config.get(section, option)
    return value

def getn(option):
    value = config.getint(section, option)
    return value

def getf(option):
    value = config.getfloat(section, option)
    return value
    
mydir = dirname(myfile)
if not exists(mydir):
    try:  mkdir(mydir)
    except: raise

if not exists(myfile):
    try: 
        open(myfile,'w+')
    except: raise
load()
