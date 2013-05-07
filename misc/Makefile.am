include $(top_srcdir)/common/python.mk

noinst_PYTHON = setup.py

EXTRA_DIST = pycheckerhelp.py preamble.py

setup.py: $(top_builddir)/config.status
	cd $(top_builddir) && $(SHELL) ./config.status $(subdir)/$@

BUILT_SOURCES=setup.py

clean-local:
	rm -f $(BUILT_SOURCES)
	rm -rf *.pyc *.pyo
