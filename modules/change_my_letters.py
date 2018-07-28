# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from gi.repository import Gtk
from create_png import get_letter_png
import time

#===============================================================
class ChangeLetters(Gtk.Dialog):
    
    def __init__(self, pt):
        self.pt = pt
        self.build() 
    
    def rm_item_in_store(self, model, path, i, letter):
        letter0 = model.get(i,1)[0]
        if letter0.replace('"', '').replace("'", "") == letter: 
            model.remove(i)
            return True 
        else:
            return False
    
    def change_letters(self, *a):
        new_list = []
        for btn in [self.check_btn0, self.check_btn1, self.check_btn2, self.check_btn3, self.check_btn4, self.check_btn5, self.check_btn6]:
            if btn.get_active(): 
                l = self.pt.list_07_letters_player[0]
                new_list.append(l)
                self.pt.list_07_letters_player.remove(l)
                try: self.pt.sideletters.liststore_letters_player.foreach(self.rm_item_in_store, l)
                except: pass
        if len(new_list) == 0:
            return
        self.pt.not_words = ""
        self.pt.list_letters_repeated.extend(new_list)
        self.pt.rounds.chose_letters_player()
        self.destroy()
        time.sleep(0.1)
        self.pt.rounds.round_computer()
    
    def select_all(self, *a):
        if self.check_all.get_active():
            self.check_btn0.set_active(True)
            self.check_btn1.set_active(True)
            self.check_btn2.set_active(True)
            self.check_btn3.set_active(True)
            self.check_btn4.set_active(True)
            self.check_btn5.set_active(True)
            self.check_btn6.set_active(True)
        else:
            self.check_btn0.set_active(False)
            self.check_btn1.set_active(False)
            self.check_btn2.set_active(False)
            self.check_btn3.set_active(False)
            self.check_btn4.set_active(False)
            self.check_btn5.set_active(False)
            self.check_btn6.set_active(False)
    
    #-----------------------------------------------------------
    def build(self, *a):
        Gtk.Dialog.__init__(self, parent=self.pt)
        area = self.get_content_area()
        area.set_border_width(0)
        self.set_icon_name("gscrabble")
        self.set_title(_('Change my letters'))
        self.set_resizable(False)
        #---------------------------
        info_bar = Gtk.InfoBar(show_close_button=False)
        info_bar.set_message_type(1)
        lab_bar = Gtk.Label(_('If you change the letters set, you lose your role.'))
        info_bar.get_content_area().pack_start(lab_bar, True, False, 0)
        area.pack_start(info_bar, False, False, 0)
        #---------------------------
        hbox = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_border_width(10)
        lab = Gtk.Label(_('Select the letters to be changed.'))
        hbox.pack_start(lab, False, False, 0)
        self.check_all = Gtk.CheckButton(_('All'))
        self.check_all.connect('toggled', self.select_all)
        hbox.pack_end(self.check_all, False, False, 0)
        area.pack_start(hbox, False, False, 10)
        area.pack_start(Gtk.Separator(), False, False, 5)
        #---------------------------
        hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_border_width(10)
        vbox = Gtk.Box(spacing=0,orientation=Gtk.Orientation.VERTICAL)
        png_file = get_letter_png(self.pt.lang_code, self.pt.list_07_letters_player[0])
        img = Gtk.Image.new_from_file(png_file)
        self.check_btn0 = Gtk.CheckButton()
        vbox.pack_start(self.check_btn0, False, False, 0)
        vbox.pack_start(img, False, False, 0)
        hbox.pack_end(vbox, False, False, 0)
        #----------------------------
        vbox = Gtk.Box(spacing=0,orientation=Gtk.Orientation.VERTICAL)
        png_file = get_letter_png(self.pt.lang_code, self.pt.list_07_letters_player[1])
        img = Gtk.Image.new_from_file(png_file)
        self.check_btn1 = Gtk.CheckButton()
        vbox.pack_start(self.check_btn1, False, False, 0)
        vbox.pack_start(img, False, False, 0)
        hbox.pack_end(vbox, False, False, 0)
        #----------------------------
        vbox = Gtk.Box(spacing=0,orientation=Gtk.Orientation.VERTICAL)
        png_file = get_letter_png(self.pt.lang_code, self.pt.list_07_letters_player[2])
        img = Gtk.Image.new_from_file(png_file)
        self.check_btn2 = Gtk.CheckButton()
        vbox.pack_start(self.check_btn2, False, False, 0)
        vbox.pack_start(img, False, False, 0)
        hbox.pack_end(vbox, False, False, 0)
        #----------------------------
        vbox = Gtk.Box(spacing=0,orientation=Gtk.Orientation.VERTICAL)
        png_file = get_letter_png(self.pt.lang_code, self.pt.list_07_letters_player[3])
        img = Gtk.Image.new_from_file(png_file)
        self.check_btn3 = Gtk.CheckButton()
        vbox.pack_start(self.check_btn3, False, False, 0)
        vbox.pack_start(img, False, False, 0)
        hbox.pack_end(vbox, False, False, 0)
        #----------------------------
        vbox = Gtk.Box(spacing=0,orientation=Gtk.Orientation.VERTICAL)
        png_file = get_letter_png(self.pt.lang_code, self.pt.list_07_letters_player[4])
        img = Gtk.Image.new_from_file(png_file)
        self.check_btn4 = Gtk.CheckButton()
        vbox.pack_start(self.check_btn4, False, False, 0)
        vbox.pack_start(img, False, False, 0)
        hbox.pack_end(vbox, False, False, 0)
        #----------------------------
        vbox = Gtk.Box(spacing=0,orientation=Gtk.Orientation.VERTICAL)
        png_file = get_letter_png(self.pt.lang_code, self.pt.list_07_letters_player[5])
        img = Gtk.Image.new_from_file(png_file)
        self.check_btn5 = Gtk.CheckButton()
        vbox.pack_start(self.check_btn5, False, False, 0)
        vbox.pack_start(img, False, False, 0)
        hbox.pack_end(vbox, False, False, 0)
        #----------------------------
        vbox = Gtk.Box(spacing=0,orientation=Gtk.Orientation.VERTICAL)
        png_file = get_letter_png(self.pt.lang_code, self.pt.list_07_letters_player[6])
        img = Gtk.Image.new_from_file(png_file)
        self.check_btn6 = Gtk.CheckButton()
        vbox.pack_start(self.check_btn6, False, False, 0)
        vbox.pack_start(img, False, False, 0)
        hbox.pack_end(vbox, False, False, 0)
        area.pack_start(hbox, False, False, 0)
        #---------------------------
        hbox = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_border_width(10)
        btn_change = Gtk.Button(_('Change'))
        btn_change.connect('clicked', self.change_letters)
        hbox.pack_start(btn_change, False, False, 0)
        btn_cancel = Gtk.Button(_('Cancel'))
        btn_cancel.connect('clicked', lambda *a: self.destroy())
        hbox.pack_end(btn_cancel, False, False, 0)
        area.pack_start(hbox, False, False, 0)
        #----------------------------
        self.show_all()
        
        
        
        