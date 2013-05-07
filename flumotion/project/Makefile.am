include $(top_srcdir)/common/python.mk
include $(top_srcdir)/common/locale.mk

flumotiondir = $(libdir)/flumotion/python/flumotion/project

flumotion_PYTHON = decklink.py

clean-local:
	rm -f *.pyc *.pyo

PROJECT = decklink

BUILT_SOURCES = decklink.py
CLEANFILES = $(BUILT_SOURCES)

EXTRA_DIST = decklink.py.in
