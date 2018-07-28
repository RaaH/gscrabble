# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository.GdkPixbuf import Pixbuf
import config as config
from tools import *
from data import *
from create_png import get_letter_png
import time

#===============================================================
class SideLetters(Gtk.IconView): 

    def __init__(self, pt):
        self.pt = pt
        self.build()
    
    def undo_added_all(self, *a):
        if len(self.pt.dict_new) == 0: return
        for cell in self.pt.dict_new.keys():
            letter = self.pt.dict_new[cell]
            if cell in self.pt.cells_empty_letter:
                letter = '*'
                self.pt.cells_empty_letter.remove(cell)
            png_file = get_letter_png(self.pt.lang_code, letter)
            pixbuf = Pixbuf.new_from_file_at_size(png_file, 70, 70)
            self.liststore_letters_player.append([pixbuf, repr(letter)])
            self.pt.chequer.queue_draw()
        self.pt.dict_new.clear()
        play_sound('undo')
    
    def undo_added(self, cell):
        play_sound('undo')
        letter = self.pt.dict_new[cell]
        if cell in self.pt.cells_empty_letter:
            letter = '*'
            self.pt.cells_empty_letter.remove(cell)
        png_file = get_letter_png(self.pt.lang_code, letter)
        pixbuf = Pixbuf.new_from_file_at_size(png_file, 70, 70)
        self.liststore_letters_player.append([pixbuf, repr(letter)])
        del self.pt.dict_new[cell]
    
    def add_letters(self, ls):
        for i in ls:
            png_file = get_letter_png(self.pt.lang_code, i)
            pixbuf = Pixbuf.new_from_file_at_size(png_file, 70, 70)
            play_sound('add')
            time.sleep(0.1)
            while (Gtk.events_pending()): Gtk.main_iteration()
            self.liststore_letters_player.append([pixbuf, repr(i)])
    
    def change_theme(self, *a):
        data = '''
        * {
        background-color: '''+config.getv('bg_grid')+''';
        }
        * text selection, *:selected  {
        background-color: '''+config.getv('bg_lines')+''';
        }
        '''
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(data.encode('utf8'))
        context = self.get_style_context()
        context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    
    def build(self, *a):
        Gtk.IconView.__init__(self)
        self.set_size_request(95, -1)
        self.liststore_letters_player = Gtk.ListStore(Pixbuf, str)
        self.set_model(self.liststore_letters_player)
        self.set_pixbuf_column(0)
        self.set_row_spacing(0)
        self.set_column_spacing(0)
        self.set_item_width(70)
        self.change_theme()
        
        