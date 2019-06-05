include Makevars

XGETTEXT = xgettext
MSGFMT = msgfmt
MSGMERGE = msgmerge
MSGINIT = msginit

LOCALEDIR ?= locale

XGETTEXTOPTIONSCOMMON = --add-comments --sort-output --msgid-bugs-address=$(BUGSADDR) --package-name=$(DOMAIN) --from-code=UTF-8

PO_REGEX = ^([a-z][a-z]|[a-z][a-z]_[A-Z][A-Z])\.po$$
LOCALE_REGEX = ^[a-z][a-z]_[A-Z][A-Z]\.utf8$$

check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

$(call check_defined, DOMAIN)
$(call check_defined, BUGSADDR)


.SUFFIXES: .po .mo .pot

PO = $(wildcard *.po)
LANG = $(basename $(PO))
ifneq ($(SOURCES_SH)$(SOURCES_PY)$(SOURCES_JAVA)$(SOURCES_C),)
MO = $(addsuffix .mo,$(LANG))
endif

%.mo: %.po
	@$(MSGFMT) -c --verbose --statistics -o $@ $<

%.po: SHELL := /bin/bash
%.po:
	@if [[ ! "$@" =~ $(PO_REGEX) ]] ; then \
	 echo "Invalid po file name, must be either xx.po or xx_YY.po" ;\
	 exit 1; \
	fi
	@if ! test -f $@; then \
	 echo "File $@ does not exist." ; \
	 if [[ "$*.utf8" =~ $(LOCALE_REGEX) ]] ; then \
	   if LANG=POSIX locale -a | grep -qxF "$*.utf8" ; then : ; else  \
	    echo "Locale '$*.utf8' not found on your system" ; exit 1 ; \
	   fi; \
	 else \
	   if LANG=POSIX locale -a | grep -qE "^$*_" ; then : ; else \
	    echo "No locale matching '$*' found on your system (see 'locale -a')" ; exit 1; \
	  fi; \
	 fi; \
	 echo -e "You can create it with :\n"; \
	 for ln in $$(LANG=POSIX locale -a | grep -E "^($*_|$*).*\.utf8") ; do \
	  echo " # $(MSGINIT) -l $$ln -i $(DOMAIN).pot -o $@"; \
	 done; \
	 echo ; exit 1; \
	fi;

all: $(MO)

update-po: SHELL := /bin/bash
update-po: $(DOMAIN).pot
	@for po in $(PO); do \
	echo -n "Updating $$po "; \
	if [[ ! "$$po" =~ $(PO_REGEX) ]] ; then \
	 echo " : invalid po file name, must be either xx.po or xx_YY.po" ;\
	 exit 1; \
	fi; \
	$(MSGMERGE) --previous -U $$po $(DOMAIN).pot; \
	done;

$(DOMAIN).pot: Makevars $(SOURCES_PY)
	@echo "Updating $@ .. "
	@$(shell :> $@)
ifdef SOURCES_PY
	@echo -n "  - PY .. "
	@$(XGETTEXT) $(XGETTEXTOPTIONSCOMMON) $(XGETTEXTOPTIONS_PY) -o $@ -j $(SOURCES_PY)
	@echo done
endif

install: all
	for i in $(MO) ; do \
	  t=../$(LOCALEDIR)/`basename $$i .mo`/LC_MESSAGES ;\
	  install -d $$t ;\
	  install -m 644 $$i $$t/$(DOMAIN).mo ;\
	done

clean:
	$(RM) $(MO) *~ $(DESKTOPS)

distclean: clean

maintainer-clean: clean

check: SHELL := /bin/bash
check:
	@for po in $(PO); do \
	echo -n "Checking $$po "; \
	if [[ ! "$$po" =~ $(PO_REGEX) ]] ; then \
	 echo " : invalid po file name, must be either xx.po or xx_YY.po" ;\
	 exit 1; \
	else \
	 echo ".. done"; \
	fi; \
	done;

.PHONY: all update-po install clean distclean maintainer-clean check
