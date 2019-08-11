#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gtk, Gdk, GObject, Pango, GLib
from gi.repository.GdkPixbuf import Pixbuf
import gettext
import config as config
from about import About
from data import *
import time

# Localization.
DOMAIN = 'gscrabble'
gettext.install(DOMAIN, LOCALDIR)

try:
    lg, enc = locale.getdefaultlocale()
    print('Locale : [%s] ' % lg)
    lang_name = config.getv('language_surface')
    if lang_name != '< System >':
        if lang_name == 'العربية': Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)
        else: Gtk.Widget.set_default_direction(Gtk.TextDirection.LTR)
        lang_code = DICT_LANGUAGES_CODE[lang_name]
        lang = gettext.translation(DOMAIN, LOCALDIR, languages=[lang_code])
        lang.install()
except: pass

from side_letters import SideLetters
from side_infos import SideInfo
from chequer_dnd import Chequer
from scrabble_core import Dict_General
from tool_bar import ToolBar
from page_starting import PageStarting
from rounds import Rounds
from objs_at_fullscreen import OBJs_1
from tools import *
from dialog_preference import DialogPreference
import sqlite3

ACCEL_CTRL_KEY, ACCEL_CTRL_MOD = Gtk.accelerator_parse("<Ctrl>")
ACCEL_SHFT_KEY, ACCEL_SHFT_MOD = Gtk.accelerator_parse("<Shift>")
ACCEL_ALT_KEY, ACCEL_ALT_MOD = Gtk.accelerator_parse("<Alt>")

#===============================================================
class Scrabble(Gtk.Window):

    def __init__(self, *a):
        Gtk.Window.__init__(self)
        self.stack = Gtk.Stack()
        #- objects1 -
        self.list_language_ready = []
        self.list_language_likely = []
        self.list_language_ready_with_dict = []
        self.list_language_ready_without_dict = []
        self.list_language_no_ready_with_stems = []
        self.list_language_no_ready_without_stems = []
        self.select_all_type_lists_language()
        #==========================
        self.LIST_GRADE = [_('Easier'), _('Easy'), _('Medium'), _('Hard'), _('Harder')]
        self.dict_new = {}
        self.dict_new_computer = {}
        self.cells_empty_letter = []
        self.computer_empty_letter = []
        self.list_07_letters_player = []
        self.list_07_letters_computer = []
        self.lang_code = 'ar'
        self.list_letters_repeated = []
        self.help_me = False
        self.ended = False
        self.started = False
        self.count_pieces = 0
        self.last_round_player = True
        self.last_round_computer = True
        self.started_player = 'player' # player or computer
        self.has_msg = False
        self.now_cell = None
        self.select_cell = None
        self.text_msg = ''
        self.not_words = ''
        self.points_player = 0
        self.points_computer = 0
        self.text_words_with_points = ''
        self.full = 0
        self.all_letters = 0
        #- objects2 -
        # self.hd_bar = HeaderBar(self)
        self.tool_bar = ToolBar(self)
        self.dict_chequer = Dict_General(self)
        self.sideletters = SideLetters(self)
        self.sideinfo = SideInfo(self)
        self.chequer = Chequer(self)
        self.rounds = Rounds(self)
        self.pagestarting = PageStarting(self)
        self.objs1 = OBJs_1(self)
        self.ch_font()
        self.build()
    
    #----------------------------------------------------------------------------------
    def quit_app(self, *a):
        if list(self.dict_chequer.values()) != [0,]*225 and self.ended == False and self.all_letters == 0:
            res = sure(self, _('Do you want to save this game?'))
            if res == -8:
                config.setv('saved', 1)
                save_game(self.dict_chequer.copy(), self.text_words_with_points,
                    self.list_letters_repeated.copy(), self.list_07_letters_player.copy(), self.list_07_letters_computer.copy(),
                    self.points_player, self.points_computer, self.cells_empty_letter.copy(), self.computer_empty_letter.copy())
            if res == -9:
                config.setv('saved', 0)
                config.setv('points_player', 0)
                config.setv('points_computer', 0)
        Gtk.main_quit()
    
    def select_all_type_lists_language(self, *a):
        self.list_language_ready.clear()
        self.list_language_likely.clear()
        self.list_language_ready_with_dict.clear()
        self.list_language_ready_without_dict.clear()
        self.list_language_no_ready_with_stems.clear()
        self.list_language_no_ready_without_stems.clear()
        for lang in LANGUAGES_SCRABBLE:
            lang_code = DICT_LANGUAGES_CODE[lang]
            dict_file1 = join(DICTS_DIR, '{}.dict'.format(lang_code,))
            dict_file2 = join(DICTS_HOME, '{}.dict'.format(lang_code,))
            stems_file1 = join(STEMS_DIR, '{}.stems'.format(lang_code,))
            stems_file2 = join(STEMS_HOME, '{}.stems'.format(lang_code,))
            b1 = exists(dict_file1)
            b2 = exists(dict_file2)
            b3 = exists(stems_file1)
            b4 = exists(stems_file2)
            b5 = False
            b6 = False
            if b1:
                con = sqlite3.connect(dict_file1)
                cur = con.cursor()
                cur.execute('SELECT * FROM dict')
                r = cur.fetchall()
                if len(r) > 0: b5 = True
                else: b5 = False
            if b2:
                con = sqlite3.connect(dict_file2)
                cur = con.cursor()
                cur.execute('SELECT * FROM dict')
                r = cur.fetchall()
                if len(r) > 0: b6 = True
                else: b6 = False
            if (b1 or b2) and (b3 or b4) and (b5 or b6): 
                self.list_language_likely.append(lang)
                self.list_language_ready.append(lang)
                self.list_language_ready_with_dict.append(lang)
            elif (b1 or b2) and (b3 or b4): 
                self.list_language_likely.append(lang)
                self.list_language_ready.append(lang)
                self.list_language_ready_without_dict.append(lang)
            elif b3 or b4: 
                self.list_language_likely.append(lang)
                self.list_language_no_ready_with_stems.append(lang)
            else: self.list_language_no_ready_without_stems.append(lang)
    
