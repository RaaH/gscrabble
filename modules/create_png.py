# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import PangoCairo, Pango
import cairo
import config as config
from tools import *
from data import *
from araby import *

    
def get_letter_png(lang_code, letter):       
    name = config.getv('language_scrabble')
    lang_code = DICT_LANGUAGES_CODE[name] 
    im = cairo.ImageSurface(cairo.FORMAT_ARGB32, 80, 80)
    cr = cairo.Context(im)
    #--bg--#
    cr.rectangle(0, 0, 80, 80)
    R, G, B = rgb(config.getv('bg_pieces'))
    cr.set_source_rgba(R, G, B, 1.0)
    cr.fill()
    #--border--#
    cr.rectangle(0, 0, 80, 80)
    R, G, B = rgb(config.getv('br_pieces'))
    cr.set_source_rgba(R, G, B, 1.0)
    cr.set_line_width(1.0)
    cr.stroke()
    if letter in COMPLEX_LETTERS[lang_code].keys():
        letter1 = COMPLEX_LETTERS[lang_code][letter]
    else:
        letter1 = letter
    if lang_code == 'ar':
        #--letter--#
        letter1 = letter.replace('ه', 'هـ')
        szfont, fmfont = split_font(config.getv('font_pieces'))
        font = '{} {}'.format(fmfont, int(4*int(szfont)))
        layout = PangoCairo.create_layout(cr)
        layout.set_text(letter1, -1)
        desc = Pango.font_description_from_string (font)
        layout.set_font_description(desc)
        layout.set_alignment(1)
        cr.save ()
        w1, h1 = layout.get_pixel_size()
        PangoCairo.update_layout (cr, layout)
        R, G, B = rgb(config.getv('fg_pieces'))
        cr.set_source_rgba(R, G, B, 1.0)
        cr.move_to((80-w1)/2, (h1-80)/2-(h1/8))
        PangoCairo.show_layout(cr, layout)
        cr.restore()
        #--number--#
        cr.set_font_size (int(40*(int(szfont)/20)))
        R, G, B = rgb(config.getv('fg_nbr'))
        cr.set_source_rgba(R, G, B, 1.0)
        cr.move_to(4, 76)
    else:
        #--letter--#
        szfont, fmfont = split_font(config.getv('font_pieces'))
        font = '{} {}'.format(fmfont, int(70*(int(szfont)/15)))
        layout = PangoCairo.create_layout(cr)
        layout.set_text(letter1, -1)
        desc = Pango.font_description_from_string (font)
        layout.set_font_description(desc)
        layout.set_alignment(1)
        cr.save ()
        w, h = layout.get_pixel_size()
        PangoCairo.update_layout (cr, layout)
        R, G, B = rgb(config.getv('fg_pieces'))
        cr.set_source_rgba(R, G, B, 1.0)
        cr.move_to(3*(80-w)/8, (80-h)/2-4)
        PangoCairo.show_layout(cr, layout)
        cr.restore()
        #--number--#
        cr.set_font_size (int(40*(int(szfont)/20)))
        R, G, B = rgb(config.getv('fg_nbr'))
        cr.set_source_rgba(R, G, B, 1.0)
        xb, yb, w, h, xa, ya = cr.text_extents(str(get_letter_value(lang_code, letter)))#xbearing, ybearing, width, height, xadvance, yadvance
        cr.move_to(76-xa, 76)
    cr.show_text (str(get_letter_value(lang_code, letter)))
    # get_all_letters(cr)
    im.write_to_png(join(HOME_DIR, 'last.png'))
    return join(HOME_DIR, 'last.png')

