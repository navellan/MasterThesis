# -*- coding: utf-8 -*-
"""
Author : Nicolas Avellan
Layout : Rectangular bottom electrode
Date : 18.02.2025
"""
import gdspy
gdspy.current_library = gdspy.GdsLibrary()
lib = gdspy.GdsLibrary()

# Variables
w_i = 2 # IDT width [um]
l_i = 100 # IDT length [um]
l_is = 10 # IDT-S distance [um]
x1 = 5   # IDT lateral interdistance [um]
x2 = 10 # IDT vertical interdistance [um]
M = 10 # IDT number per electrode

# Layout
cell = lib.new_cell('Electrode')
cell.add(gdspy.Rectangle((0, l_is), (2*M*(w_i+x1), l_is + l_i + x2)))

# GDS
lib.write_gds('BottomElectrode.gds')

# Display
gdspy.LayoutViewer()


