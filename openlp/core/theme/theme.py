# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import types

from xml.etree.ElementTree import ElementTree, XML
from PyQt4 import QtGui

DelphiColors={"clRed":0xFF0000,
                "clBlue":0x0000FF,
                "clYellow":0x0FFFF00,
               "clBlack":0x000000,
               "clWhite":0xFFFFFF}

blankstylexml=\
'''<?xml version="1.0" encoding="iso-8859-1"?>
<Theme>
  <Name>BlankStyle</Name>
  <BackgroundMode>1</BackgroundMode>
  <BackgroundType>0</BackgroundType>
  <BackgroundParameter1>$000000</BackgroundParameter1>
  <BackgroundParameter2/>
  <BackgroundParameter3/>
  <FontName>Arial</FontName>
  <FontColor>clWhite</FontColor>
  <FontProportion>30</FontProportion>
  <FontUnits>pixels</FontUnits>
  <Shadow>0</Shadow>
  <Outline>0</Outline>
  <HorizontalAlign>0</HorizontalAlign>
  <VerticalAlign>0</VerticalAlign>
  <WrapStyle>0</WrapStyle>
</Theme>
'''

class Theme:
    def __init__(self, xml):
        """ stores the info about a theme
        attributes:
          name : theme name

           BackgroundMode   : 1 - Transparent
                             1 - Opaque

          BackgroundType   : 0 - solid color
                             1 - gradient color
                             2 - image

          BackgroundParameter1 : for image - filename
                                 for gradient - start color
                                 for solid - color
          BackgroundParameter2 : for image - border colour
                                 for gradient - end color
                                 for solid - N/A
          BackgroundParameter3 : for image - N/A
                                 for gradient - 0 -> vertical, 1 -> horizontal

          FontName       : name of font to use
          FontColor      : color for main font
          FontProportion : size of font
          FontUnits      : whether size of font is in <pixels> or <points>

          Shadow       : 0 - no shadow, non-zero use shadow
          ShadowColor  : color for drop shadow
          Outline      : 0 - no outline, non-zero use outline
          OutlineColor : color for outline (or None for no outline)

          HorizontalAlign : 0 - left align
                            1 - right align
                            2 - centre align
          VerticalAlign   : 0 - top align
                            1 - bottom align
                            2 - centre align
          WrapStyle       : 0 - normal
                            1 - lyrics
        """
        # init to defaults
        self._set_from_XML(blankstylexml)
        self._set_from_XML(xml)
#        print self.__str__()

    def _get_as_string(self):
        s = u''
        keys=dir(self)
        keys.sort()
        for k in keys:
            if k[0:1] != u'_':
                s += u'_%s_' %(getattr(self,k))
        return s

    def _set_from_XML(self, xml):
        root = ElementTree(element=XML(xml))
        iter = root.getiterator()
        for element in iter:
            if element.tag != u'Theme':
                t = element.text
#                print element.tag, t, type(t)
                val = 0
                # easy!
                if type(t) == type(None):
                    val = t
                # strings need special handling to sort the colours out
                if type(t) is types.StringType or type(t) is types.UnicodeType:
#                    print u'str',
                    if t[0] == u'$': # might be a hex number
#                        print u'hex',
                        try:
                            val = int(t[1:], 16)
                        except ValueError: # nope
#                            print u'nope'
                            pass
                    elif DelphiColors.has_key(t):
#                        print u'colour ', t
                        val = DelphiColors[t]
                    else:
                        try:
                            val = int(t)
                        except ValueError:
                            val = t
                if (element.tag.find(u'Color') > 0 or
                    (element.tag.find(u'BackgroundParameter') == 0 and type(val) == type(0))):
                    # convert to a wx.Colour
                    val= QtGui.QColor((val>>16) & 0xFF, (val>>8)&0xFF, val&0xFF)
#                    print [val]
#                print u'>> ', element.tag, val
                setattr(self, element.tag, val)

    def __str__(self):
        s = u''
        for k in dir(self):
            if k[0:1] != u'_':
                s += u'%30s : %s\n' %(k, getattr(self, k))
        return s
