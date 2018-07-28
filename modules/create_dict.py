# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################


import json, sqlite3, os.path
from tools import *
from letters import *


def create_dict_language(progressbar, lang_code, file_source):
    con = sqlite3.connect(os.path.join(DICTS_HOME, '{}.dict'.format(lang_code, )))
    cur = con.cursor()
    f = open(file_source, 'r')
    list_words = f.readlines()
    #==========================================
    cur.execute('BEGIN;')
    s = 0
    len_list = len(list_words)
    for a in list_words:
        while (Gtk.events_pending()): Gtk.main_iteration()
        progressbar.set_fraction(s/len_list)
        progressbar.set_text(str(s)+' : '+str(len_list))
        progressbar.set_show_text(True)
        if a.strip() == '': continue
        s += 1
        try: word, explanation = a.split('=')
        except: word, explanation = a.replace('=', ''), ''
        cur.execute('INSERT INTO dict VALUES (?, ?, ?)', (s, word.strip().lower(), explanation.strip().lower()))
    con.commit() 

def create_db_language(progressbar, lang_code):
    list_cutoff = []
    con = sqlite3.connect(os.path.join(DICTS_HOME, '{}.dict'.format(lang_code, )))
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS stems (id integer primary key, stem varchar(255), terms varchar(255))')
    cur.execute('CREATE TABLE IF NOT EXISTS dict (id integer primary key, term varchar(255), charh varchar(255))')
    cur.execute('CREATE TABLE IF NOT EXISTS cutoff (letters varchar(255) primary key, terms varchar(255))')
    #==========================================
    try: stems_file = open(join(STEMS_DIR, '{}.stems'.format(lang_code,)), 'r')
    except: stems_file = open(join(STEMS_HOME, '{}.stems'.format(lang_code,)), 'r')
    stems_text = stems_file.read()
    stems_text_set = set(json.loads(stems_text))
    cur.execute('BEGIN;')
    s = 0
    len_list = len(stems_text_set)
    for a in stems_text_set:
        while (Gtk.events_pending()): Gtk.main_iteration()
        progressbar.set_fraction(s/len_list)
        progressbar.set_text(str(s)+' : '+str(len_list))
        progressbar.set_show_text(True)
        s += 1
        l = list(a)
        l.sort()
        cutoff = ''.join(l)
        cur.execute('INSERT INTO stems VALUES (?, ?, ?)', (s, a, repr([a,])))
        if cutoff not in list_cutoff:
            list_cutoff.append(cutoff)
            cur.execute('INSERT INTO cutoff VALUES (?, ?)', (cutoff, repr([a,])))
        else:
            cur.execute("SELECT terms FROM cutoff WHERE letters=?", (cutoff,))
            r = cur.fetchall()[0][0]
            rr = eval(r)
            rr.append(a)
            cur.execute('UPDATE  cutoff SET terms=? WHERE letters = ?', (repr(rr), cutoff))
    con.commit() 

def create_stems_language(progressbar, lang_code, file_source):
    open_file = open(file_source, 'r')
    text = open_file.read()
    for cl in COMPLEX_LETTERS[lang_code].keys():
        text = text.replace(COMPLEX_LETTERS[lang_code][cl], cl)
    list_text = text.split('\n')
    new_list = '['
    for word in list_text:
        word = word.strip()
        if word == '': continue
        word = word.upper()
        new_list += '"'+word+'", \n'
    new_list += ']'
    new_list = new_list.replace(', \n]', ']')
    stems_file = open(join(STEMS_HOME, '{}.stems'.format(lang_code,)), 'w')
    stems_file.write(new_list)
    stems_file.close()
    create_db_language(progressbar, lang_code)    
    
    