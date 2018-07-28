# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from create_png import get_letter_png
import config as config
from tools import *
from data import *
from create_dict import create_db_language

import random

#===============================================================
class PageStarting(Gtk.Box): 
    
    def __init__(self, pt):
        self.pt = pt
        self.build()
    
    def restor_to_starting_page(self, *a):
        self.lab_bar.set_label(_('Former letter will start playing.'))
        self.info_bar.set_message_type(0)
        self.btn_start.set_sensitive(False)
        self.btn_chose1.set_sensitive(True)
        self.image1.clear()
        self.image2.clear()
    
    def start_new_game(self, *a):
        self.pt.stack.set_visible_child_name('n1')
        self.pt.hd_bar.show_hide_action_buttons()
        self.pt.start_new_game()
        self.restor_to_starting_page()
    
    def create_db_language_progress_window(self, lang_code):
        try: win = Gtk.Window(Gtk.WindowType.POPUP)
        except: 
            win = Gtk.Window()
            win.set_title("مرحبا !")
        win.set_position(Gtk.WindowPosition.CENTER)
        win.set_modal(True)
        win.set_border_width(35)
        win.set_size_request(400,200)
        vb = Gtk.Box(spacing=3, orientation=Gtk.Orientation.VERTICAL)
        lab = Gtk.Label(_('Set up language files...'))
        vb.pack_start(lab, True, True, 0)
        progressbar = Gtk.ProgressBar()
        vb.pack_start(progressbar, False, False, 0)
        win.add(vb)
        win.show_all()
        while (Gtk.events_pending()): Gtk.main_iteration()
        create_db_language(progressbar, lang_code)
        win.destroy()
        self.pt.select_all_type_lists_language()
    
    def chose_tile(self, *a):
        lang = config.getv('language_scrabble')
        lang_code = DICT_LANGUAGES_CODE[lang]
        if lang in self.pt.list_language_no_ready_without_stems:
            info(self.pt, _('This language not found'))
            return
        if lang in self.pt.list_language_no_ready_with_stems:
            res = sure(self.pt, _('Files for this language are not ready.\n Do you want that?'))
            if res == -8:
                self.create_db_language_progress_window(lang_code)
            return
        self.pt.load_language_game()
        list_letters = list(DICT_LETTERS[lang_code].keys())
        #==================
        letter1 = random.choice(list_letters)
        list_letters.remove(letter1)
        png_file = get_letter_png(self.pt.lang_code, letter1)
        self.image1.set_from_file(png_file)
        #==================
        letter2 = random.choice(list_letters)
        png_file = get_letter_png(self.pt.lang_code, letter2)
        self.image2.set_from_file(png_file)
        #==================
        self.btn_chose1.set_sensitive(False)
        ls = [letter1, letter2]
        ls.sort()
        if ls[0] == letter1: 
            self.lab_bar.set_label(_('<b>Player will start playing.</b>'))
            self.pt.started_player = 'player'
        else: 
            self.lab_bar.set_label(_('<b>Computer will start playing.</b>'))
            self.pt.started_player = 'computer'
        self.info_bar.set_message_type(1)
        self.lab_bar.set_alignment(0.5, 0.5)
        self.btn_start.set_sensitive(True)
        self.show_all()
    
    def show_all_letters(self, *a):
        i  = LANGUAGES_SCRABBLE.index(DICT_LANGUAGES_NAME[self.pt.lang_code])
        self.pt.hd_bar.combo_language_preview.set_active(i)
        self.pt.all_letters = 1
        self.pt.stack.set_visible_child_name('n1')
        self.pt.sideinfo.hide()
        self.pt.vb_letters.hide()
        self.pt.hd_bar.show_hide_action_buttons()
        self.pt.hd_bar.sel_language_preview()
    
    def build(self, *a):
        Gtk.Box.__init__(self, spacing=20,orientation=Gtk.Orientation.VERTICAL)
        self.info_bar = Gtk.InfoBar(show_close_button=False)
        self.lab_bar = Gtk.Label(_('Former letter will start playing.'))
        self.lab_bar.set_use_markup(True)
        self.info_bar.get_content_area().pack_start(self.lab_bar, True, False, 0)
        self.pack_start(self.info_bar, False, False, 0)
        #----------------------------------------------------------------------------------
        hb0 = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        frame = Gtk.Frame.new()
        vb.set_border_width(25)
        frame.add(vb)
        hb0.pack_start(frame, True, False, 20)
        #----------------------------------------------------------------------------------
        hb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        self.label_language_scrabble = Gtk.Label()
        self.label_language_scrabble.set_label(_('Playing language:')+' '+config.getv('language_scrabble'))
        hb.set_center_widget(self.label_language_scrabble)
        #-------------------------------------------------------------------------------------------
        img = Gtk.Image.new_from_icon_name('view-grid-symbolic', 2)
        btn_show = Gtk.Button()
        btn_show.set_tooltip_text(_('Show all letters'))
        btn_show.connect('clicked', self.show_all_letters)
        btn_show.set_image(img)
        hb.pack_end(btn_show, False, False, 0)
        vb.pack_start(hb, False, False, 0)
        #----------------------------------------------------------------------------------
        vb.pack_start(Gtk.Separator(), False, False, 10)
        #----------------------------------------------------------------------------------
        hb = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        vb1 = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        frame_player = Gtk.Frame.new(_('Choose the player'))
        frame_player.set_label_align(0.5, 0.5)
        frame_player.set_size_request(180, 220)
        frame_player.add(vb1)
        self.image1 = Gtk.Image()
        vb1.pack_start(self.image1, True, False, 0)
        self.btn_chose1 = Gtk.Button(_('Choose'))
        self.btn_chose1.connect('clicked', self.chose_tile)
        vb1.pack_end(self.btn_chose1, False, False, 0)
        hb.pack_start(frame_player, True, False, 20)
        #----------------------------------------------------------------------------------
        vb2 = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        frame_computer = Gtk.Frame.new(_('Choose the computer'))
        frame_computer.set_label_align(0.5, 0.5)
        frame_computer.set_size_request(180, 220)
        frame_computer.add(vb2)
        self.image2 = Gtk.Image()
        vb2.pack_start(self.image2, True, False, 0)
        btn_chose2 = Gtk.Button(_('Choose'))
        btn_chose2.set_sensitive(False)
        vb2.pack_end(btn_chose2, False, False, 0)
        hb.pack_start(frame_computer, True, False, 20)
        vb.pack_start(hb, True, False, 0)
        #----------------------------------------------------------------------------------
        vb.pack_start(Gtk.Separator(), False, False, 10)
        #----------------------------------------------------------------------------------
        hb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        self.btn_start = Gtk.Button(_('Start game'))
        self.btn_start.set_sensitive(False)
        self.btn_start.connect('clicked', self.start_new_game)
        hb.pack_start(self.btn_start, True, False, 0)
        vb.pack_start(hb, False, False, 0)
        #----------------------------------------------------------------------------------

        self.pack_start(hb0, False, False, 20)
        self.show_all()
        
        
        
        