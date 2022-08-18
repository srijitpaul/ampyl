#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created July 2022.

@author: M.T. Hansen
"""

###############################################################################
#
# ampyl.py
#
# MIT License
# Copyright (c) 2022 Maxwell T. Hansen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
###############################################################################

import numpy as np
import unittest
import ampyl


class TestFlavorChannel(unittest.TestCase):
    """Class to test the FlavorChannel class."""

    def get_g_abbreviated(self, E, nP, L, kentry_row, kentry_col,
                          ell_row, mazi_row, ell_col, mazi_col):
        """Get G, abbreviated form."""
        masses = [1.]*3
        alphabeta = [-1., 0.]
        G = ampyl.QCFunctions.getG_single_entry(E, nP, L,
                                                kentry_row, kentry_col,
                                                ell_row, mazi_row,
                                                ell_col, mazi_col,
                                                *masses, *alphabeta,
                                                False,
                                                'relativistic pole',
                                                'hermitian, real harmonics')
        return G

    def get_value_direct(self, E, nP, L, kellm_space_row, kellm_space_col,
                         fcs):
        """Get G matrix in a direct way."""
        G_direct = [[]]
        for kellm_entry_row in kellm_space_row:
            G_row = []
            for kellm_entry_col in kellm_space_col:
                kentry_row = kellm_entry_row[:3]
                kentry_col = kellm_entry_col[:3]
                ell_row = kellm_entry_row[3]
                mazi_row = kellm_entry_row[4]
                ell_col = kellm_entry_col[3]
                mazi_col = kellm_entry_col[4]
                Gtmp = self.get_g_abbreviated(E, nP, L,
                                              kentry_row, kentry_col,
                                              ell_row, mazi_row,
                                              ell_col, mazi_col)
                G_row = G_row+[Gtmp*fcs.g_templates[0][0][0][0]]
            G_direct = G_direct+[G_row]
        G_direct = np.array(G_direct[1:])
        return G_direct

    def setUp(self):
        """Exectue set-up."""
        fc = ampyl.FlavorChannel(3)
        fcs = ampyl.FlavorChannelSpace(fc_list=[fc])
        fvs = ampyl.FiniteVolumeSetup()
        tbis = ampyl.ThreeBodyInteractionScheme()
        qcis = ampyl.QCIndexSpace(fcs=fcs, fvs=fvs, tbis=tbis,
                                  Emax=5., Lmax=7.)

        self.epsilon = 1.0e-15

        self.qcis = qcis
        self.fcs = fcs
        self.g = ampyl.G(qcis=qcis)

        fvs = ampyl.FiniteVolumeSetup(nP=np.array([0, 0, 1]))
        tbis = ampyl.ThreeBodyInteractionScheme()
        qcis_001 = ampyl.QCIndexSpace(fcs=fcs, fvs=fvs, tbis=tbis,
                                      Emax=5., Lmax=7.)
        self.qcis_001 = qcis_001
        self.g_001 = ampyl.G(qcis=qcis_001)

    def tearDown(self):
        """Execute tear-down."""
        pass

    def test_g_zero(self):
        """Test G."""
        E = 4.
        nP = np.array([0, 0, 0])
        L = 5.
        kentry_row = nP
        kentry_col = nP
        ell_row = 0
        mazi_row = 0
        ell_col = 0
        mazi_col = 0
        m = 1.
        masses = [m]*3
        alphabeta = [-1., 0.]
        G = ampyl.QCFunctions.getG_single_entry(E, nP, L,
                                                kentry_row, kentry_col,
                                                ell_row, mazi_row,
                                                ell_col, mazi_col,
                                                *masses, *alphabeta,
                                                False,
                                                'relativistic pole',
                                                'hermitian, real harmonics')
        smpl = 1./(2.*m*L**3)
        covpole = 1./((E-2.*m)**2-m**2)
        G_direct = smpl**2*covpole
        self.assertTrue(np.abs(G-G_direct) < self.epsilon)

        G = ampyl.QCFunctions.getG_single_entry(E, nP, L,
                                                kentry_row, kentry_col,
                                                ell_row, mazi_row,
                                                ell_col, mazi_col,
                                                *masses, *alphabeta,
                                                False,
                                                'original pole',
                                                'hermitian, real harmonics')
        smpl_nv = 1./(2.*m)
        pole = 1./(E-3.*m)
        G_direct = smpl**2*pole*smpl_nv
        self.assertTrue(np.abs(G-G_direct) < self.epsilon)

        E = 6.
        nP = np.array([0, 0, 1])
        L = 10.
        kentry_row = np.array([0, 1, 1])
        kentry_col = np.array([1, 0, 0])
        m = 1.5
        masses = [m]*3
        alphabeta = [-1., 0.]
        G = ampyl.QCFunctions.getG_single_entry(E, nP, L,
                                                kentry_row, kentry_col,
                                                ell_row, mazi_row,
                                                ell_col, mazi_col,
                                                *masses, *alphabeta,
                                                False,
                                                'relativistic pole',
                                                'hermitian, real harmonics')
        om_1 = np.sqrt(m**2+(2.*np.pi/L)**2*(kentry_row@kentry_row))
        om_2 = np.sqrt(m**2+(2.*np.pi/L)**2*(kentry_col@kentry_col))
        om_3 = np.sqrt(m**2+(2.*np.pi/L)**2*((nP-kentry_row-kentry_col)
                                             @ (nP-kentry_row-kentry_col)))
        smpl_a = 1./(2.*om_1*L**3)
        smpl_b = 1./(2.*om_2*L**3)
        covpole = 1./((E-om_1-om_2)**2-om_3**2)
        G_direct = smpl_a*smpl_b*covpole
        self.assertTrue(np.abs(G-G_direct) < self.epsilon)

        E = 3.
        m = 1.
        masses = [m]*3
        alphabeta = [-1., 0.]
        G = ampyl.QCFunctions.getG_single_entry(E, nP, L,
                                                kentry_row, kentry_col,
                                                ell_row, mazi_row,
                                                ell_col, mazi_col,
                                                *masses, *alphabeta,
                                                False,
                                                'relativistic pole',
                                                'hermitian, real harmonics')
        om_1 = np.sqrt(m**2+(2.*np.pi/L)**2*(kentry_row@kentry_row))
        om_2 = np.sqrt(m**2+(2.*np.pi/L)**2*(kentry_col@kentry_col))
        om_3 = np.sqrt(m**2+(2.*np.pi/L)**2*((nP-kentry_row-kentry_col)
                                             @ (nP-kentry_row-kentry_col)))
        smpl_a = 1./(2.*om_1*L**3)
        smpl_b = 1./(2.*om_2*L**3)
        covpole = 1./((E-om_1-om_2)**2-om_3**2)
        E2rowSQ = (E-om_1)**2-(2.*np.pi/L)**2*(nP-kentry_row)@(nP-kentry_row)
        E2colSQ = (E-om_2)**2-(2.*np.pi/L)**2*(nP-kentry_col)@(nP-kentry_col)
        HH = ampyl.BKFunctions.J_slow(E2rowSQ/(2.*m)**2)\
            * ampyl.BKFunctions.J_slow(E2colSQ/(2.*m)**2)
        G_direct = smpl_a*smpl_b*covpole*HH
        self.assertTrue(np.abs(G-G_direct) < self.epsilon)

    def test_g_one(self):
        """Test G, first test."""
        G = self.g.get_value(5., 7.)
        G_direct = self.get_value_direct(5., np.array([0, 0, 0]), 7.,
                                         self.qcis.kellm_spaces[0][0],
                                         self.qcis.kellm_spaces[0][0],
                                         self.fcs)
        self.assertTrue((G-G_direct < self.epsilon).all())

    def test_g_two(self):
        """Test G, second test."""
        G = self.g_001.get_value(5., 7.)
        G_direct = self.get_value_direct(5., np.array([0, 0, 1]), 7.,
                                         self.qcis_001.kellm_spaces[0][0],
                                         self.qcis_001.kellm_spaces[0][0],
                                         self.fcs)
        self.assertTrue((G-G_direct < self.epsilon).all())


class Template(unittest.TestCase):
    """Test."""

    def setUp(self):
        """Exectue set-up."""
        pass

    def tearDown(self):
        """Execute tear-down."""
        pass

    def __example(self, x):
        return x

    def test(self):
        """Example test."""
        self.assertEqual(10., self.__example(10.))


unittest.main()