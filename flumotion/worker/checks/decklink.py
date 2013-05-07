# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

# flumotion-decklink - feeder component for BlackMagic decklink cards
#
# Copyright 2012 Brown University
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA


import gobject
import gst

from flumotion.common import errors, messages

__version__ = "$Rev$"


def getPropsAndCaps():
    """
    Probe the gst decklink plugin for properties and capabilities.

    @returns: L{twisted.internet.defer.Deferred}
    """
    result = messages.Result()

    decklinksrc = gst.element_factory_make('decklinksrc', 'srcprobe')
    if not decklinksrc:
        raise errors.ComponentSetupError('No decklink card found.')

    def get_enum(p):
        vals = []
        if not gobject.type_is_a(p.value_type, gobject.TYPE_ENUM):
            raise errors.ComponentSetupError(p.name + ': unexpected property type.')
        else:
            for item in p.enum_class.__enum_values__.items():
                vals.append({
                    'value': item[0],
                    'name': item[1].value_name,
                    'nick': item[1].value_nick
                })
        return vals

    props = {}
    for p in decklinksrc.props:
        if p.name in ('device', 'subdevice'):
            props['device'] = {
                    'minimum': p.minimum,
                    'maximum': p.maximum
            }
        elif p.name == 'connection':
            props['connection'] = get_enum(p)
        elif p.name == 'mode':
            props['mode'] = get_enum(p)
        elif p.name == 'audio-input':
            props['audio-input'] = get_enum(p)

    def get_data(key, value, props):
        props[key] = value
        return 1

    caps = {
        'video': [],
        'audio': []
    }
    videopad = decklinksrc.get_pad_template('videosrc')
    for cap in videopad.get_caps():
        attrs = { 'name': cap.get_name() }
        cap.foreach(get_data, attrs)
        caps['video'].append(attrs)
    audiopad = decklinksrc.get_pad_template('audiosrc')
    for cap in audiopad.get_caps():
        attrs = { 'name': cap.get_name() }
        cap.foreach(get_data, attrs)
        caps['audio'].append(attrs)

    result.succeed((props, caps))
    return result
