Flumotion-decklink
==================

This is a Flumotion producer component for Blackmagic DeckLink devices.
It is based on the free decklink gstreamer plugin, which is part of
http://gstreamer.freedesktop.org/modules/gst-plugins-bad.html.

Flumotion (http://www.flumotion.net/) is an open source multimedia
streaming server.

BlackMagic (http://www.blackmagicdesign.com/) makes video production hardware.

Install
-------

First run the autotools::

 libtoolize -c --force
 autopoint --force
 intltoolize -f
 aclocal -I common
 autoconf
 automake -a -c -f

Then you can run either::

 configure
 make

or, you can build a debian package::

 dpkg-buildpackage

There's also a .spec file for building an rpm.
