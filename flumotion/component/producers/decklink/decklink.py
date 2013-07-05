# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

# Flumotion - a streaming media server
# Copyright (C) 2004,2005,2006,2007,2008,2009 Fluendo, S.L.
# Copyright (C) 2010,2011 Flumotion Services, S.A.
# All rights reserved.
#
# This file may be distributed and/or modified under the terms of
# the GNU Lesser General Public License version 2.1 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.LGPL" in the source distribution for more information.
#
# Headers in this file shall remain intact.

from flumotion.common.i18n import gettexter
from flumotion.component.common.avproducer import avproducer

__version__ = "$Rev$"
T_ = gettexter()


class Decklink(avproducer.AVProducerBase):

    def get_raw_video_element(self):
        return self.pipeline.get_by_name('raw')

    def get_pipeline_template(self, properties):
        return ('decklinksrc name=src subdevice=%s'
                    '      mode=%s connection=%s audio-input=%s '
                    '  src.videosrc ! identity silent=true name=raw ! queue '
                    '    ! @feeder:video@'
                    '  src.audiosrc ! queue '
                    '    ! volume name=setvolume'
                    '    ! level name=volumelevel message=true '
                    '    ! @feeder:audio@' % (self.device,
                           self.mode, self.connection, self.audio_input))

    def _parse_aditional_properties(self, props):
        self.device = props.get('device', 0)
        self.mode = props.get('mode', 10)
        self.connection = props.get('connection', 0)
        self.audio_input = props.get('audio-input', 0)
