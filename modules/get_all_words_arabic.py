# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################


import json, sqlite3, re
from os.path import join, exists
from os import mkdir, listdir


path_verb = '/media/rr/my_prog/my_programs/myprogram/FassihGame/Arabic_Scrabble/src/archive/new_data/verbs'
path_noun = '/media/rr/my_prog/my_programs/myprogram/FassihGame/Arabic_Scrabble/src/archive/new_data/nouns'

roots_verb = join(path_verb, 'roots1')
roots_noun = join(path_noun, 'roots1')

out_verb = join(path_verb, 'out')

con = sqlite3.connect(join(path_noun, 'PatternsNom.db'))
cur = con.cursor()

#  
for f in listdir(roots_noun):
    if f != 'ق.txt': continue
    new_text = ''
    of = open(join(roots_verb, f), 'r')
    lf = of.readlines()
    for l in lf:
        if l.strip() == '': continue
        root, derivatives = l.split(':')
        for d in derivatives.split(' '):
            d = int(d)
            cur.execute("SELECT stem FROM stems WHERE id=?", (d,))
            ss = cur.fetchall()
            if len(ss) == 0: continue
            stem = ss[0][0]
            if len(root) > 2:
                stem = re.sub('ف', root[0], stem, 1)
                stem = re.sub('ع', root[1], stem, 1)
                stem = re.sub('ل', root[2], stem, 1)
            if len(root) > 3:
                stem = re.sub('ل', root[3], stem, 1)
            new_text += '{}:{}'.format(root, stem)
    wf = open(join(out_verb, f), 'w') 
    wf.write(new_text)
    wf.close()


# 
# cur.execute('CREATE TABLE IF NOT EXISTS stems (id integer primary key, stem varchar(255))')
# of = open('/media/rr/my_prog/my_programs/myprogram/FassihGame/Arabic_Scrabble/src/archive/new_data/nouns/PatternsNom.txt', 'r')
# lf = of.readlines()
# cur.execute('BEGIN;')
# for l in lf:
#     if l.strip() == '': continue
#     n, derivatives = str(l).split(':')
#     print(type(n), type(derivatives), n, derivatives)
#     cur.execute('INSERT INTO stems VALUES (?, ?)', (int(n), derivatives))
# con.commit() 
 
# rr = "drezdr"
# ff = re.sub('r', '', rr, 1)
# print(ff)
