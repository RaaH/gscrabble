# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from gi.repository import Gtk

#===============================================================
class About(Gtk.AboutDialog):
    
    def __init__(self, pt):
        self.pt = pt
        Gtk.AboutDialog.__init__(self, parent = self.pt, wrap_license = True)
        self.set_icon_name("gscrabble")
        self.set_logo_icon_name('gscrabble')
        self.set_program_name(_("Golden Scrabble"))
        self.set_version("0.1.4")
        self.set_comments(_("Crossword puzzle game amusing and useful."))
        self.set_website("http://sourceforge.net/projects/gscrabble/files/")
        self.set_website_label(_('Golden Scrabble website'))
        self.set_translator_credits(_("translator-credits"))
        self.set_authors(['',
                           'أحمد رغدي<asmaaarab@gmail.com>',
                           ])
        self.set_license(_("This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version."))
        self.run()
        self.destroy()
