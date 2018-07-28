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
from text_help import *
from word_viewer import Viewer
from add_lang_dict import Add_lang_dict

#===============================================================
class DialogPreference(Gtk.Dialog):
    
    def __init__(self, pt):
        self.pt = pt
        self.build()  
    
    #-----------------------------------------------------------
    def ch_sound(self, btn):
        nconf = btn.get_name()
        config.setv(nconf, btn.get_value())
        name = nconf.replace('_ms', '').replace('pipe_', '')
        play_sound(name)
    
    #-----------------------------------------------------------
    def ch_font(self, btn):
        nconf = btn.get_name()
        font = btn.get_font()
        config.setv(nconf, font)
        self.pt.ch_font()
        self.pt.chequer.queue_draw()
    
    #-----------------------------------------------------------
    def ch_thick(self, btn):
        v = btn.get_value()
        config.setv('br_thick', v)
        self.pt.chequer.queue_draw()
    
    #-----------------------------------------------------------
    def ch_color(self, btn):
        nconf = btn.get_name()
        color = btn.get_rgba().to_string()
        config.setv(nconf, color)
        self.pt.sideinfo.wordviewer.change_theme()
        self.pt.hd_bar.view.change_theme()
        self.pt.sideletters.change_theme()
        self.pt.chequer.queue_draw()
    
    #-----------------------------------------------------------
    def set_default(self, btn, n):
        self.pt.hd_bar.btn_pref.set_active(False)
        res = sure(self.pt, _('Do you want to restore the default settings?'))
        if res == -8:
            if n == 2:
                fg_pieces = 'rgb(32,74,135)'
                fg_cell = 'rgb(46,52,54)'
                bg_pieces = 'rgb(253,253,215)'
                bg_no_install = 'rgb(255,245,154)'
                bg_last_word =  'rgb(221,245,125)'
                fg_nbr = 'rgb(204,0,0)'
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
                config.setv('fg_pieces', fg_pieces)
                config.setv('fg_nbr', fg_nbr)
                config.setv('fg_cell', fg_cell)
                config.setv('bg_pieces', bg_pieces)
                config.setv('bg_no_install', bg_no_install)
                config.setv('bg_last_word', bg_last_word)
                config.setv('sel_pieces', sel_pieces)
                config.setv('br_pieces', br_pieces)
                config.setv('bg_area', bg_area)
                config.setv('bg_grid', bg_grid)
                config.setv('br_grid', br_grid)
                config.setv('bg_lines', bg_lines)
                config.setv('fg_msg', fg_msg)
                config.setv('bg_hX2', bg_hX2)
                config.setv('bg_hX3', bg_hX3)
                config.setv('bg_kX2', bg_kX2)
                config.setv('bg_kX3', bg_kX3)
                config.setv('bg_start', bg_start)
            elif n == 1:
                config.setv('font_pieces', 'Sans 11')
                config.setv('font_msg', 'Sans 25')
                config.setv('font_win', 'Sans 15')
                config.setv('font_special', 'Sans 15')
                config.setv('br_thick', 1)
            elif n == 3:
                config.setv('pipe_drop', 9000)
                config.setv('pipe_ok', 5000)
                config.setv('pipe_undo', 1300)
                config.setv('pipe_add', 9000)    
                config.setv('pipe_drop_ms', 20)
                config.setv('pipe_ok_ms', 20)
                config.setv('pipe_undo_ms', 20)
                config.setv('pipe_add_ms', 20)
            self.pt.ch_font()
            self.pt.sideinfo.wordviewer.change_theme()
            self.pt.hd_bar.view.change_theme()
            self.pt.sideletters.change_theme()
            self.pt.chequer.queue_draw()

    #-----------------------------------------------------------
    def sel_language_surface(self, btn):
        self.pt.hd_bar.btn_pref.set_active(False)
        name = btn.get_active_text()
        config.setv('language_surface', name)
        info(self.pt, _('It will do the change after you restart the program.'))
    
    #-----------------------------------------------------------
    def sel_grade(self, btn, n):
        config.setv('grade', n)
        self.pt.sideinfo.label_grade.set_label(self.pt.LIST_GRADE[n])
    
    #-----------------------------------------------------------
    def sel_language_scrabble(self, btn):
        name = btn.get_active_text()
        if name == config.getv('language_scrabble'): return
        self.pt.hd_bar.btn_pref.set_active(False)
        if list(self.pt.dict_chequer.values()) == [0,]*225 or self.pt.ended == True: pass
        else:
            res = sure(self.pt, _('If you want to change the language you will need to start a new game. \n Do you want that?'))
            if res == -8: pass
            else:
                btn.set_active(config.getn('language_scrabble')) 
                return
        config.setv('language_scrabble', name)
        self.pt.sideinfo.label_language_scrabble.set_label(name)
        self.pt.pagestarting.label_language_scrabble.set_label(_('Playing language:')+' '+name)
        self.pt.pagestarting.restor_to_starting_page()
        self.pt.restart_game()
    
    #-----------------------------------------------------------
    def restart_game(self, *a):
        if self.pt.all_letters == 1: return
        self.pt.hd_bar.btn_pref.set_active(False)
        if list(self.pt.dict_chequer.values()) == [0,]*225: self.pt.restart_game()
        if self.pt.ended == True: self.pt.restart_game()
        if self.pt.stack.get_visible_child_name() == 'n0':  self.pt.restart_game()
        else:
            res = sure(self.pt, _('If you want to start a new game you will lose the current game. \n Do you want that?'))
            if res == -8:
                self.pt.restart_game()
    
    #-----------------------------------------------------------
    def set_autohide_info(self, btn):
        n = btn.get_active()
        if n:
            config.setv('autohide_info', 1)
            if self.pt.all_letters == 0:
                self.pt.sideinfo.set_no_show_all(True)
                self.pt.sideinfo.hide()
        else:
            config.setv('autohide_info', 0)
            if self.pt.all_letters == 0:
                self.pt.sideinfo.set_no_show_all(False)
                self.pt.sideinfo.show_all()
    
    #-----------------------------------------------------------
    def set_autohide_letters(self, btn):
        n = btn.get_active()
        if n:
            config.setv('autohide_letters', 1)
            if self.pt.all_letters == 0:
                self.pt.vb_letters.set_no_show_all(True)
                self.pt.vb_letters.hide()
        else:
            config.setv('autohide_letters', 0)
            if self.pt.all_letters == 0:
                self.pt.vb_letters.set_no_show_all(False)
                self.pt.vb_letters.show_all()
    
    def load_languages_play(self, *a):
        self.combo_language_scrabble.remove_all()
        for lang in self.pt.list_language_likely:
            self.combo_language_scrabble.append_text(lang)
    
    #-----------------------------------------------------------
    def on_switch_activated(self, *a):
        if self.switch_sound.get_active():
            config.setv('sound', 1)
        else:
            config.setv('sound', 0)
    
    
    def sel_added(self, *a):
        self.combo_dict_lang.remove_all()
        if self.check_add_dict.get_active():
            self.combo_dict_lang.set_wrap_width(2)
            self.view_lang_dict.view_bfr.set_text(TEXT_ADD_DICT)
            for lang in self.pt.list_language_ready_without_dict:
                self.combo_dict_lang.append_text(lang)
        else:
            self.view_lang_dict.view_bfr.set_text(TEXT_ADD_LANG)
            self.combo_dict_lang.set_wrap_width(5)
            for lang in self.pt.list_language_no_ready_without_stems:
                self.combo_dict_lang.append_text(lang)
        self.view_lang_dict.with_tag(['"="', '↓', _('How do I add my dictionary?'), _('How do I add my language?')])
        try: self.combo_dict_lang.set_active(self.pt.list_language_ready_without_dict.index(config.getv('language_scrabble')))
        except: self.combo_dict_lang.set_active(0)
    
    def add_dict_lang_cb(self, *a):
        if self.check_add_dict.get_active():
            self.add_lg_dt.add_dictionary_cb()
        else:
            self.add_lg_dt.add_language_cb()
    
    #-----------------------------------------------------------
    def build(self, *a):
        Gtk.Dialog.__init__(self, parent=self.pt)
        area = self.get_content_area()
        self.set_icon_name("gscrabble")
        self.set_title(_('Preference'))
        self.set_default_size(500, 450)
        hbox = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        #---------------------------
        self.stack_pref = Gtk.Stack()
        self.stack_pref.set_border_width(7)
        self.stack_pref.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack_pref.set_transition_duration(300)
        stack_switcher = Gtk.StackSwitcher(spacing=1,orientation=Gtk.Orientation.VERTICAL)
        stack_switcher.set_homogeneous(True)
        stack_switcher.set_stack(self.stack_pref)
        hbox.pack_start(stack_switcher, False, False, 0)
        hbox.pack_start(self.stack_pref, True, True, 0)
        area.pack_start(hbox, True, True, 0)
        #---------------------------
        view_info = Viewer(self.pt)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(view_info)
        view_info.view_bfr.set_text(TEXT_HOW_PLAY)
        list_tag = [
            '=',
            _('''How to Play Scrabble'''),
            _('''This is the law of the game in fact'''),
            _('''1- Make sure that you have everything you need to play Scrabble:'''),
            _('''2- Choose a dictionary to use for challenges:'''),
            _('''3- Put the tiles in the bag and shake them:'''),
            _('''4- Determine who goes first:'''),
            _('''5- Draw your tiles:'''),
            _('''6- Play the first word:'''),
            _('''7- Count up your points:'''),
            _('''8- Draw new tiles:'''),
            _('''9- Build on other players’ words:'''),
            _('''10-  Use your tiles to get the highest score possible per turn:'''),
            _('''11-  Challenge other players to dispute a word:'''),
            _('''12- Exchange tiles you don’t want:'''),
            _('''13- Watch for Premium Score squares:'''),
            _('''14- Get 50 points added to your word score if you get a bingo, also known as a bonus:'''),
            _('''15- Add up each player’s scores at the end of the game:'''),
            _('''16- Announce the winner:''')
            ]
        view_info.with_tag(list_tag)
        
        self.stack_pref.add_titled(scroll, 'n0', _('Game Code'))
        
        #---------------------------
        view_hotkeys = Viewer(self.pt)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(view_hotkeys)
        view_hotkeys.view_bfr.set_text(TEXT_HOT_KEYS)
        view_hotkeys.with_tag(['"A"', '"Q+Ctrl"', '"O"', '"P"', '"U"', '"C"', '"S"', '"W"', '"G"', '"F11"', _('The right button:'), _('The left button:'), _('Mouse:')])
        
        self.stack_pref.add_titled(scroll, 'n00', _('Hot Keys'))
        
        #---------------------------
        vb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)        
        hb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label.new(_('Interface language:')), False, False, 0)
        self.combo_language_surface = Gtk.ComboBoxText()
        # self.combo_language_surface.set_wrap_width(2)
        self.combo_language_surface.set_size_request(150, -1)
        for lang in LANGUAGES_SURFACE:
            self.combo_language_surface.append_text(lang)
        self.combo_language_surface.set_active(LANGUAGES_SURFACE.index(config.getv('language_surface')))
        self.combo_language_surface.connect('changed', self.sel_language_surface)
        hb.pack_end(self.combo_language_surface, False, False, 0)
        vb.pack_start(hb, False, False, 0)
        
        hb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label.new(_('Playing language:')), False, False, 0)
        self.combo_language_scrabble = Gtk.ComboBoxText()
        self.combo_language_scrabble.set_wrap_width(2)
        self.combo_language_scrabble.set_size_request(150, -1)
        self.load_languages_play()
        try: i = self.pt.list_language_likely.index(config.getv('language_scrabble'))
        except: i = -1
        self.combo_language_scrabble.set_active(i)
        self.combo_language_scrabble.connect('changed', self.sel_language_scrabble)
        hb.pack_end(self.combo_language_scrabble, False, False, 0)
        vb.pack_start(hb, False, False, 0)
        vb.pack_start(Gtk.Separator(), False, False, 0)
        
        hb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        self.check_add_lang = Gtk.RadioButton.new_with_label_from_widget(None, _('Add language'))
        hb.pack_start(self.check_add_lang, True, True, 0)
        
        self.check_add_dict = Gtk.RadioButton.new_with_label_from_widget(self.check_add_lang, _('Add dictionary'))
        hb.pack_start(self.check_add_dict, True, True, 0)
        vb.pack_start(hb, False, False, 0)
        
        self.view_lang_dict = Viewer(self.pt)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_lang_dict)
        vb.pack_start(scroll, True, True, 0)
        
        hb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        self.combo_dict_lang = Gtk.ComboBoxText()
        self.add_lg_dt = Add_lang_dict(self.pt, self.combo_dict_lang)
        btn_add_dict = Gtk.Button(_('Add'))
        btn_add_dict.connect('clicked', self.add_dict_lang_cb)
        hb.pack_start(btn_add_dict, False, False, 0)
        self.combo_dict_lang.set_size_request(150, -1)
        hb.pack_end(self.combo_dict_lang, False, False, 0)
        vb.pack_start(hb, False, False, 0)
        self.check_add_lang.connect("toggled", self.sel_added, 1)
        self.check_add_dict.connect("toggled", self.sel_added, 2)
        self.check_add_lang.set_active(True)
        self.sel_added()
        
        self.stack_pref.add_titled(vb, 'n1', _('Language'))
        #----------------------------------------------------------------------------------
        vb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)    
        vb.pack_start(Gtk.Label.new(_('Difficulty level:')), False, False, 0)

        btn0 = Gtk.RadioButton.new_with_label_from_widget(None, self.pt.LIST_GRADE[0])
        btn0.connect("toggled", self.sel_grade, 0)
        vb.pack_start(btn0, False, False, 0)
        if config.getn('grade') == 0: btn0.set_active(True)
        
        btn1 = Gtk.RadioButton.new_with_label_from_widget(btn0, self.pt.LIST_GRADE[1])
        btn1.connect("toggled", self.sel_grade, 1)
        vb.pack_start(btn1, False, False, 0)
        if config.getn('grade') == 1: btn1.set_active(True)
        
        btn2 = Gtk.RadioButton.new_with_label_from_widget(btn1, self.pt.LIST_GRADE[2])
        btn2.connect("toggled", self.sel_grade, 2)
        vb.pack_start(btn2, False, False, 0)
        if config.getn('grade') == 2: btn2.set_active(True)
        
        btn3 = Gtk.RadioButton.new_with_label_from_widget(btn2, self.pt.LIST_GRADE[3])
        btn3.connect("toggled", self.sel_grade, 3)
        vb.pack_start(btn3, False, False, 0)
        if config.getn('grade') == 3: btn3.set_active(True)
        
        btn4 = Gtk.RadioButton.new_with_label_from_widget(btn3, self.pt.LIST_GRADE[4])
        btn4.connect("toggled", self.sel_grade, 4)
        vb.pack_start(btn4, False, False, 0)
        if config.getn('grade') == 4: btn4.set_active(True)
        
        self.stack_pref.add_titled(vb, 'n2', _('Difficulty'))
        
        #----------------------------
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        vb0 = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        vb0.set_border_width(20)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.NONE)
        scroll.add(vb0)
        ls_btn_font = [('font_pieces', _('Font of letters')), ('font_special', _('Font of cells')), ('font_msg', _('Font of notification')),('font_win', _('Font of window'))]
        for a in ls_btn_font:
            hb = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
            btn = Gtk.FontButton.new_with_font(config.getv(a[0]))
            btn.set_name(a[0])
            btn.connect('font-set',self.ch_font)
            hb.pack_start(Gtk.Label.new(a[1]), False, False, 0)
            hb.pack_end(btn, False, False, 0)
            vb0.pack_start(hb, False, False, 0)
        hb = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        adj = Gtk.Adjustment.new(1, 1, 10, 1, 5, 0)
        btn= Gtk.SpinButton()
        btn.set_adjustment(adj)
        btn.set_wrap(True)
        btn.set_value(config.getf('br_thick'))
        btn.connect('value-changed',self.ch_thick)
        hb.pack_start(Gtk.Label.new(_('Lines of grid')), False, False, 0)
        hb.pack_end(btn, False, False, 0)
        vb0.pack_start(hb, False, False, 0)
        
        vb.pack_start(scroll, True, True, 0)
        vb.pack_start(Gtk.Separator(), False, False, 3)
        btn_default = Gtk.ToolButton()
        btn_default.set_label(_('Prepare defaults'))
        vb.pack_start(btn_default, False, False, 0)
        btn_default.connect('clicked', self.set_default, 1)
        self.stack_pref.add_titled(vb, 'n3', _('Fonts'))
        
        #---------------------------
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        vb0 = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        vb0.set_border_width(20)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.NONE)
        scroll.add(vb0)
        hb = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        ls_btn_color = [('fg_pieces',_('Color of letter')), ('fg_nbr',_('Color of number')), ('fg_cell',_('Word of cell')), ('bg_pieces',_('Background of letter')), 
                        ('bg_no_install', _('New piece')), ('bg_last_word', _('Last word')), ('br_pieces',_('Border of letter')), 
                        ('bg_area',_('Background')), ('bg_grid',_('Background of grid')), 
                        ('br_grid',_('Border of grid')),('bg_lines',_('Lines of grid')), ('fg_msg',_('Color of notification')),
                        ('bg_start',_('Start')),('bg_hX2',_('Background of DLS')),('bg_hX3',_('Background of TLS')),
                        ('bg_kX2',_('Background of DWS')),('bg_kX3',_('Background of TWS'))]
        for a in ls_btn_color:
            hb = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
            btn = Gtk.ColorButton.new_with_rgba(rgba(config.getv(a[0])))
            btn.set_name(a[0])
            btn.connect('color-set',self.ch_color)
            hb.pack_start(Gtk.Label.new(a[1]), False, False, 0)
            hb.pack_end(btn, False, False, 0)
            vb0.pack_start(hb, False, False, 0)
        vb.pack_start(scroll, True, True, 0)
        
        vb.pack_start(Gtk.Separator(), False, False, 3)
        btn_default = Gtk.ToolButton()
        btn_default.set_label(_('Prepare defaults'))
        vb.pack_start(btn_default, False, False, 0)
        btn_default.connect('clicked', self.set_default, 2)
        self.stack_pref.add_titled(vb, 'n4', _('Colors'))
        
        #---------------------------
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        vb0 = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        vb0.set_border_width(20)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_shadow_type(Gtk.ShadowType.NONE)
        scroll.add(vb0)
        
        hb = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        self.switch_sound = Gtk.Switch()
        self.switch_sound.connect("notify::active", self.on_switch_activated)
        if config.getn('sound') == 1: self.switch_sound.set_active(True)
        else: self.switch_sound.set_active(False)
        hb.pack_start(Gtk.Label.new(_('Enable audio')), False, False, 0)
        hb.pack_start(self.switch_sound, False, False, 0)
        vb.pack_start(hb, False, False, 0)
        vb.pack_start(Gtk.Separator(), False, False, 3)
        
        ls_btn_sound = [('pipe_drop', _('Install a letter')), ('pipe_ok', _('Adoption of the word')), ('pipe_undo', _('Undo a letter')),
                        ('pipe_add', _('Add a letters'))]
        for a in ls_btn_sound:
            hb = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
            adj1 = Gtk.Adjustment.new(20, 1, 1000, 1, 5, 0)
            btn= Gtk.SpinButton()
            btn.set_adjustment(adj1)
            btn.set_wrap(True)
            btn.set_value(config.getf(a[0]+"_ms"))
            btn.set_name(a[0]+"_ms")
            btn.connect('value-changed',self.ch_sound)
            hb.pack_end(btn, False, False, 0)
            #-----------------------------------------
            adj = Gtk.Adjustment.new(1, 0, 10000, 1, 5, 0)
            btn= Gtk.SpinButton()
            btn.set_adjustment(adj)
            btn.set_wrap(True)
            btn.set_value(config.getf(a[0]))
            btn.set_name(a[0])
            btn.connect('value-changed',self.ch_sound)
            hb.pack_end(btn, False, False, 0)
            hb.pack_start(Gtk.Label.new(a[1]), False, False, 0)
            vb0.pack_start(hb, False, False, 0)
        vb.pack_start(scroll, True, True, 0)
        
        vb.pack_start(Gtk.Separator(), False, False, 3)
        btn_default = Gtk.ToolButton()
        btn_default.set_label(_('Prepare defaults'))
        vb.pack_start(btn_default, False, False, 0)
        btn_default.connect('clicked', self.set_default, 3)
        self.stack_pref.add_titled(vb, 'n5', _('Sounds'))
        
        #---------------------------
        vb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        check_autohid_info = Gtk.CheckButton(_('Autohide the information box'))
        if config.getn('autohide_info') == 1: check_autohid_info.set_active(True)
        vb.pack_start(check_autohid_info, False, False, 0)
        check_autohid_info.connect('clicked', self.set_autohide_info)
        
        check_autohid_letters = Gtk.CheckButton(_('Autohide the letters box'))
        if config.getn('autohide_letters') == 1: check_autohid_letters.set_active(True)
        vb.pack_start(check_autohid_letters, False, False, 0)
        check_autohid_letters.connect('clicked', self.set_autohide_letters)

        self.stack_pref.add_titled(vb, 'n6', _('Others'))
        
        
        self.show_all()
        
        