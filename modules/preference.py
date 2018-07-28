# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from gi.repository import Gtk
from about import About
import config as config
from tools import *
from data import *
from os import listdir
from dialog_preference import DialogPreference

#===============================================================
class Preference(Gtk.Box):
    
    def __init__(self, pt):
        Gtk.Box.__init__(self, spacing=3,orientation=Gtk.Orientation.VERTICAL)
        self.set_border_width(7)
        self.pt = pt
        self.build()
    
    #-----------------------------------------------------------
    def restart_game(self, *a):
        if self.pt.all_letters == 1: self.pt.hd_bar.close_show_letters()
        self.pt.hd_bar.btn_pref.set_active(False)
        if list(self.pt.dict_chequer.values()) == [0,]*225: self.pt.restart_game()
        if self.pt.ended == True: self.pt.restart_game()
        if self.pt.stack.get_visible_child_name() == 'n0':  self.pt.restart_game()
        else:
            res = sure(self.pt, _('If you want to start a new game you will lose the current game. \n Do you want that?'))
            if res == -8:
                self.pt.restart_game()
    
    #-----------------------------------------------------------
    def build(self, *a):
        self.new_game = Gtk.ToolButton()
        self.new_game.set_label(_('New game'))
        self.new_game.connect('clicked', self.restart_game)
        self.pack_start(self.new_game, False, False, 0)
        self.pack_start(Gtk.Separator(), False, False, 3)

        btn_lang = Gtk.ToolButton()
        btn_lang.set_label(_('Preference'))
        self.pack_start(btn_lang, False, False, 0)
        btn_lang.connect('clicked', lambda *a: DialogPreference(self.pt))
        btn_lang.connect('clicked', lambda *a: self.pt.hd_bar.btn_pref.set_active(False))
        
        btn_about = Gtk.ToolButton()
        btn_about.set_label(_('About!'))
        self.pack_start(btn_about, False, False, 0)
        btn_about.connect('clicked', lambda *a: self.pt.hd_bar.btn_pref.set_active(False))
        btn_about.connect('clicked', lambda *a: About(self.pt))
        self.show_all()
        