#     def close_timer(self, *a):
#         self.has_msg = False
#         try: GObject.source_remove(self.time_other)
#         except: pass
#         self.chequer.queue_draw()

    def add_timer(self, text):
        self.has_msg = True
        self.text_msg = text
#         self.time_other = GObject.timeout_add(1000, self.close_timer)
        self.chequer.queue_draw()
    
    def ch_font(self, *a):
        szfont, fmfont = split_font(config.getv('font_win'))
        data = '''* {font-family: "'''+fmfont+'''";
        font-size: '''+szfont+'''px;}'''
        screen = self.get_screen()
        css_provider = Gtk.CssProvider()
        context = self.get_style_context()
        css_provider.load_from_data(data.encode('utf8'))
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def start_new_game(self,*a):
        self.started = True
        self.ended = False
        self.last_round_player = True
        self.last_round_computer = True
        self.sideinfo.sel_count_pieces(config.getn('count_pieces'))
        self.add_timer(_('New game'))
        self.rounds.round_starting(self.started_player)

    def start_old_game(self,*a):
        self.stack.set_visible_child_name('n1')
        # self.hd_bar.show_hide_action_buttons()
        self.tool_bar.show_hide_action_buttons()
        self.started = True
        list_saved = load_game_scrabble()
        for a in list_saved[0].keys():
            self.dict_chequer[a] = list_saved[0][a]
        self.text_words_with_points = list_saved[1]
        self.list_letters_repeated = list_saved[2]
        self.list_07_letters_player = list_saved[3]
        self.list_07_letters_computer = list_saved[4]
        self.points_player = list_saved[5]
        self.points_computer = list_saved[6]
        self.cells_empty_letter = list_saved[7]
        self.computer_empty_letter = list_saved[8]
        self.sideinfo.lab_points_computer.set_label(str(self.points_computer))
        self.sideinfo.lab_points_player.set_label(str(self.points_player))
        if config.getn('point_words') == 0: self.sideinfo.wordviewer_buf.set_text(re.sub('=\d*', '', self.text_words_with_points))
        else: self.sideinfo.wordviewer_buf.set_text(self.text_words_with_points)
        self.sideinfo.wordviewer.with_tag(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '='])
        self.sideletters.liststore_letters_player.clear()
        self.sideletters.add_letters(self.list_07_letters_player)
        self.sideinfo.sel_count_pieces(config.getn('count_pieces'))
        self.add_timer(_('Previous game'))
        time.sleep(0.1)
        while (Gtk.events_pending()): Gtk.main_iteration()
        self.rounds.load_words_help()

    def load_language_game(self, *a):
        lang = config.getv('language_scrabble')
        if lang == None:
            lang = config.getv('language_surface')
        self.lang_code = DICT_LANGUAGES_CODE[lang]
        self.list_letters_repeated = get_list_letters_repeated(self.lang_code)
        self.count_pieces = len(self.list_letters_repeated)
        self.sideinfo.label_count_pieces.set_label(str(self.count_pieces).zfill(3))
        self.dict_chequer.get_data(self.lang_code)

    def restart_game(self, *a):
        self.ended = False
        self.pagestarting.restor_to_starting_page()
        config.setv('saved', 0)
        self.dict_new.clear()
        self.dict_new_computer.clear()
        self.list_07_letters_player = []
        self.list_07_letters_computer = []
        self.cells_empty_letter = []
        self.computer_empty_letter = []
        self.points_player = 0
        self.points_computer = 0
        self.text_words_with_points = ''
        config.setv('points_player', 0)
        config.setv('points_computer', 0)
        self.dict_chequer.clear_dict_all()
        self.sideletters.liststore_letters_player.clear()
        self.sideinfo.lab_points_computer.set_label('00')
        self.sideinfo.lab_points_player.set_label('00')
        self.sideinfo.wordviewer_buf.set_text('')
        self.load()

    def load(self, *a):
        lang = config.getv('language_scrabble')
        if lang == None:
            lang = config.getv('language_surface')
        if lang in self.list_language_ready:
            self.load_language_game()
            if config.getn('saved') == 1:
                try: 
                    self.start_old_game()
                    return
                except: pass
        self.stack.set_visible_child_name('n0')
        # self.hd_bar.show_hide_action_buttons()
        self.tool_bar.show_hide_action_buttons()
    
    def set_fullscreen_cb(self, *a):
        if self.full == 0:
            self.full = 1
            self.fullscreen()
            if self.all_letters == 0:
                self.objs1.set_no_show_all(False)
                self.show_all()
        else:
            self.full = 0
            self.unfullscreen()
            if self.all_letters == 0:
                self.objs1.set_no_show_all(True)
                self.objs1.hide()
    
    def build(self, *a):
        self.connect("delete-event", self.quit_app)
        self.set_default_size(1000, 700)
        self.maximize()
        self.set_icon_name('gscrabble')
        self.set_title(_('Golden Scrabble'))
        # self.set_titlebar(self.hd_bar)
        self.axl = Gtk.AccelGroup()
        self.add_accel_group(self.axl)
        #============================================
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_transition_duration(200)
        #============================================
        self.vbox_window = Gtk.Box(spacing=0,orientation=Gtk.Orientation.VERTICAL)
        self.hb_window = Gtk.Box(spacing=0,orientation=Gtk.Orientation.HORIZONTAL)
        self.vb_letters = Gtk.Box(spacing=0,orientation=Gtk.Orientation.VERTICAL)
        self.vb_letters.pack_start(self.objs1, False, False, 0)
        self.objs1.set_no_show_all(True)
        self.vb_letters.pack_start(self.sideletters, True, True, 0)
        #----------------------------------------------------------------------------------
        # button_names = [Gtk.STOCK_ABOUT, Gtk.STOCK_ADD, Gtk.STOCK_REMOVE, Gtk.STOCK_QUIT]
        # self.buttons = [Gtk.ToolButton.new_from_stock(name) for name in button_names]
        # self.toolbar = Gtk.Toolbar()
        # self.toolbar.set_show_arrow(False)
        # for button in self.buttons:
        #     self.toolbar.insert(button, -1)
        # style_context = self.toolbar.get_style_context()
        # style_context.add_class(Gtk.STYLE_CLASS_INLINE_TOOLBAR)
        #----------------------------------------------------------------------------------
        self.vbox_window.pack_start(self.tool_bar, False, False, 0)
        self.vbox_window.pack_start(self.hb_window, True, True, 0)
        #----------------------------------------------------------------------------------
        self.hb_window.pack_start(self.vb_letters, False, False, 0)
        self.hb_window.pack_start(self.chequer, True, True, 0)
        self.hb_window.pack_start(self.sideinfo, False, False, 0)
        #---------------------------------------------------------------------------------
        self.stack.add_named(self.pagestarting, 'n0')
        self.stack.add_named(self.vbox_window, 'n1')
        #---------------------------------------------------------------------------------
        self.sideletters.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.COPY)
        self.sideletters.drag_source_set_target_list(None)
        self.sideletters.drag_source_add_text_targets()
        self.chequer.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        self.chequer.drag_dest_set_target_list(None)
        self.chequer.drag_dest_add_text_targets()
        self.add(self.stack)
        #------------------------------------------------------------------------------------
        self.axl.connect(Gdk.KEY_F11, 0, Gtk.AccelFlags.VISIBLE, self.set_fullscreen_cb)
        ## self.axl.connect(Gdk.KEY_W, 0, Gtk.AccelFlags.VISIBLE, self.hd_bar.help_me_letters)
        ## self.axl.connect(Gdk.KEY_U, 0, Gtk.AccelFlags.VISIBLE, self.hd_bar.undo_added)
        ## self.axl.connect(Gdk.KEY_S, 0, Gtk.AccelFlags.VISIBLE, self.hd_bar.skip_2_computer)
        ## self.axl.connect(Gdk.KEY_C, 0, Gtk.AccelFlags.VISIBLE, self.hd_bar.change_my_letters)
        ## self.axl.connect(Gdk.KEY_O, 0, Gtk.AccelFlags.VISIBLE, self.hd_bar.apply_added)
        ## self.axl.connect(Gdk.KEY_G, 0, Gtk.AccelFlags.VISIBLE, self.hd_bar.mepref.restart_game)
        self.axl.connect(Gdk.KEY_W, 0, Gtk.AccelFlags.VISIBLE, self.tool_bar.help_me_letters)
        self.axl.connect(Gdk.KEY_U, 0, Gtk.AccelFlags.VISIBLE, self.tool_bar.undo_added)
        self.axl.connect(Gdk.KEY_S, 0, Gtk.AccelFlags.VISIBLE, self.tool_bar.skip_2_computer)
        self.axl.connect(Gdk.KEY_C, 0, Gtk.AccelFlags.VISIBLE, self.tool_bar.change_my_letters)
        self.axl.connect(Gdk.KEY_O, 0, Gtk.AccelFlags.VISIBLE, self.tool_bar.apply_added)
        self.axl.connect(Gdk.KEY_G, 0, Gtk.AccelFlags.VISIBLE, self.tool_bar.mepref.restart_game)
        self.axl.connect(Gdk.KEY_Q, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE, self.quit_app)
        self.axl.connect(Gdk.KEY_P, 0, Gtk.AccelFlags.VISIBLE, lambda *a: DialogPreference(self))
        self.axl.connect(Gdk.KEY_A, 0, Gtk.AccelFlags.VISIBLE, lambda *a: About(self))
        #------------------------------------------------------------------------------------
        self.show_all()
        self.load()

def main():
    Scrabble()
    Gtk.main()

if __name__ == "__main__":
    main()
