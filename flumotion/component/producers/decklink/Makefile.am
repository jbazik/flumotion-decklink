include $(top_srcdir)/common/python.mk

componentdir = $(libdir)/flumotion/python/flumotion/component/producers/decklink
component_DATA = 	\
	decklink.xml	\
	wizard.glade

component_PYTHON = 	\
	__init__.py 	\
	admin_gtk.py 	\
	decklink.py	\
	wizard_gtk.py

clean-local:
	rm -rf *.pyc *.pyo

EXTRA_DIST = $(component_DATA)
