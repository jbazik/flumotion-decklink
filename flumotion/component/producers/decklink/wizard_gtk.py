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


import gettext
import os

import gobject
import gst

from zope.interface import implements

from flumotion.admin.assistant.interfaces import IProducerPlugin
from flumotion.admin.assistant.models import AudioProducer, VideoProducer,\
	AudioEncoder, VideoEncoder, VideoConverter
from flumotion.common import errors, messages
from flumotion.common.i18n import N_, gettexter
from flumotion.common.messages import Info
from flumotion.admin.gtk.basesteps import AudioProducerStep, VideoProducerStep

__version__ = "$Rev$"
_ = gettext.gettext
T_ = gettexter()


class DecklinkProducer(AudioProducer, VideoProducer):
    componentType = 'decklink-producer'

    def __init__(self):
        super(DecklinkProducer, self).__init__()

        self.properties.device = 0
        self.properties.connection = 0
        self.properties.mode = 0
        self.properties.audio_input = 0
        self.properties.width = 640
        self.properties.height = 360
        self.properties.framerate = 30.0

    def getFeederName(self, component):
        if isinstance(component, AudioEncoder):
            return 'audio'
        elif isinstance(component, (VideoEncoder, VideoConverter)):
            return 'video'
        else:
            raise AssertionError

class _DecklinkCommon:
    # icon = 'decklink.png'
    gladeFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'wizard.glade')
    componentType = 'decklink'

    def setup(self):
        #self._probeCards()
        self.device.data_type = int
        self.mode.data_type = int
        self.connection.data_type = int
        self.audio_input.data_type = int
        self.width.data_type = int
        self.height.data_type = int
        self.framerate.data_type = float
        self.mode.prefill([('default', self.model.properties.mode)])
        self.connection.prefill([('default', self.model.properties.connection)])
        self.audio_input.prefill([('default', self.model.properties.audio_input)])
        self._aspect = self.model.properties.width / self.model.properties.height;
        self.add_proxy(self.model.properties,
            ['device', 'mode', 'connection', 'audio_input',
             'width', 'height', 'framerate'])
        self._sigs = {
            'mode': self.mode.connect('changed', self.on_mode_changed),
            'width': self.width.connect('value-changed', self.on_width_changed),
            'height': self.height.connect('value-changed', self.on_height_changed)
        }

    def on_mode_changed(self, combo):
        mode = self.mode.get_selected()
        if mode is not None:
            aspect = self.get_aspect(self.model.properties.mode)
            if self._aspect != aspect:
               self._aspect = aspect
               height = int(round(self.model.properties.width / self._aspect))
               if self.model.properties.height != height:
                   self.height.handler_block(self._sigs['height'])
                   self.height.set_value(height)
                   self.height.handler_unblock(self._sigs['height'])

    def on_width_changed(self, entry):
        height = int(round(self.model.properties.width / self._aspect))
        if self.model.properties.height != height:
            self.height.handler_block(self._sigs['height'])
            self.height.set_value(height)
            self.height.handler_unblock(self._sigs['height'])

    def on_height_changed(self, entry):
        width = int(round(self.model.properties.height * self._aspect))
        if self.model.properties.width != width:
            self.width.handler_block(self._sigs['width'])
            self.width.set_value(width)
            self.width.handler_unblock(self._sigs['width'])

    def get_aspect(self, mode):
        cap = self._caps['video'][mode]
        return float(cap['width']) / float(cap['height'])

    def workerChanged(self, worker):
        self.model.worker = worker
        self.wizard.requireElements(worker, 'decklinksrc')
        self._probeCards()

    def _format_menu(self, p):
        menu = []
        for item in p:
            label = item['nick'] or item['name']
            menu.append((str(item['value']) + ": " + label, item['value']))
        return menu

    def _probeCards(self):
        self.vbox1.set_sensitive(False)
        self.wizard.blockNext(True)
        msg = messages.Info(T_(N_('Probing for Decklink devices...')),
            mid='decklink-probe')
        self.wizard.add_msg(msg)

        d = self.wizard.runInWorker(self.model.worker,
            'flumotion.worker.checks.decklink', 'getPropsAndCaps')

        def gotPropsAndCaps((props, caps)):
            self.wizard.clear_msg('decklink-probe')
            self._props = props
            self._caps = caps
            self.mode.prefill(self._format_menu(props['mode']))
            self.connection.prefill(self._format_menu(props['connection']))
            self.audio_input.prefill(self._format_menu(props['audio-input']))
            self._aspect = self.get_aspect(self.model.properties.mode)
            self.wizard.blockNext(False)
            self.vbox1.set_sensitive(True)

        d.addCallback(gotPropsAndCaps)

        return d

class DecklinkVideoStep(_DecklinkCommon, VideoProducerStep):
    name = 'Decklink Video'
    title = _('Decklink Video')
    #docSection = 'help-configuration-assistant-producer-video-decklink'
    #docAnchor = ''

    def __init__(self, wizard, model):
        VideoProducerStep.__init__(self, wizard, model)

    # WizardStep

    def setup(self):
        _DecklinkCommon.setup(self)
        self.audio_frame.hide()

class DecklinkAudioStep(_DecklinkCommon, AudioProducerStep):
    name = 'Decklink Audio'
    title = _('Decklink Audio')
    #docSection = 'help-configuration-assistant-producer-video-decklink'
    #docAnchor = ''

    def __init__(self, wizard, model):
        AudioProducerStep.__init__(self, wizard, model)

    # WizardStep

    def setup(self):
        _DecklinkCommon.setup(self)
        self.video_frame.hide()

    def getNext(self):
        return None

class DecklinkWizardPlugin(object):
    implements(IProducerPlugin)

    def __init__(self, wizard):
        self.wizard = wizard
        self.model = DecklinkProducer()

    def getProductionStep(self, type):
        if type == 'audio':
            return DecklinkAudioStep(self.wizard, self.model)
        elif type == 'video':
            return DecklinkVideoStep(self.wizard, self.model)
