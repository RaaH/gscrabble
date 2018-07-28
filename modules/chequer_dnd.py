# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

import config as config
from tools import *
from data import *
from chequer_draw import DrawArea

#===============================================================
class Chequer(DrawArea):
    
    def __init__(self, pt):
        self.pt = pt
        self.build()
    
    #a تحديد الرقعة لوضع حرف----------------------------------------------
    def valid_chequer(self, x, y):
        if int(x) in range(int(self.st), int(self.st+self.bwn*15)) and int(y) in range(int(self.br), int(self.br+self.bwn*15)):
            return True
        return False
    
    #a تحديد الخانة المناسبة لوضع حرف----------------------------------------------
    def valid_cell(self, x, y):
        if self.valid_chequer(x, y):
            y0 = int((y-self.br)/self.bwn)
            x0 = int((x-self.st)/self.bwn)
            n_cell = y0*15+x0
            if n_cell not in self.pt.dict_new.keys() and self.pt.dict_chequer[n_cell] == 0:
                self.pt.now_cell = y0*15+x0
                return True
        return False
        
    #a تحديد الخانة الموضوع فيها حرف غير مثبت ----------------------------------------------
    def new_cell(self, x, y):
        y0 = int((y-self.br)/self.bwn)
        x0 = int((x-self.st)/self.bwn)
        n_cell = y0*15+x0
        if n_cell in self.pt.dict_new.keys():
            return n_cell
        return None
    
    def chose_letter(self, btn):
        letter = btn.get_name()
        play_sound('drop')
        self.dict_new[self.pt.now_cell] = letter
        model = self.pt.sideletters.liststore_letters_player
        try: model.foreach(self.rm_item_in_store)
        except: pass
        self.pt.cells_empty_letter.append(self.pt.now_cell)
    
    def dialog_chose_letter(self, *a):
        dlg = Gtk.Dialog(parent=self.pt, title=_('Select a letter for the blank piece.'))
        dlg.set_default_size(450, 300)
        area = dlg.get_content_area()
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(12)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        s = 0
        ls_letters = list(DICT_LETTERS[self.pt.lang_code].keys())
        ls_letters.sort()
        for letter in ls_letters:
            if letter != '*':
                s += 1
                button = Gtk.Button(get_word_complex_letters(self.pt.lang_code, letter))
                button.set_name(letter)
                button.connect('clicked', self.chose_letter)
                button.connect('clicked', lambda *a: dlg.destroy())
                flowbox.add(button)
        scrolled.add(flowbox)
        area.pack_start(scrolled, True, True, 0)
        dlg.show_all()
     
    def set_letter_in_cell(self, ev):
        items = self.pt.sideletters.get_selected_items() 
        if len(items) > 0:
            selected_path = items[0]
            selected_iter = self.pt.sideletters.get_model().get_iter(selected_path)
            selected_letter = self.pt.sideletters.get_model().get_value(selected_iter, 1)
            self.pt.now_letter = selected_letter.replace('"', '').replace("'", "")
            if self.pt.now_letter == '*':
                self.dialog_chose_letter(selected_iter)
            else:
                play_sound('drop')
                self.dict_new[self.pt.now_cell] = self.pt.now_letter
                self.pt.sideletters.get_model().remove(selected_iter)
        else:
            self.show_letters_popover(ev)
    
    #a إذا كانت إحدى الخانتين ذات قطعة فارغة-------------------
    def change_place_blank_tile(self, cell1, cell2):
        if cell1 in self.pt.cells_empty_letter and cell2 in self.pt.cells_empty_letter:
            pass
        elif cell1 in self.pt.cells_empty_letter:
            self.pt.cells_empty_letter.append(cell2)
            self.pt.cells_empty_letter.remove(cell1)
        elif cell2 in self.pt.cells_empty_letter:
            self.pt.cells_empty_letter.append(cell1)
            self.pt.cells_empty_letter.remove(cell2)
            
    #----------------------------------------------------------- 
    def swap_pieces(self, cell, n):
        #a إذا كانت الخانة الجديدة مشغولة----------------
        if n == 1: 
            if self.pt.select_cell == None:
                self.pt.select_cell = cell
            else:
                self.change_place_blank_tile(self.pt.select_cell, cell)
                letter1 = self.pt.dict_new[self.pt.select_cell]
                letter2 = self.pt.dict_new[cell]
                self.pt.dict_new[self.pt.select_cell] = letter2
                self.pt.dict_new[cell] = letter1
                self.pt.select_cell = None
        #a إذا كانت الخانة الجديدة فارغة--------------------
        else: 
            if self.pt.select_cell != None:
                self.change_place_blank_tile(self.pt.select_cell, self.pt.now_cell)
                letter1 = self.pt.dict_new[self.pt.select_cell]
                del self.pt.dict_new[self.pt.select_cell]
                self.pt.dict_new[self.pt.now_cell] = letter1
                self.pt.select_cell = None
    
    def rm_item_in_store(self, model, path, i):
        letter = model.get(i,1)[0]
        if letter.replace('"', '').replace("'", "") == self.pt.now_letter: 
            model.remove(i)
            return True 
        else:
            return False
     
    def set_letter_popover(self, btn, pop): 
        pop.hide()
        self.pt.now_letter = btn.get_name().replace('"', '').replace("'", "")
        if self.pt.now_letter == '*':
            self.dialog_chose_letter()
        else:
            play_sound('drop')
            self.dict_new[self.pt.now_cell] = self.pt.now_letter
            model = self.pt.sideletters.liststore_letters_player
            try: model.foreach(self.rm_item_in_store)
            except: pass
        self.queue_draw()

     
    def show_letters_popover(self, ev): 
        if self.pt.ended: return
        #----------------------------------------------
        list_07_letters_player = self.pt.list_07_letters_player.copy()
        for c in self.pt.dict_new.keys():
            if c in self.pt.cells_empty_letter: list_07_letters_player.remove('*')
        for v in self.pt.dict_new.values():
            if v in list_07_letters_player: list_07_letters_player.remove(v)
        if  len(list_07_letters_player) == 0: return
        #----------------------------------------------
        pop = Gtk.Popover()
        pop.set_relative_to(self)
        rect = pop.get_pointing_to()[1]
        rect.x = ev.x-self.w/2
        if ev.y < self.bwn+self.br: 
            rect.y = self.bwn+self.br-2
            n = 8
        else: 
            rect.y = ev.y
            n = 4
        pop.set_pointing_to(rect)
        pop.set_position(Gtk.PositionType.TOP)
        #----------------------------------------------
        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(n)
        flowbox.set_min_children_per_line(n)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        for letter in list_07_letters_player:
            btn = Gtk.Button(get_word_complex_letters(self.pt.lang_code, letter))
            btn.set_name(letter)
            btn.connect('clicked', self.set_letter_popover, pop)
            flowbox.add(btn)
        clo = Gtk.Button('ألغ')
        clo.connect('clicked', lambda *a: pop.hide())
        flowbox.add(clo)
        pop.add(flowbox)
        pop.show_all()
     
    #-----------------------------------------------------------
    def drag_motion_cb(self, widget, cn, x, y, time):
        b = self.valid_cell(x, y)
        if b: self.no_drop = False
        else: self.no_drop = True
        self.queue_draw()
        return True
    
    #-----------------------------------------------------------
    def button_press_scrabble(self, widget, ev):
        new_cell = self.new_cell(ev.x, ev.y)
        valid_chequer = self.valid_chequer(ev.x, ev.y)
        valid_cell = self.valid_cell(ev.x, ev.y)
        if self.pt.has_msg:
            self.pt.has_msg  = False
        elif valid_chequer:
            #a الضغط بيسار الفأرة--------------------------
            if ev.button == 1:
                if valid_cell:
                    if self.pt.select_cell == None: self.set_letter_in_cell(ev)
                    else: self.swap_pieces(new_cell, 0)
                elif new_cell != None:
                    self.swap_pieces(new_cell, 1)
                else:
                    self.pt.select_cell = None
                    
            #a الضغط بيمين الفأرة--------------------------
            elif ev.button == 3:
                if new_cell != None:
                    self.pt.sideletters.undo_added(new_cell)
                    self.pt.select_cell = None
                    #elif valid_cell:
                    #  self.show_letters_popover(ev)
        self.queue_draw()

    #-----------------------------------------------------------
    def motion_notify_cb(self, widget, ev):
        if ev.x < 7 and config.getn('autohide_info') == 1 and self.pt.sideinfo.get_no_show_all():
            self.pt.sideinfo.set_no_show_all(False)
            self.pt.sideinfo.show_all()
        elif ev.x > 7 and config.getn('autohide_info') == 1 and not self.pt.sideinfo.get_no_show_all():
            self.pt.sideinfo.set_no_show_all(True)
            self.pt.sideinfo.hide()
        #-------------------------------------------------------------------------------
        if ev.x > self.w-7 and config.getn('autohide_letters') == 1 and self.pt.vb_letters.get_no_show_all():
            self.pt.vb_letters.set_no_show_all(False)
            self.pt.vb_letters.show_all()
        elif ev.x < self.w-7 and config.getn('autohide_letters') == 1 and not self.pt.vb_letters.get_no_show_all():
            self.pt.vb_letters.set_no_show_all(True)
            self.pt.vb_letters.hide()
        

    #-----------------------------------------------------------
    def drag_leave_cb(self, widget, cn, time):
        selected_path = self.pt.sideletters.get_selected_items()[0]
        selected_iter = self.pt.sideletters.get_model().get_iter(selected_path)
        selected_letter = self.pt.sideletters.get_model().get_value(selected_iter, 1)
        self.pt.now_letter = selected_letter.replace('"', '').replace("'", "")
        if self.no_drop == False:
            self.set_letter_in_cell(selected_iter)
            self.queue_draw()
        self.no_drop = False
        return True
    
    def build(self, *a):
        DrawArea.__init__(self, self.pt)
        self.set_events(Gdk.EventMask.EXPOSURE_MASK
         | Gdk.EventMask.LEAVE_NOTIFY_MASK
         | Gdk.EventMask.BUTTON_PRESS_MASK
         | Gdk.EventMask.POINTER_MOTION_MASK
         | Gdk.EventMask.POINTER_MOTION_HINT_MASK)
        self.connect("drag_motion", self.drag_motion_cb)
        self.connect("drag_leave", self.drag_leave_cb)
        self.connect("button-press-event", self.button_press_scrabble)
        self.connect("motion-notify-event", self.motion_notify_cb)
       
        
        