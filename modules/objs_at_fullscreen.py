# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk
from preference import Preference
from word_viewer import Viewer

from tools import *

#===============================================================
class OBJs_1(Gtk.Box): 
    
    def __init__(self, pt):
        self.pt = pt
        Gtk.Box.__init__(self, spacing=3,orientation=Gtk.Orientation.VERTICAL)
        self.set_border_width(3)
        #---------------------------------------------------------------------------------------------
        img = Gtk.Image.new_from_icon_name('emblem-ok-symbolic', 2)
        btn_apply = Gtk.Button()
        btn_apply.set_size_request(80, -1)
        btn_apply.set_tooltip_text(_('Adopted the word that I set.'))
        btn_apply.connect('clicked', self.pt.hd_bar.apply_added)
        btn_apply.set_image(img)
        self.pack_start(btn_apply, False, False, 0)
        #===========================================
        hb = Gtk.Box(spacing=0,orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(hb.get_style_context(), "linked")
        #-------------------------------------------------------------------------------------------
        img = Gtk.Image.new_from_icon_name('dialog-information-symbolic', 2)
        btn_help = Gtk.Button()
        btn_help.set_tooltip_text(_('Suggested word list.'))
        btn_help.connect('clicked', self.pt.hd_bar.help_me_letters)
        btn_help.set_image(img)
        hb.pack_start(btn_help, True, True, 0)
        #-------------------------------------------------------------------------------------------
        nm_icon = 'edit-undo-symbolic'
        if self.pt.get_direction() == Gtk.TextDirection.RTL: nm_icon = 'edit-undo-symbolic-rtl'
        img = Gtk.Image.new_from_icon_name(nm_icon, 2)
        btn_undo = Gtk.Button()
        btn_undo.set_tooltip_text(_('Undo install letters'))
        btn_undo.connect('clicked', self.pt.hd_bar.undo_added)
        btn_undo.set_image(img)
        hb.pack_start(btn_undo,  True, True, 0)
        self.pack_start(hb, False, False, 0)
        #===========================================
        hb = Gtk.Box(spacing=0,orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(hb.get_style_context(), "linked")
        #--------------------------------------------------------------------------------------------
        nm_icon = 'media-seek-forward-symbolic'
        if self.pt.get_direction() == Gtk.TextDirection.RTL: nm_icon = 'media-seek-forward-symbolic-rtl'
        img = Gtk.Image.new_from_icon_name(nm_icon, 2)
        btn_no_play = Gtk.Button()
        btn_no_play.set_tooltip_text(_('I have no word passed the role to the computer.'))
        btn_no_play.connect('clicked', self.pt.hd_bar.skip_2_computer)
        btn_no_play.set_image(img)
        hb.pack_start(btn_no_play, True, True, 0)
        #-------------------------------------------------------------------------------------------
        img = Gtk.Image.new_from_icon_name('view-refresh-symbolic', 2)
        btn_change = Gtk.Button()
        btn_change.set_tooltip_text(_('Change my letter group.'))
        btn_change.connect('clicked', self.pt.hd_bar.change_my_letters)
        btn_change.set_image(img)
        hb.pack_start(btn_change, True, True, 0)
        self.pack_start(hb, False, False, 0)

        
        