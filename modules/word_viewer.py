# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

import config
from tools import *
from data import *

def show_dict(pt, ls_id):
    dlg = Gtk.Dialog(parent=pt, title=_('Dictionary'))
    #dlg.set_icon_name("asmaa")
    dlg.set_default_size(450, 300)
    area = dlg.get_content_area()
    area.set_spacing(6)
    view_info = Viewer(pt)
    view_info.set_cursor_visible(False)
    view_info.set_editable(False)
    view_info.set_right_margin(10)
    view_info.set_left_margin(10)
    view_info.set_wrap_mode(Gtk.WrapMode.WORD)
    view_info_bfr = view_info.get_buffer()
    scroll = Gtk.ScrolledWindow()
    scroll.set_shadow_type(Gtk.ShadowType.IN)
    scroll.add(view_info)
    text = '\n'
    if config.getv('language_scrabble') == 'العربية':
        for id0 in ls_id:
            pt.dict_chequer.cur.execute('SELECT * FROM dict WHERE id=?',(id0, ))
            rec0 = pt.dict_chequer.cur.fetchall()
            text += rec0[0][1]+': \n'+rec0[0][2]+'\n'
    else:
        pt.dict_chequer.cur.execute('SELECT * FROM dict WHERE term=?',(ls_id[0].lower(), ))
        rec0 = pt.dict_chequer.cur.fetchall()
        if len(rec0) > 0:  text += rec0[0][1]+': \n'+rec0[0][2]+'\n'
    view_info_bfr.set_text(text)
    view_info.with_tag(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '='])

    area.pack_start(scroll, True, True, 0)
    dlg.show_all()

#===============================================================
class Viewer(Gtk.TextView): 
     
    def select_word_textview(self,  widget, event):
        if event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
            if self.view_bfr.get_has_selection():
                sel = self.view_bfr.get_selection_bounds()
                sel_text = self.view_bfr.get_text(sel[0], sel[1],True)
                if config.getv('language_scrabble') == 'العربية': sel_text = stripTashkeel(sel_text)
                self.explanation_word(sel_text)
    
    def explanation_word(self, text):
        text = text.replace('_', '')
        text = re.sub('\d', '', text)
        ls_stems = text.split(' ')
        list_id = []
        self.pt.dict_chequer.cur.execute('SELECT * FROM dict')
        rec0 = self.pt.dict_chequer.cur.fetchall()
        if len(rec0) > 0:
            for word in ls_stems:
                self.pt.dict_chequer.cur.execute('SELECT terms FROM stems WHERE stem=?',(word, ))
                rec = self.pt.dict_chequer.cur.fetchall()
                for t in rec:
                    ls = eval(t[0])
                    for id0 in ls:
                        list_id.append(id0)
            if len(list_id) > 0:
                show_dict(self.pt, list_id)
        else:
            info(self.pt, _('There is no dictionary for this language.'))
    
    def change_theme(self, *a):
        self.text_tag.set_property('foreground', config.getv('fg_nbr')) 
        data = '''
        * {
        background-color: '''+config.getv('bg_pieces')+''';
        color: '''+config.getv('fg_pieces')+''';
        }
        #View text selection, #View:selected  {
        color: '''+config.getv('bg_pieces')+''';
        background-color: '''+config.getv('fg_pieces')+''';
        }
        '''
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(data.encode('utf8'))
        context = self.get_style_context()
        context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)        
    
    def search_and_mark(self, text, start):
        end = self.view_bfr.get_end_iter()
        match = start.forward_search(text, 0, end)
        if match != None:
            match_start, match_end = match
            self.view_bfr.apply_tag(self.text_tag, match_start, match_end)
            self.search_and_mark(text, match_end)
            
    def with_tag(self, ls):
        for text in ls:
            cursor_mark = self.view_bfr.get_insert()
            start = self.view_bfr.get_iter_at_mark(cursor_mark)
            if start.get_offset() == self.view_bfr.get_char_count():
                start = self.view_bfr.get_start_iter()
            self.search_and_mark(text, start)
    
    def __init__(self, pt):
        self.pt = pt
        Gtk.TextView.__init__(self)
        self.set_name('View')
        self.set_cursor_visible(False)
        self.set_editable(False)
        self.set_right_margin(10)
        self.set_left_margin(10)
        self.set_wrap_mode(Gtk.WrapMode.WORD)
        self.view_bfr = self.get_buffer()
        self.connect("event", self.select_word_textview)
        self.text_tag = self.view_bfr.create_tag("text_tag")
        self.text_tag.set_property('foreground', config.getv('fg_nbr')) 
        self.change_theme()
        