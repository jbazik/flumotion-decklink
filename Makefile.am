AUTOMAKE_OPTIONS = dist-bzip2 no-dist-gzip 1.8

ACLOCAL_AMFLAGS = -I common

include $(srcdir)/common/changelog.mk
include $(srcdir)/common/common.mk
include $(srcdir)/common/pychecker.mk
include $(srcdir)/common/deb.mk
include $(srcdir)/common/rpm.mk

SUBDIRS = flumotion conf common misc po

EXTRA_DIST = \
	env.in \
	.version \
	RELEASE \
	LICENSE.LGPL \
	flumotion-decklink.spec

PYCHECKER_WHITELIST = flumotion/component/*/*/*.py \
                      flumotion/component/*/*.py \
PYCHECKER_BLACKLIST =

COVERAGE_MODULES = 

BUILT_SOURCES = $(top_srcdir)/.version
$(top_srcdir)/.version:
	echo $(VERSION) > $@-t && mv $@-t $@

dist: changelog
