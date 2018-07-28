# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk, Gdk
from os.path import join, dirname, realpath, expanduser, exists
from os import mkdir
import pickle
import re, sys
import config

if getattr(sys, 'frozen', False):
    APP_DIR = dirname(dirname(sys.executable))
else:
    APP_DIR     = dirname(dirname(realpath(__file__)))
HOME_DIR      = expanduser('~/.gscrabble')
STEMS_HOME = join(HOME_DIR, 'stems')
DICTS_HOME  = join(HOME_DIR, 'dicts')
DATA_DIR      = join(APP_DIR, 'data')
STEMS_DIR    = join(DATA_DIR, 'stems')
DICTS_DIR    = join(DATA_DIR, 'dicts')
LOCALDIR      = join(APP_DIR, 'locale')

if not exists(STEMS_HOME):
    try:  mkdir(STEMS_HOME)
    except: raise
    
if not exists(DICTS_HOME):
    try:  mkdir(DICTS_HOME)
    except: raise

#------------------------------------------

def rgb(value):
    if value.startswith('#'):
        value = value.lstrip('#')
        v = int(len(value)/3)
        R = int(value[0:v], 16)/15.999**v
        G = int(value[v:2*v], 16)/15.999**v
        B = int(value[2*v:3*v], 16)/15.999**v
    elif value.startswith('rgba'):
        value = value.lstrip('rgba')
        v = eval(value)
        R = v[0]/255.0
        G = v[1]/255.0
        B = v[2]/255.0
    else:
        value = value.lstrip('rgb')
        v = eval(value)
        R = v[0]/255.0
        G = v[1]/255.0
        B = v[2]/255.0
    return R, G, B

def rgba(value):
    if value.startswith('#'):
        value = value.lstrip('#')
        v = int(len(value)/3)
        R = int(value[0:v], 16)/15.999**v
        G = int(value[v:2*v], 16)/15.999**v
        B = int(value[2*v:3*v], 16)/15.999**v
    elif value.startswith('rgba'):
        value = value.lstrip('rgba')
        v = eval(value)
        R = v[0]/255.0
        G = v[1]/255.0
        B = v[2]/255.0
    else:
        value = value.lstrip('rgb')
        v = eval(value)
        R = v[0]/255.0
        G = v[1]/255.0
        B = v[2]/255.0
    A = 1.0
    return Gdk.RGBA(R, G, B, A)

#a------------------------------------------
def info(parent, msg):
    dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL,
                            Gtk.MessageType.INFO, Gtk.ButtonsType.CLOSE, msg)
    dlg.set_keep_above(True)
    dlg.run()
    dlg.destroy()

#a------------------------------------------
def sure(parent, msg):
    dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL, Gtk.MessageType.WARNING,
                             Gtk.ButtonsType.YES_NO)
    dlg.set_markup(msg)
    dlg.set_keep_above(True)
    r = dlg.run()
    dlg.destroy()
    return r

#a---------------------------------------------------
def split_font(font):
    ls = font.split(' ')
    szfont = ls.pop(-1)
    fmfont = ' '.join(ls)
    return szfont, fmfont
#a---------------------------------------------------
def pipeline_stop(pipeline, gst):
    pipeline.set_state(gst.State.NULL)
    return False

def play_sound(name):
    frequency = config.getf('pipe_{}'.format(name,))
    ms = config.getf('pipe_{}_ms'.format(name,))
    if config.getn('sound') == 1: 
        from gi.repository import Gst, GObject
        Gst.init(None)
        pipeline = Gst.Pipeline(name='note')
        source = Gst.ElementFactory.make('audiotestsrc', 'src')
        sink = Gst.ElementFactory.make('autoaudiosink', 'output')
        source.set_property('freq', frequency)
        pipeline.add(source)
        pipeline.add(sink)
        source.link(sink)
        pipeline.set_state(Gst.State.PLAYING)
        GObject.timeout_add(ms, pipeline_stop, pipeline, Gst)

#a---------------------------------------------------
def save_game(dict_all, w_p_text, list_repeated, ls_7_p, ls_7_c, p_player, p_computer, cells_empty, c_empty_letter):
    output = open(join(HOME_DIR, 'saved.pkl'), 'wb')
    pickle.dump([dict_all, w_p_text, list_repeated, ls_7_p, ls_7_c, p_player, p_computer, cells_empty, c_empty_letter], output)
    output.close()

#a---------------------------------------------------
def load_game_scrabble():
    list_saved = pickle.load(open(join(HOME_DIR, 'saved.pkl'), 'rb'))
    return list_saved

#a----------------------------------------------------        
TASHKEEL_pattern =re.compile(r"[\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652]")  
def stripTashkeel(text):
    return re.sub(TASHKEEL_pattern,'',text);

#a 0 خانة البداية
#a 1 الأحرف المضاعفة 
#a 2 الأحرف المثلثة
#a 3 الكلمات المضاعفة
#a 4 الكلمات المثلثة

DICT_SPECIAL_CELLS = {
    0: 4, 128: 1, 3: 1, 7: 4, 136: 2, 11: 1, 140: 2,
    14: 4, 16: 3, 188: 1, 20: 2, 165: 1, 217: 4, 24: 2,
    132: 1, 154: 3, 28: 3, 208: 3, 32: 3, 176: 3, 36: 1,
    38: 1, 168: 3, 221: 1, 42: 3, 172: 1, 48: 3, 52: 1,
    182: 3, 56: 3, 186: 1, 45: 1, 192: 3, 64: 3, 160: 3,
    196: 3, 70: 3, 200: 2, 204: 2, 59: 1, 76: 2, 224: 4,
    80: 2, 210: 4, 84: 2, 213: 1, 88: 2, 179: 1, 92: 1,
    96: 1, 144: 2, 98: 1, 102: 1, 105: 4, 108: 1, 112: 0,
    116: 1, 119: 4, 148: 2, 122: 1, 126: 1}
