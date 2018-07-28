# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import PangoCairo, Pango
import config as config
from tools import *
from data import *

#===============================================================
class DrawArea(Gtk.DrawingArea):
    
    def __init__(self, pt):
        Gtk.DrawingArea.__init__(self)
        self.connect('draw', self.on_draw)
        self.pt = pt
        self.br = 12
        self.dict_new = self.pt.dict_new
        self.dict_all = self.pt.dict_chequer
        self.no_drop = False
        self.show_all()

    #-----------------------------------------------------------
    def coloring_special_cell(self, cr, cell, special):
        ls = [(_('Start'),config.getv('bg_start')),(_('DLS'),config.getv('bg_hX2')),(_('TLS'),config.getv('bg_hX3')),
              (_('DWS'),config.getv('bg_kX2')),(_('TWS'),config.getv('bg_kX3'))]
        x = int(cell%15)
        y = int(cell/15)
        x0 = self.st+(x*self.bwn)
        y0 = self.br+(y*self.bwn)
        text = ls[special][0]
        #--bg--#
        cr.rectangle(x0, y0, self.bwn, self.bwn)
        R, G, B = rgb(ls[special][1])
        cr.set_source_rgba(R, G, B, 1.0)
        cr.fill()
        #--text--#
        szfont, fmfont = split_font(config.getv('font_special'))
        font = '{} {}'.format(fmfont, int((self.bwn/64)*int(szfont)))
        layout = PangoCairo.create_layout(cr)
        layout.set_text(text, -1)
        desc = Pango.font_description_from_string (font)
        layout.set_font_description(desc)
        layout.set_alignment(1)
        cr.save ()
        w, h = layout.get_pixel_size()
        PangoCairo.update_layout (cr, layout)
        R, G, B = rgb(config.getv('fg_cell'))
        cr.set_source_rgb(R, G, B)
        cr.move_to(x0+(self.bwn-w)/2, y0+(self.bwn-h)/2)
        PangoCairo.show_layout(cr, layout)
        cr.restore()
    
    #-----------------------------------------------------------
    def coloring_no_drop(self, cr):
        cr.rectangle(0, 0, self.w, self.h)
        R, G, B = rgb(config.getv('bg_area'))
        cr.set_source_rgba(R, G, B, 0.4)
        cr.clip()
        cr.paint()
    
    #-----------------------------------------------------------
    def coloring_background(self, cr):
        cr.rectangle(0, 0, self.w, self.h)
        R, G, B = rgb(config.getv('bg_area'))
        cr.set_source_rgba(R, G, B, 1.0)
        cr.clip()
        cr.paint()
        #--------------
        cr.move_to(self.w, 0)
        cr.line_to(self.w, self.h)
        cr.set_line_width(1)
        cr.set_source_rgba(0.0, 0.0, 0.0, 0.6)
        cr.stroke()
        #--------------
        cr.move_to(0, 0)
        cr.line_to(0, self.h)
        cr.set_line_width(1)
        cr.set_source_rgba(0.0, 0.0, 0.0, 0.6)
        cr.stroke()
        #--------------
        cr.rectangle(self.st-2, self.br-2, self.h1+4, self.h1+4)
        R, G, B = rgb(config.getv('br_grid'))
        cr.set_source_rgba(R, G, B, 1.0)
        cr.clip()
        cr.paint()
        #--------------
        cr.rectangle(self.st, self.br, self.h1, self.h1)
        R, G, B = rgb(config.getv('bg_grid'))
        cr.set_source_rgba(R, G, B, 1.0)
        cr.clip()
        cr.paint()
        for a in DICT_SPECIAL_CELLS.keys():
            self.coloring_special_cell(cr, a, DICT_SPECIAL_CELLS[a])
    
    #-----------------------------------------------------------
    def draw_text(self, cr):
        text = ''
        if self.pt.has_msg: text = self.pt.text_msg
        elif self.pt.ended: text = self.pt.text_msg
        if text == '': return
        layout = PangoCairo.create_layout(cr)
        layout.set_text(text, -1)
        desc = Pango.font_description_from_string (config.getv('font_msg'))
        layout.set_font_description( desc)
        cr.save ()
        w, h = layout.get_pixel_size()
        #--bg--#
        cr.rectangle((self.w-w)/2-100, (self.h-h)/2-50, w+200, h+100)
        R, G, B = rgb(config.getv('bg_start'))
        cr.set_source_rgba(R, G, B, 1.0)
        cr.fill()
        #--text--#
        PangoCairo.update_layout (cr, layout)
        R, G, B = rgb(config.getv('fg_msg'))
        cr.set_source_rgb(R, G, B)
        cr.move_to((self.w-w)/2, (self.h-h)/2)
        PangoCairo.show_layout(cr, layout)
        cr.restore()
        
    #-----------------------------------------------------------
    def draw_letter(self, cr, letter, x, y, is_new):
        PF = self.bwn/20
        ls = [config.getv('bg_start'), config.getv('bg_hX2'), config.getv('bg_hX3'),
              config.getv('bg_kX2'), config.getv('bg_kX3')]
        x0 = self.st+(x*self.bwn)
        y0 = self.br+(y*self.bwn)
        cell = y*15+x
        #--bg--#
        cr.rectangle(x0, y0, self.bwn, self.bwn)
        if is_new: R, G, B = rgb(config.getv('bg_no_install'))
        elif cell in self.pt.dict_new_computer: R, G, B = rgb(config.getv('bg_last_word'))
        else: R, G, B = rgb(config.getv('bg_pieces'))
        cr.set_source_rgba(R, G, B, 1.0)
        cr.fill()
        #--border--#
        cr.rectangle(x0, y0, self.bwn, self.bwn)
        R, G, B = rgb(config.getv('br_pieces'))
        cr.set_source_rgba(R, G, B, 1.0)
        cr.set_line_width(1.0)
        cr.stroke()
        if letter in COMPLEX_LETTERS[self.pt.lang_code].keys():
            letter1 = COMPLEX_LETTERS[self.pt.lang_code][letter]
        else:
            letter1 = letter
        if self.pt.lang_code == 'ar':
            #--special-cell--#
            if cell in DICT_SPECIAL_CELLS.keys():
                special = DICT_SPECIAL_CELLS[y*15+x]
                R, G, B = rgb(ls[special])
                cr.set_source_rgba(R, G, B, 1.0)
                cr.rectangle(x0+1, y0+1, self.bwn/3, self.bwn/3)
                cr.fill()
            #--letter--#
            letter1 = letter.replace('ه', 'هـ')
            szfont, fmfont = split_font(config.getv('font_pieces'))
            font = '{} {}'.format(fmfont, int(PF*int(szfont)))
            layout = PangoCairo.create_layout(cr)
            layout.set_text(letter1, -1)
            desc = Pango.font_description_from_string (font)
            layout.set_font_description(desc)
            layout.set_alignment(1)
            cr.save ()
            w1, h1 = layout.get_pixel_size()
            PangoCairo.update_layout (cr, layout)
            if cell in self.pt.cells_empty_letter: R, G, B = rgb(config.getv('fg_nbr'))
            else: R, G, B = rgb(config.getv('fg_pieces'))
            cr.set_source_rgba(R, G, B, 1.0)
            cr.move_to(x0+(self.bwn-w1)/2, y0-(h1-self.bwn)/2-(h1/6))
            PangoCairo.show_layout(cr, layout)
            cr.restore()
            #--number--#
            cr.set_font_size (PF/2*int(szfont))
            R, G, B = rgb(config.getv('fg_nbr'))
            cr.set_source_rgba(R, G, B, 1.0)
            cr.move_to(x0+(self.bwn/20), (y0+self.bwn)-(self.bwn/20))
            if cell in self.pt.cells_empty_letter: cr.show_text ('0')
            else: cr.show_text (str(get_letter_value(self.pt.lang_code, letter)))
        else:
            #--special-cell--#
            if cell in DICT_SPECIAL_CELLS.keys():
                special = DICT_SPECIAL_CELLS[y*15+x]
                R, G, B = rgb(ls[special])
                cr.set_source_rgba(R, G, B, 1.0)
                cr.rectangle(x0+(2*self.bwn/3)-1, y0+1, self.bwn/3, self.bwn/3)
                cr.fill()
            #--letter--#
            szfont, fmfont = split_font(config.getv('font_pieces'))
            font = '{} {}'.format(fmfont, int(PF*int(szfont)))
            layout = PangoCairo.create_layout(cr)
            layout.set_text(letter1, -1)
            desc = Pango.font_description_from_string (font)
            layout.set_font_description(desc)
            layout.set_alignment(1)
            cr.save ()
            w, h = layout.get_pixel_size()
            PangoCairo.update_layout (cr, layout)
            if cell in self.pt.cells_empty_letter: R, G, B = rgb(config.getv('fg_nbr'))
            else: R, G, B = rgb(config.getv('fg_pieces'))
            cr.set_source_rgba(R, G, B, 1.0)
            cr.move_to(x0+(3*(self.bwn-w)/8), y0+(self.bwn-h)/2-(self.bwn/20))
            PangoCairo.show_layout(cr, layout)
            cr.restore()
            #--number--#
            cr.set_font_size (int(PF/2*int(szfont)))
            R, G, B = rgb(config.getv('fg_nbr'))
            cr.set_source_rgba(R, G, B, 1.0)
            xb, yb, w, h, xa, ya = cr.text_extents(str(get_letter_value(self.pt.lang_code, letter)))#xbearing, ybearing, width, height, xadvance, yadvance
            cr.move_to(x0+self.bwn-xa-(self.bwn/20), (y0+self.bwn)-(self.bwn/20))
            if cell in self.pt.cells_empty_letter: cr.show_text ('0')
            else: cr.show_text (str(get_letter_value(self.pt.lang_code, letter)))
        #-------------------------------------------
        if self.pt.select_cell == cell:
            cr.rectangle(x0, y0, self.bwn, self.bwn)
            R, G, B = rgb(config.getv('br_pieces'))
            cr.set_source_rgba(R, G, B, 1.0)
            cr.set_line_width(4.0)
            cr.stroke()
 
    #-----------------------------------------------------------
    def draw_all_letters(self, cr):
        for a in self.dict_all.keys():
            if self.dict_all[a] != 0:
                letter = self.dict_all[a]
                x = int(a%15)
                y = int(a/15)
                self.draw_letter(cr, letter, x, y, 0)
        for cell1 in self.pt.dict_new.keys():
            letter1 = self.pt.dict_new[cell1]
            x1 = int(cell1%15)
            y1 = int(cell1/15)
            self.draw_letter(cr, letter1, x1, y1, 1)
    
    #----------------------------------------------------------- 
    def draw_lines(self, cr):
        #-- V lines --#
        for e in range(16):
            y1 = self.br
            y2 = self.h1+self.br
            x = self.st+(e*self.bwn)
            cr.move_to(x, y1)
            cr.line_to(x, y2)
            cr.set_line_width(config.getf('br_thick'))
            R, G, B = rgb(config.getv('bg_lines'))
            cr.set_source_rgba(R, G, B, 1.0)
            cr.stroke()
        #-- H lines --#
        for e in range(16):
            x1 = self.st
            x2 = self.h1+self.st
            y = self.br+(e*self.bwn)
            cr.move_to(x1, y)
            cr.line_to(x2, y)
            cr.set_line_width(config.getf('br_thick'))
            R, G, B = rgb(config.getv('bg_lines'))
            cr.set_source_rgba(R, G, B, 1.0)
            cr.stroke()
    
    #-----------------------------------------------------------
    def on_draw(self, widget, cr):
        self.cr = cr
        self.w = self.get_allocated_width()
        self.h = self.get_allocated_height()
        self.h1 = self.h-(self.br*2)
        self.st = (self.w-self.h1)/2
        self.bwn = (self.h1)/15
        self.coloring_background(cr)
        self.draw_lines(cr)
        self.draw_all_letters(cr)
        self.draw_text(cr)
        if self.no_drop: self.coloring_no_drop(cr)
        return False
    