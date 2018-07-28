# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from word_viewer import Viewer
from tools import *
from data import *


#===============================================================
class SideInfo(Gtk.Box): 
    
    def __init__(self, pt):
        self.pt= pt
        self.build()
    
    def sel_show_points(self, w):
        if w.get_active():
            config.setv('point_words', 1)
            self.wordviewer_buf.set_text(self.pt.text_words_with_points)
        else:
            config.setv('point_words', 0)
            self.wordviewer_buf.set_text(re.sub('=\d*', '', self.pt.text_words_with_points))
        self.wordviewer.with_tag(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '='])
    
    def word_and_inversion(self, word):
        text = word
        ls = list(text)
        ls.reverse()
        word2 = ''.join(ls)
        if word2 in self.pt.dict_chequer.stems_text_set:
            if word != word2: text += ','+word2
        return text
        
    def add_words(self, list_words, n):   
        words = ''
        for t in list_words[1]:
            word = get_word_complex_letters(self.pt.lang_code, t[0])
            ws = self.word_and_inversion(word)
            ww =ws+'='+str(t[1])
            words += ww+'  '
        self.pt.text_words_with_points += words
        if config.getn('point_words') == 0: self.wordviewer_buf.set_text(re.sub('=\d*', '', self.pt.text_words_with_points))
        else: self.wordviewer_buf.set_text(self.pt.text_words_with_points)
        self.wordviewer.with_tag(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '='])
        if n == 1:
            self.pt.points_player += list_words[0]
            config.setv('points_player', self.pt.points_player)
            self.lab_points_player.set_label(str(self.pt.points_player))
        else:
            self.pt.points_computer += list_words[0]
            config.setv('points_computer', self.pt.points_computer)
            self.lab_points_computer.set_label(str(self.pt.points_computer))
    
    def change_combo_count_pieces(self, *a):
        n = self.combo_count_pieces.get_active()
        config.setv('count_pieces', n)
        self.sel_count_pieces(n)
    
    def sel_count_pieces(self, n):
        all_p = str(self.pt.count_pieces).zfill(3)
        last_p = str(len(self.pt.list_letters_repeated)).zfill(3)
        use_p = str(self.pt.count_pieces-len(self.pt.list_letters_repeated)-len(self.pt.list_07_letters_computer)-len(self.pt.list_07_letters_player)).zfill(3)
        plyr_p = str(len(self.pt.list_07_letters_player)).zfill(3)
        cmp_p = str(len(self.pt.list_07_letters_computer)).zfill(3)
        if n == 0: self.label_count_pieces.set_label(all_p)
        elif n == 1: self.label_count_pieces.set_label(last_p)
        elif n == 2: self.label_count_pieces.set_label(use_p)
        elif n == 3: self.label_count_pieces.set_label(cmp_p)
        elif n == 4: self.label_count_pieces.set_label(plyr_p)
        
    def build(self, *a):
        Gtk.Box.__init__(self, spacing=3,orientation=Gtk.Orientation.VERTICAL)
        self.set_border_width(5)
        self.set_size_request(200, -1)
        #----------------------------------------------------------------------------------
        hb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label(_('Difficulty:')), False, False, 3)
        self.label_grade = Gtk.Label()
        self.label_grade.set_label(self.pt.LIST_GRADE[config.getn('grade')])
        hb.pack_start(self.label_grade, False, False, 0)
        self.pack_start(hb, False, False, 0)
        #----------------------------------------------------------------------------------
        hb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label(_('Language:')), False, False, 3)
        self.label_language_scrabble = Gtk.Label()
        self.label_language_scrabble.set_label(config.getv('language_scrabble'))
        hb.pack_start(self.label_language_scrabble, False, False, 0)
        self.pack_start(hb, False, False, 0)
        #----------------------------------------------------------------------------------
        self.pack_start(Gtk.Separator(), False, False, 5)
        #----------------------------------------------------------------------------------
        hb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        self.combo_count_pieces = Gtk.ComboBoxText()
        self.combo_count_pieces.set_size_request(150, -1)
        for t in [_('All pieces'), _('Remaining pieces'), _('Used pieces'), _('Computer pieces'), _('Player pieces')]:
            self.combo_count_pieces.append_text(t)
        hb.pack_start(self.combo_count_pieces, False, False, 0)
        hb.pack_start(Gtk.Label(' : '), False, False, 0)
        self.label_count_pieces = Gtk.Label()
        hb.pack_start(self.label_count_pieces, False, False, 0)
        self.combo_count_pieces.connect('changed', self.change_combo_count_pieces)
        self.combo_count_pieces.set_active(config.getn('count_pieces'))
        self.pack_start(hb, False, False, 0)
        #----------------------------------------------------------------------------------
        self.pack_start(Gtk.Separator(), False, False, 5)
        #----------------------------------------------------------------------------------
        hb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label(_('Player Points:')), False, False, 3)
        self.lab_points_player = Gtk.Label('00')
        hb.pack_start(self.lab_points_player, False, False, 0)
        self.pack_start(hb, False, False, 0)
        #----------------------------------------------------------------------------------
        hb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label(_('Computer Points:')), False, False, 3)
        self.lab_points_computer = Gtk.Label('00')
        hb.pack_start(self.lab_points_computer, False, False, 0)
        self.pack_start(hb, False, False, 0)
        #----------------------------------------------------------------------------------
        self.pack_start(Gtk.Separator(), False, False, 7)
        #----------------------------------------------------------------------------------
        hb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label(_('Installed words:')), False, False, 0)
        self.check_show_points = Gtk.CheckButton()
        self.check_show_points.set_active(config.getn('point_words'))
        self.check_show_points.set_tooltip_text(_('Show word values.'))
        self.check_show_points.connect('toggled', self.sel_show_points)
        hb.pack_end(self.check_show_points, False, False, 0)
        self.pack_start(hb, False, False, 0)
        self.wordviewer = Viewer(self.pt)
        self.wordviewer_buf = self.wordviewer.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.wordviewer)
        self.pack_start(scroll, True, True, 0)
        
        