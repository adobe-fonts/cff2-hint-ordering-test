This repository contains a single variable font file with support the limited
glyph set A-Z, a-z, and 1 (plus a normal space and .notdef). This font was
created to test CFF2 rasterization when the ordering of horizontal or veritcal
stems changes as a result of elements moving relative to one another in
different instances.

The CFF specification requires that, within a given CharString, the lists of
vertical and horizontal stems be stored in sort order (by the start of the
stem). The original CFF2 specification did not add to or modify this
requirement, although stems sizes and positions could now be variable.

In some variable glyph designs the stem of one element might cross another.  if
the requirement were that stems must stay ordered in all regions of
designspace, one or the other of those stems would need to be removed. Because
it is desirable to support hinting of both stems in such cases, Adobe has
proposed loosening the requirement so that stems for the *default instance*
must be in order, but can change order in other regions of designspace.

The limited font built from this repository, which is based on glyphs copied
from Source-Serif, tests such cases. The two axes—`wght` and `opsz`—from Source
Serif are retained. An additional `posi` axis causes an accent-like element to
move from bottom to top, or left to right, relative to a letter.  As a result of
that movement the stem(s) of the accent-like element cross stems of the letter.

The font can be used to test existing CFF2 rasterizers to determine how fonts
encoded according to the modified specification will behave. So far, Adobe's
testing with both its own CoolType rasterizer and the open source FreeType
rasterizer indicate that the glyphs render the same way regardless of the
accent position. This suggests that those implementations are not depending on
the ordering of the stems when rasterizing (e.g. doing a binary search for
matching stems rather than a linear scan).  Any such rasterizer already complies
with the proposed change to the specification.

This branch of the repository contains the original sources for the font.

It can be built by running:

`python ./buildVFs.py --hinted`

assuming AFDKO has been installed.  `otfautohint` is run with the `-k` option,
causing it to not strip out "conflicting" stems.

Note, however, that the following entries were added to the name table after
the creation of the font using ttx:

```
    <namerecord nameID="8" platformID="3" platEncID="1" langID="0x409">
      Adobe
    </namerecord>
    <namerecord nameID="9" platformID="3" platEncID="1" langID="0x409">
      Frank Grießhammer and Skef Iterum
    </namerecord>
    <namerecord nameID="11" platformID="3" platEncID="1" langID="0x409">
      http://github.com/adobe-fonts/cff2-hint-ordering-test
    </namerecord>
    <namerecord nameID="13" platformID="3" platEncID="1" langID="0x409">
      This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL. This Font Software is distributed on an ‘AS IS’ BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the SIL Open Font License for the specific language, permissions and limitations governing your use of this Font Software.
    </namerecord>
    <namerecord nameID="14" platformID="3" platEncID="1" langID="0x409">
      http://scripts.sil.org/OFL
    </namerecord>

```

I have created this branch mostly as a record; I do not expect this font
will need to be built again.  The `composition_files` directory contains the 
(very hacky) scripts and files used to build the UFO directories, starting with
the Roman Source-Serif UFO sources.  They may be of some use as references for
a similar project, but that's probably all.
