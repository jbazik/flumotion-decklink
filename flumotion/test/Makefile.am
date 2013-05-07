include $(top_srcdir)/common/python.mk
include $(top_srcdir)/common/trial.mk

setup.py: $(top_builddir)/config.status
	cd $(top_builddir) && $(SHELL) ./config.status $(subdir)/$@

BUILT_SOURCES = setup.py

EXTRA_DIST = __init__.py

TRIAL_ENV = $(top_builddir)/env

check-local: trial

clean-local:
	rm -f $(BUILT_SOURCES)

