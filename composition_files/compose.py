#!/usr/bin/env python

import os
import shutil
import math
import random
import fontforge
import psMat

f = fontforge.font()
cp = 26
angle = math.radians(70)
tfr = psMat.rotate(angle)
trr = psMat.inverse(tfr)

accents = [ 'dotaccentcmb', 'macroncmb', 'ringcmb', 'verticallinemod', 'dieresiscmb' ]

template = 'hintordertest_%s%s%s.ufo'

glyphs = [ 'A_', 'B_', 'C_', 'D_', 'E_', 'F_', 'G_', 'H_', 'I_', 'J_', 'K_', 'L_', 'M_',
              'N_', 'O_', 'P_', 'R_', 'S_', 'T_', 'U_', 'V_', 'W_', 'X_', 'Y_', 'Z_',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
              'one' ]


def addBB(bb1, bb2):
    return (round(min(bb1[0], bb2[0])), 
            round(min(bb1[1], bb2[1])), 
            round(max(bb1[2], bb2[2])), 
            round(max(bb1[3], bb2[3])))

positions = [ 'm', 'd', 'M' ]

adata = {}

for a in accents:
    fname = template % ('d', 'd', 'd') + '/glyphs/' + a + '.glif'
    g = f.createChar(cp)
    cp += 1
    g.importOutlines(fname)
    bb = g.boundingBox()
    c = (round((bb[0] + bb[2]) / 2), round((bb[1] + bb[3]) / 2))
    bbmap = {}
    for i in positions:
        for j in positions:
            fn = template % (i, j, 'd') + '/glyphs/' + a + '.glif'
            g.clear()
            g.importOutlines(fn)
            bbmap[i + j] = (g.boundingBox(), g.foreground)
    adata[a] = (c, bbmap)

for i, gn in enumerate(glyphs):
    a = accents[i % 5]
    vert = (i % 2) == 0
    contouroffset = -1
    minlow = 10000
    maxhigh = -10000
    maxdist = -10000
    maxmove = -10000
    ad = adata[a]
    ac = ad[0]
    for i in positions:
        for j in positions:
            fn = template % (i, j, 'm') + '/glyphs/' + gn + '.glif'
            g.clear()
            g.importOutlines(fn)
            if contouroffset == -1:
                lfg = len(g.foreground)
                if lfg == 0:
                    contouroffset = 0
                else:
                    contouroffset = random.randrange(lfg)
            bb = g.boundingBox()
            abb = ad[1][i + j][0]
            if vert:
                ahalfsize = round((abb[3] - abb[1]) / 2)
                low = bb[1] - ahalfsize - 30
                high = bb[3] + ahalfsize + 30
                dist = bb[2] + ac[0] - abb[0] + 5
                move = 0
            else:
                ahalfsize = round((abb[2] - abb[0]) / 2)
                low = bb[0] - ahalfsize - 30
                high = bb[2] + ahalfsize + 30
                dist = bb[3] + ac[1] - abb[1] + 5
                if (low - ahalfsize) > 0:
                    move = 0
                else:
                    move = ahalfsize - low
            minlow = min(minlow, low)
            maxhigh = max(maxhigh, high)
            maxdist = max(maxdist, dist)
            maxmove = max(maxmove, move)
    print(gn, maxdist - ac[0])
    tf = {}
    if vert:
        tf['m'] = psMat.translate(maxdist - ac[0], minlow - ac[1])
        tf['d'] = psMat.translate(maxdist - ac[0], round((maxhigh - minlow) * .4) + minlow - ac[1])
        tf['M'] = psMat.translate(maxdist - ac[0], maxhigh - ac[1])
    else:
        tf['m'] = psMat.translate(minlow - ac[0], maxdist - ac[1])
        tf['d'] = psMat.translate(round((maxhigh - minlow) * .4) + minlow - ac[0], maxdist - ac[1])
        tf['M'] = psMat.translate(maxhigh - ac[0], maxdist - ac[1])
    if move != 0:
        tf['move'] = psMat.translate(maxmove, 0);

    for i in positions:
        for j in positions:
            for k in positions:
                fn = template % (i, j, k) + '/glyphs/' + gn + '.glif'
                g.clear()
                g.importOutlines(fn)
                l = g.foreground
                al = ad[1][i + j][1].dup()
                al.transform(tf[k])
                abb = ad[1][i + j][0]
                bb = g.boundingBox()
                nl = fontforge.layer()
                for c in range(contouroffset):
                    nl += l[c]
                nl += al
                for c in range(contouroffset, len(l)):
                    nl += l[c]
                g.foreground = nl
                if 'move' in tf:
                    g.transform(tf['move'])
                if vert:
                    g.width = round(move + maxdist + abb[2] - ac[0] + 30)
                else:
                    g.width = round(move + maxhigh + abb[2] - ac[0] + 30)
                g.export(fn)
