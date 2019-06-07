#!/usr/bin/python3
# -*- coding: utf-8 -*-


from distutils.core import setup
from glob import glob


doc_files  = ['AUTHORS', 'ChangeLog', 'README', 'TODO']
data_files = [
              ('share/applications/', ['gscrabble.desktop']),
              ('share/icons/hicolor/gscalable/apps', ['gscrabble.svg']),
              ('share/doc/GScrabble', doc_files),
	      ('share/GScrabble/modules', glob('modules/*.py')),
              ('share/GScrabble/data/stems', glob('data/stems/*.*')),
              ('share/GScrabble/data/dicts', glob('data/dicts/*.*')),
              ('share/GScrabble/locale/en/LC_MESSAGES/', ['locale/en/LC_MESSAGES/gscrabble.mo']),
              ('share/GScrabble/locale/ar/LC_MESSAGES/', ['locale/ar/LC_MESSAGES/gscrabble.mo']),
	      ('share/GScrabble/locale/nl/LC_MESSAGES/', ['locale/nl/LC_MESSAGES/gscrabble.mo']),
	      ('share/GScrabble/locale/fr/LC_MESSAGES/', ['locale/fr/LC_MESSAGES/gscrabble.mo']),
              ('share/icons/hicolor/16x16/apps/', ['hicolor/16x16/apps/gscrabble.png']),
              ('share/icons/hicolor/22x22/apps/', ['hicolor/22x22/apps/gscrabble.png']),
              ('share/icons/hicolor/24x24/apps/', ['hicolor/24x24/apps/gscrabble.png']),
              ('share/icons/hicolor/32x32/apps/', ['hicolor/32x32/apps/gscrabble.png']),
              ('share/icons/hicolor/36x36/apps/', ['hicolor/36x36/apps/gscrabble.png']),
              ('share/icons/hicolor/48x48/apps/', ['hicolor/48x48/apps/gscrabble.png']),
              ('share/icons/hicolor/64x64/apps/', ['hicolor/64x64/apps/gscrabble.png']),
              ('share/icons/hicolor/72x72/apps/', ['hicolor/72x72/apps/gscrabble.png']),
              ('share/icons/hicolor/96x96/apps/', ['hicolor/96x96/apps/gscrabble.png']),
              ('share/icons/hicolor/128x128/apps/',['hicolor/128x128/apps/gscrabble.png']),
              ]

setup(
      name="GoldenScrabble",
      description='crossword puzzle game',
      long_description='crossword puzzle game is funny and useful.',
      version="0.1.0",
      author='Ahmed Raghdi',
      author_email='asmaaarab@gmail.com',
      url="http://sourceforge.net/projects/gscrabble/files/",
      license='GPL License',
      platforms='Linux',
      scripts=['gscrabble'],
      keywords=['game', 'arabic', 'crossword', 'puzzle', 'gold', 'scrabble', 'language'],
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: POSIX :: Linux',
          'Development Status :: 4 - Beta',
          'Environment :: X11 Applications :: Gtk',
          'Natural Language :: Arabic',
          'Intended Audience :: End Users/Desktop',
          'Topic :: Desktop Environment :: Gnome',
			],
      data_files=data_files
      )
