# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################
from os import listdir
from tools import *
from languages import *
from letters import *
import config as config
import json


def get_letter_value(lang_code, letter):
    return DICT_LETTERS[lang_code][letter][1]

def get_list_letters_repeated(lang_code):
    list_letters_repeated = []
    for letter in DICT_LETTERS[lang_code].keys():
        list_letters_repeated.extend([letter,]*DICT_LETTERS[lang_code][letter][0])
    return list_letters_repeated    

def get_stems_text(lang_code):
    try: stems_file = open(join(STEMS_DIR, '{}.stems'.format(lang_code,)), 'r')
    except: stems_file = open(join(STEMS_HOME, '{}.stems'.format(lang_code,)), 'r')
    stems_text = stems_file.read()
    stems_text_set = set(json.loads(stems_text))
    return stems_text_set

def get_database(lang_code):
    dict_name = join(DICTS_DIR, '{}.dict'.format(lang_code,))
    if not exists(dict_name):
        dict_name = join(DICTS_HOME, '{}.dict'.format(lang_code,))
    return dict_name   

def get_word_complex_letters(lang_code, word):
    for a in COMPLEX_LETTERS[lang_code].keys():
        word = word.replace(a, COMPLEX_LETTERS[lang_code][a])
    return word  


    