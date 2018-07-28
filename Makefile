#========================#
# -GoldenScrabble Makefile 0.1 #
# - Under GPL license   #
# - Date 1439/10/09      #
#========================#
	
SHELL=/bin/bash
PYTHON=`which python`
DESTDIR=/
PREFIX=/usr
.PHONY: all install uninstall

all:
	@echo "You can use install uninstall args , if you want to install in system use root permissions .";

install:
	python3 setup.py install --prefix=$(PREFIX) --root=$(DESTDIR) --record=installed-files.txt

uninstall:		
	@bash uninstall
