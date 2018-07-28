# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk
from word_viewer import Viewer
from data import *
from tools import *
from create_dict import create_dict_language, create_db_language, create_stems_language


#=========================================================
class Add_lang_dict(object): 
    
    def __init__(self, pt, combo):
        self.pt = pt
        self.combo_language = combo
        object.__init__(self)
    
    #--------------------------------------------------------------------------------
    def create_db_language_progress_window(self, lang_code, file_source):
        try: win = Gtk.Window(Gtk.WindowType.POPUP)
        except: 
            win = Gtk.Window()
            win.set_title("مرحبا !")
        win.set_position(Gtk.WindowPosition.CENTER)
        win.set_modal(True)
        win.set_border_width(35)
        win.set_size_request(400,200)
        vb = Gtk.Box(spacing=3, orientation=Gtk.Orientation.VERTICAL)
        lab = Gtk.Label(_('Set up dictionary file...'))
        vb.pack_start(lab, True, True, 0)
        progressbar = Gtk.ProgressBar()
        vb.pack_start(progressbar, False, False, 0)
        win.add(vb)
        win.show_all()
        while (Gtk.events_pending()): Gtk.main_iteration()
        create_stems_language(progressbar, lang_code, file_source)
        win.destroy()
        self.pt.select_all_type_lists_language()
        self.pt.hd_bar.mepref.load_languages_play()
    
    #--------------------------------------------------------------------------------
    def add_language_cb(self, *a):
        lang = self.combo_language.get_active_text()
        lang_code = DICT_LANGUAGES_CODE[lang]
        res = sure(self.pt, _('Do you want to add file of {}'.format(lang, )))
        if res == -8:
            open_dlg = Gtk.FileChooserDialog(_('Choose language file'),
                                         self.pt, Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                         Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
            res1 = open_dlg.run()
            if res1 == Gtk.ResponseType.OK:
                file_source = open_dlg.get_filenames()[0]
                self.create_db_language_progress_window(lang_code, file_source)
            open_dlg.destroy()
    
    #--------------------------------------------------------------------------------
    def create_dictionary_progress_window(self, lang_code, file_source):
        try: win = Gtk.Window(Gtk.WindowType.POPUP)
        except: 
            win = Gtk.Window()
            win.set_title("مرحبا !")
        win.set_position(Gtk.WindowPosition.CENTER)
        win.set_modal(True)
        win.set_border_width(35)
        win.set_size_request(400,200)
        vb = Gtk.Box(spacing=3, orientation=Gtk.Orientation.VERTICAL)
        lab = Gtk.Label(_('Set up dictionary file...'))
        vb.pack_start(lab, True, True, 0)
        progressbar = Gtk.ProgressBar()
        vb.pack_start(progressbar, False, False, 0)
        win.add(vb)
        win.show_all()
        while (Gtk.events_pending()): Gtk.main_iteration()
        create_dict_language(progressbar, lang_code, file_source)
        win.destroy()
        self.pt.select_all_type_lists_language()
    
    #--------------------------------------------------------------------------------
    def add_dictionary_cb(self, *a):
        lang = self.combo_language.get_active_text()
        lang_code = DICT_LANGUAGES_CODE[lang]
        res = sure(self.pt, _('Do you want to add a dictionary of {}'.format(lang, )))
        if res == -8:
            open_dlg = Gtk.FileChooserDialog(_('Choose dictionary file'),
                                         self.pt, Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                         Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
            res1 = open_dlg.run()
            if res1 == Gtk.ResponseType.OK:
                file_source = open_dlg.get_filenames()[0]  
                self.create_dictionary_progress_window(lang_code, file_source)     
            open_dlg.destroy()

      