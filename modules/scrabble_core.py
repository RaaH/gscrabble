#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################


import sqlite3
from itertools import combinations, zip_longest
from data import *
from tools import *
from araby import *
import config as config

class Dict_General(dict):
    
    def __init__(self, pt):
        dict.__init__(self)
        for a in range(225):
            self[a] = 0
        self.pt = pt
        self.list_words_cutoff = []
        self.list_words_possible = []
        self.list_07_letters = []
        self.list_words_exist = []
        self.list_cells_side = []

    def get_data(self, lang_code):
        self.stems_text_set = get_stems_text(lang_code)
        dict_file = get_database(lang_code)
        if exists(dict_file):
            self.con = sqlite3.connect(dict_file)
            self.cur = self.con.cursor()
    
    #-----------------------------------------------------------
    def clear_dict_all(self, *a):
        self.pt.dict_new.clear()
        for a in range(225):
            self[a] = 0
    
    #a إذا كانت الخانات تنتمي إلى سطر واحد متصلة ومتصلة بما قبلها-----------
    def check_line(self, *a):  
        r = 0
        
        #a البداية من خانة البداية-----------------------------------if not return: 1
        if self[112] == 0 and 112 not in self.pt.dict_new: return 1
        
        #a الكلمة لا تقل عن حرفين---------------------------------if not return: 2
        if self[112] == 0 and len(self.pt.dict_new) == 1: return 2
        
        #a على استقامة واحدة-------------------------------------if not return: 3
        ls_y = []
        ls_x = [] 
        for c in self.pt.dict_new.keys():
            ls_y.append(int(c/15))
            ls_x.append(c%15)
        if ls_y != [ls_y[0],]*len(ls_y) and ls_x != [ls_x[0],]*len(ls_x): return 3
        
        #a على اتصال------------------------------------------------if not return: 4
        if len(self.pt.dict_new) > 1:
            v_step, v_side = self.select_line()
            ls_keys = list(self.pt.dict_new.keys())
            ls_keys.sort()
            for k in range(ls_keys[0]+v_step, ls_keys[-1], v_step):
                if k not in self.pt.dict_new and self[k] == 0: return 4
                
        #a متصلة بما قبلها-------------------------------------------if not return: 5
        if self[112] != 0:
            self.get_cells_side()
            for k0 in self.pt.dict_new.keys():
                if k0 in self.list_cells_side: 
                    r = 0
                    break
                else: r = 5
                
        #---------------------------------------
        return r
    
    #a تحديد اتجاه السطر الذي تنتمي إليه الكلمة وإرجاع قيمة نقلة الحرف-------
    def select_line(self, *a): 
        if len(self.pt.dict_new) > 1:
            ls_y = []
            ls_x = []
            for c in self.pt.dict_new.keys():
                ls_y.append(int(c/15))
                ls_x.append(c%15)
            if ls_y == [ls_y[0],]*len(ls_y): return 1, 15
            elif ls_x == [ls_x[0],]*len(ls_x): return 15, 1
        else:
            c = list(self.pt.dict_new.keys())[0]
            if c+1 in list(range(225)) and self[c+1] != 0: return 1, 15
            elif c-1 in list(range(225)) and self[c-1] != 0: return 1, 15
            elif c+15 in list(range(225)) and self[c+15] != 0: return 15, 1
            elif c-15 in list(range(225)) and self[c-15] != 0: return 15, 1
    
    #a إذا كانت الخانة فارغة وبجانبها خانة ملأى------------------------------------   
    def check_cells(self, now_cell):
        for e in self.pt.dict_new.keys(): 
            if now_cell == e: return False
        if now_cell not in self.keys():  return False
        if self[now_cell] != 0: return False
        if now_cell > 14:
            if self[now_cell-15] != 0: return True
        if now_cell < 210:
            if self[now_cell+15] != 0: return True
        if int(now_cell%15) < 14:
            if self[now_cell+1] != 0: return True
        if int(now_cell%15) > 0:
            if self[now_cell-1] != 0: return True
        for e in self.pt.dict_new.keys(): 
            if e > 14:
                if e-15 == now_cell: return True
            if e < 210:
                if e+15 == now_cell: return True
            if int(e%15) < 14:
                if e+1 == now_cell: return True
            if int(e%15) > 0:
                if e-1 == now_cell: return True
        return False
    
    #a ارجاع جميع الخانات المجاورة للخانات الملأى------------------------------------   
    def get_cells_side(self, *a):
        self.list_cells_side.clear()
        for cell in self.keys():
            if self[cell] != 0: continue
            if cell > 14:
                if self[cell-15] != 0: 
                    if cell not in self.list_cells_side: self.list_cells_side.append(cell)
                    continue
            if cell < 210:
                if self[cell+15] != 0: 
                    if cell not in self.list_cells_side: self.list_cells_side.append(cell)
                    continue
            if int(cell%15) < 14:
                if self[cell+1] != 0: 
                    if cell not in self.list_cells_side: self.list_cells_side.append(cell)
                    continue
            if int(cell%15) > 0:
                if self[cell-1] != 0: 
                    if cell not in self.list_cells_side: self.list_cells_side.append(cell)
                    continue

    #a إرجاع قيمة كلمة-----------------------------------------------------------
    def count_word(self, ls_new, ls, is_computer=0, main_word=0):
        kx = 1
        value = 0
        for l in ls:
            v = get_letter_value(self.pt.lang_code, l[0])
            if l[0] in self.pt.computer_empty_letter and is_computer == 1: v = 0
            if l[1] in self.pt.cells_empty_letter: v = 0
            if l[1] not in ls_new:  v = v
            else:
                if l[1] not in DICT_SPECIAL_CELLS.keys(): v = v
                elif DICT_SPECIAL_CELLS[l[1]] == 0: kx  = kx*2
                elif DICT_SPECIAL_CELLS[l[1]] == 1: v   = v*2
                elif DICT_SPECIAL_CELLS[l[1]] == 2: v   = v*3
                elif DICT_SPECIAL_CELLS[l[1]] == 3: kx = kx*2
                elif DICT_SPECIAL_CELLS[l[1]] == 4: kx = kx*3
            value += v
        value = value*kx
        if len(ls_new) == 7 and main_word == 1: value += 50
        return value

    #a معالجة كلمة معترضة---------------------------------------------------
    def side_word(self, ls_new, idx, letter, v_side, is_computer=0, main_word=0):
        ls_letters = [letter,]
        ls_indexes =[idx,]
        i = int(int(idx/v_side)%15)
        i0 = idx-(i*v_side)
        i1 = idx+((14-i)*v_side)
        for b in range(idx-v_side, i0-1, -1*v_side):
            if self[b] != 0: 
                ls_letters.insert(0, self[b])
                ls_indexes.insert(0, b)
            elif b in self.pt.dict_new.keys():
                ls_letters.insert(0, self.pt.dict_new[b])
                ls_indexes.insert(0, b)
            else: break
        for b in range(idx+v_side, i1+1, v_side):
            if self[b] != 0: 
                ls_letters.append(self[b])
                ls_indexes.append(b)
            elif b in self.pt.dict_new.keys():
                ls_letters.append(self.pt.dict_new[b])
                ls_indexes.append(b)
            else: break
        if len(ls_letters) == 1:
            return []
        word1 = ''.join(ls_letters)
        nw1 = False
        if word1 in self.stems_text_set:
            ls_word = list(zip_longest(ls_letters, ls_indexes))
            value = self.count_word(ls_new, ls_word, is_computer, main_word)
            ls_side_word = [value, [word1, value]]
            return ls_side_word
        elif Gtk.Widget.get_default_direction() == Gtk.TextDirection.RTL: 
            nw1 = True
        else: 
            return None
        ls_letters.reverse()
        ls_indexes.reverse()
        word2 = ''.join(ls_letters)
        if word2 in self.stems_text_set:
            ls_word = list(zip_longest(ls_letters, ls_indexes))
            value = self.count_word(ls_new, ls_word, is_computer, main_word)
            ls_side_word = [value, [word2, value]]
            return ls_side_word
        else: 
            if nw1:
                self.pt.not_words = word2+' '+word1+' '
        return None
        
    #a معالجة الكلمة الرئيسة---------------------------------------------------
    def main_word(self, word, ls_new, ls_indexes, v_side):
        ls_word = list(zip_longest(list(word),ls_indexes))
        value = self.count_word(ls_new, ls_word, 1, 1)
        ls_word_terminal = [value, [[word, value]]]
        dict_new = []
        for idx in ls_new:
            i = ls_indexes.index(idx, )
            letter = ls_word[i][0]
            dict_new.append([idx, letter])
            ls_side_word = self.side_word(ls_new, idx, letter, v_side, 1, 0)
            if ls_side_word != None: 
                if len(ls_side_word) > 0:
                    ls_word_terminal[0] += ls_side_word[0]
                    ls_word_terminal[1].append(ls_side_word[1])
            else: return None
        ls_word_terminal.append(dict_new)
        return ls_word_terminal
    
    #a معالجة كلمات موضع محدد----------------------------------------------------
    def treat_words_index(self, word_re, ls_words, ls_new, ls_indexes, v_side):
        for word in ls_words:
            m = re.match(word_re, word)
            if m != None:
                ls_word_terminal = self.main_word(word, ls_new, ls_indexes, v_side)
                if ls_word_terminal != None:
                    self.list_words_exist.append(ls_word_terminal)
    
    #a إذا كانت الكلمة متصلة----------------------------------------------------
    def is_connected(self, start, long, n_line, v_step, v_side):
        idx_start = start*v_step + n_line*v_side
        idx_end = (start+long)*v_step + n_line*v_side
        idxs = list(range(idx_start, idx_end, v_step))
        for i in idxs:
            if list(self.values()) == [0,]*225 and i == 112: return True
            if i in self.list_cells_side: return True
        return False
    
    #a استخراج الكلمات ذات نفس الطول من سطر واحد---------------------------
    def words_with_long_line(self, ls , long, line, n_line, v_step, v_side):
        o = len(ls)
        ls2 = list(ls)
        for b in range(15):
            if b+long < 15: pass
            else: continue
            if b > 0 and line[b-1] != 0: continue
            else: pass
            if line[b:b+long].count(0) == o: pass
            else: continue
            if b+long <= 14 and line[b+long] != 0: continue
            else: pass
            if self.is_connected(b, long, n_line, v_step, v_side): pass
            else: continue
            s=0;ls_indexes=[];ls_new=[];ls_cutoff=[];word_re='';
            for v in range(b,b+long):
                ls_indexes.append(v*v_step + n_line*v_side)
                if line[v] == 0:
                    word_re += '\w'
                    ls_cutoff.append(ls2[s])
                    ls_new.append(v*v_step + n_line*v_side)
                    s += 1
                else:
                    word_re += line[v]
                    ls_cutoff.append(line[v])
            ls_cutoff.sort()
            word_cutoff = ''.join(ls_cutoff) 
            self.cur.execute('''SELECT terms FROM cutoff WHERE letters=?''', (word_cutoff,))
            rs = self.cur.fetchall()
            if len(rs) > 0: 
                self.treat_words_index(word_re, eval(rs[0][0]),ls_new, ls_indexes, v_side)
    
    #a معالجة سطر واحد---------------------------------------------------
    def treat_line(self, line, n_line, v_step, v_side):
        for long in range(2, 16):
            for o in range(1, 8):
                ls_combinations = combinations(self.list_07_letters, o)
                for ls in list(ls_combinations):
                    self.words_with_long_line(ls, long, line, n_line, v_step, v_side)
    
    #a إرجاع قائمة بمحتوى العمود---------------------------------------------------
    def get_column(self, v):
        if list(self.values()) == [0,]*225 and v == 7: return [0,]*15
        column = []
        column1 = []
        column2 = []
        if v < 14:
            for c1 in range(v+1, v+226, 15): 
                if self[c1] != 0:
                    column1.append(self[c1])
        if v > 0:
            for c2 in range(v-1, v+224, 15): 
                if self[c2] != 0:
                    column2.append(self[c2])
        for c in range(v, v+225, 15): column.append(self[c])
        if column1 == [] and column2 == [] and column == [0,]*15: return None
        return column
     
    #a إرجاع قائمة بمحتوى السطر----------------------------------------------------
    def get_row(self, v):
        if list(self.values()) == [0,]*225 and v == 7: return [0,]*15
        row = []
        row1 = []
        row2 = []
        if v < 14:
            for c1 in range((v+1)*15, (v+2)*15): 
                if self[c1] != 0:
                    row1.append(self[c1])
        if v > 0:
            for c2 in range((v-1)*15, v*15): 
                if self[c2] != 0:
                    row2.append(self[c2])
        for c in range(v*15, (v+1)*15): row.append(self[c])
        if row1 == [] and row2 == [] and row == [0,]*15: return None
        return row

    #-----------------------------------------------------------
    def find_words_computer(self, *a):
        self.list_words_exist.clear()
        self.list_07_letters = self.pt.list_07_letters_computer
        self.get_cells_side()
        for n_line in range(15):
            column = self.get_column(n_line)
            if column != None: self.treat_line(column, n_line, 15, 1)
            row = self.get_row(n_line)
            if row != None: self.treat_line(row, n_line, 1, 15) 
        self.list_words_exist.sort()
        return self.list_words_exist
    
    def get_words_help(self, *a):
        self.list_words_exist.clear()
        self.list_07_letters = self.pt.list_07_letters_player
        self.get_cells_side()
        for n_line in range(15):
            column = self.get_column(n_line)
            if column != None: self.treat_line(column, n_line, 15, 1)
            row = self.get_row(n_line)
            if row != None: self.treat_line(row, n_line, 1, 15) 
        return self.list_words_exist
    
    #-----------------------------------------------------------
    def main_word_player(self, *a):
        ls_new = list(self.pt.dict_new.keys())
        idx = ls_new[0]
        letter = self.pt.dict_new[idx]
        v_step, v_side = self.select_line()
        #a إيجاد الكلمة الرئيسية--------------
        ls_word_terminal = [0, []]
        ls_side_word = self.side_word(ls_new, idx, letter, v_step, 0, 1)
        if ls_side_word != None: 
                if len(ls_side_word) > 0:
                    ls_word_terminal[0] += ls_side_word[0]
                    ls_word_terminal[1].append(ls_side_word[1])
        else: return None
        #a إيجاد الكلمات الجانبية--------------
        for idx in ls_new:
            letter = self.pt.dict_new[idx]
            ls_side_word = self.side_word(ls_new, idx, letter, v_side, 0, 0)
            if ls_side_word != None: 
                if len(ls_side_word) > 0:
                    ls_word_terminal[0] += ls_side_word[0]
                    ls_word_terminal[1].append(ls_side_word[1])
            else: return None
        return ls_word_terminal
    
    #-----------------------------------------------------------
    def find_words_player(self, *a):
        self.list_07_letters = self.pt.list_07_letters_player
        list_words = self.main_word_player()
        return list_words


