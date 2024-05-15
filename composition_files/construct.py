#!/usr/bin/env python

import os
import shutil

srcdir = '/home/skef/ft/adobe/source-serif/Roman'
constdir = '.'

dirfiles = [ 'fontinfo.plist', 'metainfo.plist' ]

fontinfosubs = { 'Source Serif Master': 'Hint Order Test',
                 'Frank Grießhammer': 'Frank Grießhammer, Skef Iterum',
                'SourceSerif4Variable' : 'HintOrderTest'
               }

constfiles = [ 'layercontents.plist', 'lib.plist' ]

smp = { 'mm' : 'Masters/caption/master_0/SourceSerif_c0.ufo',
        'dm' : 'Masters/caption/master_1/SourceSerif_c1.ufo',
        'Mm' : 'Masters/caption/master_2/SourceSerif_c2.ufo',
        'md' : 'Masters/text/master_0/SourceSerif_0.ufo',
        'dd' : 'Masters/text/master_1/SourceSerif_1.ufo',
        'Md' : 'Masters/text/master_2/SourceSerif_2.ufo',
        'mM' : 'Masters/display/master_0/SourceSerif_d0.ufo',
        'dM' : 'Masters/display/master_1/SourceSerif_d1.ufo',
        'MM' : 'Masters/display/master_2/SourceSerif_d2.ufo'
      }

glyphlist = [ 'A_', 'B_', 'C_', 'D_', 'E_', 'F_', 'G_', 'H_', 'I_', 'J_', 'K_', 'L_', 'M_',
              'N_', 'O_', 'P_', 'R_', 'S_', 'T_', 'U_', 'V_', 'W_', 'X_', 'Y_', 'Z_',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
              '_notdef', 'space', 'one', 'dotaccentcmb', 'macroncmb', 'ringcmb', 
              'verticallinemod', 'dieresiscmb'
            ]

for t in ('m', 'd', 'M'):
    for k, v in smp.items():
        sdir = srcdir + '/' + v
        T = k + t
        dname = 'hintordertest_' + T + '.ufo'
        os.mkdir(dname)
        for fn in constfiles:
            shutil.copy(constdir + '/' + fn, dname)
        for fn in dirfiles:
            with open(sdir + '/' + fn, 'r') as f:
                fstr = f.read()
                if fn == 'fontinfo.plist':
                    for sk, sv in fontinfosubs.items():
                        fstr = fstr.replace(sk, sv)
                with open(dname + '/' + fn, 'w') as w:
                    w.write(fstr)
        sgname = sdir + '/glyphs'
        dgname = dname + '/glyphs'
        os.mkdir(dgname)
        for g in glyphlist:
            shutil.copy(sgname + '/' + g + '.glif', dgname + '/' + g + '.glif')
        shutil.copy(constdir + '/contents.plist', dgname + '/contents.plist')
