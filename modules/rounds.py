# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

import config as config
from tools import *
from data import *
import random, time

#===============================================================
class Rounds(object): 
    
    def __init__(self, pt):
        self.pt = pt
        object.__init__(self)
    
    #-----------------------------------------------------------
    def chose_letters_player(self, *a):
        n = 7-len(self.pt.list_07_letters_player)
        l = len(self.pt.list_letters_repeated)
        if l == 0: return
        list_new = []
        a = 0
        while a < n:
            if len(self.pt.list_letters_repeated) == 0: break
            letter = random.choice(self.pt.list_letters_repeated)
            list_new.append(letter)
            self.pt.list_07_letters_player.append(letter)
            self.pt.list_letters_repeated.remove(letter)
            a +=1
        self.pt.sideletters.add_letters(list_new)
        time.sleep(0.1)
        while (Gtk.events_pending()): Gtk.main_iteration()
        self.pt.sideinfo.sel_count_pieces(config.getn('count_pieces'))
        
    
    def slect_letter_4_empty_tile_computer(self, *a):
        for letter in DICT_LETTERS[self.pt.lang_code].keys():
            if letter not in self.pt.list_07_letters_computer and letter != '*':
                self.pt.list_07_letters_computer.append(letter)
                self.pt.computer_empty_letter.append(letter)
                return
    
    #-----------------------------------------------------------
    def chose_letters_computer(self, *a):
        n = 7-len(self.pt.list_07_letters_computer)
        l = len(self.pt.list_letters_repeated)
        if l == 0: return
        a = 0
        while a < n:
            if len(self.pt.list_letters_repeated) == 0: break
            letter = random.choice(self.pt.list_letters_repeated)
            if letter == '*': self.slect_letter_4_empty_tile_computer()
            else: self.pt.list_07_letters_computer.append(letter)
            self.pt.list_letters_repeated.remove(letter)
            a +=1
        self.pt.sideinfo.sel_count_pieces(config.getn('count_pieces'))

    def accept_word_player_added(self, list_words_player):
        for a in  self.pt.dict_new.keys():
            self.pt.dict_chequer[a] = self.pt.dict_new[a]
            if a in self.pt.cells_empty_letter: self.pt.list_07_letters_player.remove('*')
            else: self.pt.list_07_letters_player.remove(self.pt.dict_new[a])
        self.pt.add_timer(_('Well done, \n Computer role.'))
        while (Gtk.events_pending()): Gtk.main_iteration()
        self.pt.sideinfo.add_words(list_words_player, 1)
        self.pt.sideletters.set_sensitive(False)
        while (Gtk.events_pending()): Gtk.main_iteration()
        self.pt.chequer.queue_draw()
        self.pt.sideinfo.sel_count_pieces(config.getn('count_pieces'))
        self.pt.last_round_player = True
        self.pt.last_round_computer = True
        self.round_computer()
    
    #-----------------------------------------------------------
    def accept_word_computer_added(self, ls):
        for a in ls[2]:
            self.pt.has_msg = False
            play_sound('drop')
            self.pt.dict_chequer[a[0]] = a[1]
            if a[1] in self.pt.computer_empty_letter:
                self.pt.cells_empty_letter.append(a[0])
                self.pt.computer_empty_letter.remove(a[1])
            self.pt.chequer.queue_draw()
            while (Gtk.events_pending()): Gtk.main_iteration()
            time.sleep(0.1)
            self.pt.list_07_letters_computer.remove(a[1])
        self.pt.sideinfo.add_words(ls, 2)
    
    #-----------------------------------------------------------
    def is_ended(self, list_07_letters_hostile):
        l = len(self.pt.list_letters_repeated)
        l1 = len(list_07_letters_hostile)
        if l == 0 and l1 == 0:
            self.end_game()
            return True
        return False
    
    #-----------------------------------------------------------
    def count_residual_points(self, *a):
        v1 = 0
        v2 = 0
        for t1 in self.pt.list_07_letters_computer:
            if t1 in self.pt.computer_empty_letter:
                self.pt.computer_empty_letter.remove(t1)
            else:
                v1 += get_letter_value(self.pt.lang_code, t1)
        self.pt.points_computer -= v1
        for t2 in self.pt.list_07_letters_player:
            v2 += get_letter_value(self.pt.lang_code, t2)
        self.pt.points_player -= v2
    
    #-----------------------------------------------------------
    def end_game(self, *a):
        self.pt.sideletters.set_sensitive(False)
        text = _('Game over.')
        text += '\n' #-----------------------------
        if len(self.pt.list_letters_repeated) == 0:
            if len(self.pt.list_07_letters_computer) == 0: text += _('The computer does not have any pieces.')
            elif len(self.pt.list_07_letters_player) == 0: text += _('You does not have any pieces.')
            else: text += _('You can not play both.')
        else:
            text += _('You can not play both.')
        text += '\n' #-----------------------------
        self.count_residual_points()
        if self.pt.points_computer > self.pt.points_player:
            text += _('You lost, Try again.')
        if self.pt.points_computer < self.pt.points_player:
            text += _('You won, Congratulations to you.')
        if self.pt.points_computer == self.pt.points_player:
            text += _("They drew, It's okay.")
        text += '\n' #-----------------------------
        text += _('Computer Points: {}.').format(self.pt.points_computer,)
        text += '\n' #-----------------------------
        text += _('Your Points: {}.').format(self.pt.points_player,)
        self.pt.text_msg = text
        self.pt.ended = True
        config.setv('saved', 0)
        self.pt.chequer.queue_draw()
    
    #------------------------------------------------------------
    def round_player(self, *a):
        self.pt.chequer.queue_draw()
        if self.is_ended(self.pt.list_07_letters_computer): return
        self.pt.sideletters.set_sensitive(True)
        self.pt.not_words = ""
        self.pt.dict_new.clear()
        self.chose_letters_player()
    
    def select_word_computer_on_grade(self, list_words_computer):
        l = len(list_words_computer)
        h = int(l/2)
        g = config.getn('grade')
        if l >= 2:
            if g == 0: ls = list_words_computer[0]
            elif g == 1: ls = random.choice(list_words_computer[:h])
            elif g == 2: ls = list_words_computer[h]
            elif g == 3: ls = random.choice(list_words_computer[h:])
            elif g == 4: ls = list_words_computer[-1]
        else: ls = list_words_computer[0]
        return ls
    
    #------------------------------------------------------------
    def change_computer_letters(self, *a):
        if len(self.pt.list_letters_repeated) > 0:
            self.pt.list_letters_repeated.extend(self.pt.list_07_letters_computer)
            self.pt.list_07_letters_computer.clear()
            self.chose_letters_computer()
            return True
        return False
      
    #------------------------------------------------------------
    def round_computer(self, *a):
        if self.is_ended(self.pt.list_07_letters_player): return
        while (Gtk.events_pending()): Gtk.main_iteration()
        self.chose_letters_computer()
        list_words_computer = self.pt.dict_chequer.find_words_computer()
        if len(list_words_computer) == 0: 
            self.pt.add_timer(_('The computer does not have any words.'))
            if not self.change_computer_letters():
                if self.pt.last_round_player == False:
                    if len(self.pt.hd_bar.list_help_words) == 0:
                        self.end_game()
                        return
                    res = sure(self.pt, _('Computer does not have a word if you does not have a word, the game will end. \n Do you want that?'))
                    if res == -8:
                        self.end_game()
                        return
                else: self.load_words_help()
            else: self.pt.add_timer(_('The computer changed its letters.'))
            self.pt.dict_new_computer = self.pt.dict_new
            self.round_player()
            self.pt.last_round_computer = False
            return
        #------------------------------------------------------
        ls = self.select_word_computer_on_grade(list_words_computer)
        self.pt.dict_new_computer.clear()
        for a in ls[2]:
            self.pt.dict_new_computer[a[0]] = a[1]
        self.accept_word_computer_added(ls)
        #------------------------------------------------------
        time.sleep(0.01)
        while (Gtk.events_pending()): Gtk.main_iteration()
        self.round_player()
        self.pt.sideinfo.sel_count_pieces(config.getn('count_pieces'))
        self.pt.last_round_computer = True
        self.pt.last_round_player = True
        self.load_words_help()
        
        
    #a تحميل قائمة الكلمات المقترحة للاعب---------------------------
    def load_words_help(self, *a):
        list_words = self.pt.dict_chequer.get_words_help()
        self.pt.hd_bar.list_help_words.clear()
        for a in list_words:
            for b in a[1]:
                word = get_word_complex_letters(self.pt.lang_code, b[0])
                if word not in self.pt.hd_bar.list_help_words: self.pt.hd_bar.list_help_words.append(word)
        
    def round_starting(self, started_player):
        if started_player == 'player':
            self.round_player()
            while (Gtk.events_pending()): Gtk.main_iteration()
            self.load_words_help()
        else:
            self.round_computer()
        
        
        
        