# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk
from preference import Preference
from word_viewer import Viewer
from change_my_letters import ChangeLetters
from tools import *
from data import *
import time

#===============================================================
class HeaderBar(Gtk.HeaderBar): 
    
    def __init__(self, pt):
        self.pt = pt
        self.list_help_words = []
        self.mepref = Preference(self.pt)
        self.build()
    
    #-----------------------------------------------------------
    def apply_added(self, *a):
        if self.pt.ended: return
        if self.pt.all_letters == 1: return
        if self.pt.stack.get_visible_child_name() == 'n0': return
        if len(self.pt.dict_new) == 0: return
        #--------------------------------------------
        r = self.pt.dict_chequer.check_line()
        if r == 1: self.pt.add_timer(_('You must start from the start cell.'))
        elif r == 2: self.pt.add_timer(_('The word must not be less than two letters.'))
        elif r == 3: self.pt.add_timer(_('Not a single straightness.'))
        elif r == 4: self.pt.add_timer(_('The word must be connected.'))
        elif r == 5: self.pt.add_timer(_('The word must be connected to what preceded it.'))
        #--------------------------------------------
        else:
            list_words_player = self.pt.dict_chequer.find_words_player()
            if list_words_player == None: self.pt.add_timer(_('Some words are not in the dictionary.\n As : {}').format(get_word_complex_letters(self.pt.lang_code, self.pt.not_words),))
            else: 
                play_sound('ok')
                while (Gtk.events_pending()): Gtk.main_iteration()
                time.sleep(0.1)
                self.dialog_help.hide()
                self.pt.rounds.accept_word_player_added(list_words_player)
            
    #-----------------------------------------------------------
    def undo_added(self, *a):
        if self.pt.ended: return
        if self.pt.all_letters == 1: return
        if self.pt.stack.get_visible_child_name() == 'n0': return
        self.pt.select_cell = None
        self.pt.sideletters.undo_added_all()

    #-----------------------------------------------------------
    def help_me_letters(self, *a):
        if self.pt.ended: return
        if self.pt.all_letters == 1: return
        if self.pt.stack.get_visible_child_name() == 'n0': return
        text = ' - '.join(self.list_help_words)
        self.view_help_bfr.set_text(text)
        self.view.with_tag(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '='])
        self.dialog_help.set_no_show_all(False)
        self.entry_search.set_text('')
        self.dialog_help.show_all()
    
    #-----------------------------------------------------------
    def search_dialog_help(self, entry):
        ls0 = []
        text0 = entry.get_text().upper()
        if text0.strip() == '':
            text = ' - '.join(self.list_help_words)
            self.view_help_bfr.set_text(text)
        else:
            for word in self.list_help_words:
                if text0 in word:
                    ls0.append(word)
            text = ' - '.join(ls0)
            self.view_help_bfr.set_text(text)
        
        
    #------------------------------------------------------------
    def change_my_letters(self, *a):
        self.dialog_help.hide()
        if self.pt.ended: return
        if self.pt.all_letters == 1: return
        if self.pt.stack.get_visible_child_name() == 'n0': return
        if len(self.pt.list_letters_repeated) == 0: 
            self.pt.add_timer(_('There are no letters to change.'))
            return
        self.undo_added()
        ChangeLetters(self.pt)
    
    #------------------------------------------------------------
    def skip_2_computer(self, *a):
        self.dialog_help.hide()
        if self.pt.ended: return
        if self.pt.all_letters == 1: return
        if self.pt.stack.get_visible_child_name() == 'n0': return
        if self.pt.last_round_computer == False:
            if len(self.list_help_words) == 0:
                self.pt.rounds.end_game()
                return
            res = sure(self.pt, _('Computer does not have a word if you pass the role to it, the game will end. \n Do you want that?'))
            if res == -8:
                self.pt.rounds.end_game()
                return
            else: return
        res = sure(self.pt, _('If you do not have a word you will take the computer role.'))
        if res == -8:
            self.pt.sideletters.undo_added_all()
            time.sleep(0.1)
            self.pt.last_round_player = False
            self.pt.rounds.round_computer()
    
    def show_hide_action_buttons(self, *a):
        if self.pt.all_letters == 0 and self.pt.stack.get_visible_child_name() == 'n1':
            self.hb_actions.set_no_show_all(False)
            self.hb_actions.show_all()
            self.btn_apply.set_no_show_all(False)
            self.btn_apply.show_all()
            self.btn_close_show_letters.set_no_show_all(True)
            self.btn_close_show_letters.hide()
            self.combo_language_preview.set_no_show_all(True)
            self.combo_language_preview.hide()
        elif self.pt.all_letters == 1:
            self.hb_actions.set_no_show_all(True)
            self.hb_actions.hide()
            self.btn_apply.set_no_show_all(True)
            self.btn_apply.hide()
            self.btn_close_show_letters.set_no_show_all(False)
            self.btn_close_show_letters.show_all()
            self.combo_language_preview.set_no_show_all(False)
            self.combo_language_preview.show_all()
        else:
            self.hb_actions.set_no_show_all(True)
            self.hb_actions.hide()
            self.btn_apply.set_no_show_all(True)
            self.btn_apply.hide()
            self.btn_close_show_letters.set_no_show_all(True)
            self.btn_close_show_letters.hide()
            self.combo_language_preview.set_no_show_all(True)
            self.combo_language_preview.hide()

    def close_show_letters(self, *a):
        self.pt.all_letters = 0
        self.pt.stack.set_visible_child_name('n0')
        self.pt.show_all()
        self.show_hide_action_buttons()
        self.pt.dict_chequer.clear_dict_all()
        name = config.getv('language_scrabble')
        self.pt.lang_code = DICT_LANGUAGES_CODE[name]
    
    def sel_language_preview(self, *a):
        name = self.combo_language_preview.get_active_text()
        self.pt.lang_code = DICT_LANGUAGES_CODE[name]
        list_letters_repeated = []
        for letter in DICT_LETTERS[self.pt.lang_code].keys():
            list_letters_repeated.extend([letter,]*DICT_LETTERS[self.pt.lang_code][letter][0])
        list_letters_repeated.sort()
        self.pt.dict_chequer.clear()
        for a in range(len(list_letters_repeated)):
            self.pt.dict_chequer[a] = list_letters_repeated[a]
        self.pt.chequer.queue_draw()
    
    def build(self, *a):
        Gtk.HeaderBar.__init__(self)
        self.set_show_close_button(True)
        self.set_title(_('Golden Scrabble'))
        #===========================================
        self.hb_actions = Gtk.Box(spacing=0,orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.hb_actions.get_style_context(), "linked")
        #-------------------------------------------------------------------------------------------
        img = Gtk.Image.new_from_icon_name('dialog-information-symbolic', 2)
        btn_help = Gtk.Button()
        btn_help.set_tooltip_text(_('Suggested word list.'))
        btn_help.connect('clicked', self.help_me_letters)
        btn_help.set_image(img)
        self.hb_actions.pack_start(btn_help, False, False, 0)
        #-------------------------------------------------------------------------------------------
        nm_icon = 'edit-undo-symbolic'
        if self.pt.get_direction() == Gtk.TextDirection.RTL: nm_icon = 'edit-undo-symbolic-rtl'
        img = Gtk.Image.new_from_icon_name(nm_icon, 2)
        btn_undo = Gtk.Button()
        btn_undo.set_tooltip_text(_('Undo install letters.'))
        btn_undo.connect('clicked', self.undo_added)
        btn_undo.set_image(img)
        self.hb_actions.pack_start(btn_undo, False, False, 0)
        #--------------------------------------------------------------------------------------------
        nm_icon = 'media-seek-forward-symbolic'
        if self.pt.get_direction() == Gtk.TextDirection.RTL: nm_icon = 'media-seek-forward-symbolic-rtl'
        img = Gtk.Image.new_from_icon_name(nm_icon, 2)
        btn_no_play = Gtk.Button()
        btn_no_play.set_tooltip_text(_('I have no word passed the role to the computer.'))
        btn_no_play.connect('clicked', self.skip_2_computer)
        btn_no_play.set_image(img)
        self.hb_actions.pack_start(btn_no_play, False, False, 0)
        #-------------------------------------------------------------------------------------------
        img = Gtk.Image.new_from_icon_name('view-refresh-symbolic', 2)
        btn_change = Gtk.Button()
        btn_change.set_tooltip_text(_('Change my letter group.'))
        btn_change.connect('clicked', self.change_my_letters)
        btn_change.set_image(img)
        self.hb_actions.pack_start(btn_change, False, False, 0)
        self.pack_start(self.hb_actions)
        #---------------------------------------------------------------------------------------------
        img = Gtk.Image.new_from_icon_name('system-shutdown-symbolic', 2)
        self.btn_close_show_letters = Gtk.Button()
        self.btn_close_show_letters.set_tooltip_text(_('Close the preview.'))
        self.btn_close_show_letters.connect('clicked', self.close_show_letters)
        self.btn_close_show_letters.set_image(img)
        self.pack_start(self.btn_close_show_letters)
        self.btn_close_show_letters.set_no_show_all(True)
        #---------------------------------------------------------------------------------------------
        self.combo_language_preview = Gtk.ComboBoxText()
        for t in LANGUAGES_SCRABBLE:
            self.combo_language_preview.append_text(t)
        self.combo_language_preview.set_wrap_width(5)
        self.pack_start(self.combo_language_preview)
        self.combo_language_preview.connect('changed', self.sel_language_preview)
        #---------------------------------------------------------------------------------------------
        img = Gtk.Image.new_from_icon_name('emblem-ok-symbolic', 2)
        self.btn_apply = Gtk.Button()
        self.btn_apply.set_size_request(80, -1)
        self.btn_apply.set_tooltip_text(_('Adopted the word that I set.'))
        self.btn_apply.connect('clicked', self.apply_added)
        self.btn_apply.set_image(img)
        self.pack_start(self.btn_apply)
        #-------------------------------------------------------------------------------------------
        img = Gtk.Image.new_from_icon_name('view-fullscreen-symbolic', 2)
        self.btn_fullscreen = Gtk.Button()
        self.btn_fullscreen.set_tooltip_text(_('Fullscreen'))
        self.btn_fullscreen.connect('clicked', self.pt.set_fullscreen_cb)
        self.btn_fullscreen.set_image(img)
        self.pack_end(self.btn_fullscreen)
        #- btn_pref---------------------------------------------------------------------------------
        img = Gtk.Image.new_from_icon_name('open-menu-symbolic', 2)
        self.btn_pref = Gtk.MenuButton()
        self.btn_pref.set_tooltip_text(_('Preference'))
        self.popover_pref = Gtk.Popover()
        self.btn_pref.set_popover(self.popover_pref)
        self.btn_pref.set_name('btn_pref')
        self.btn_pref.set_image(img)
        self.popover_pref.add(self.mepref)
        self.pack_end(self.btn_pref)
        #- dialog_help---------------------------------------------------------------------------------
        self.dialog_help = Gtk.Dialog(parent=self.pt, title=_('Suggested words'))
        self.dialog_help.connect("delete-event", lambda *a: self.dialog_help.hide() or True) 
        hb_bar = Gtk.HeaderBar()
        hb_bar.set_show_close_button(True)
        self.dialog_help.set_titlebar(hb_bar)
        hb_bar.set_title(_('Suggested words'))
        self.entry_search = Gtk.SearchEntry()
        self.entry_search.connect('changed', self.search_dialog_help)
        hb_bar.pack_start(self.entry_search)
        self.dialog_help.set_default_size(450, 300)
        area = self.dialog_help.get_content_area()
        area.set_spacing(6)
        self.view = Viewer(self.pt)
        self.view_help_bfr = self.view.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view)
        area.pack_start(scroll, True, True, 0)
        self.dialog_help.set_no_show_all(True)
        self.set_custom_title(Gtk.Label(_('Golden Scrabble')))
        self.show_hide_action_buttons()
        
        
        