# -*- coding: utf-8 -*-
"""
Author : Nicolas Avellan
Layout : Rectangular bottom electrode
Date : 18.02.2025
"""

import gdspy
lib = gdspy.GdsLibrary()

# Variables
w = 10 # width [um]
h = 10 # height [um]

# Layers
ld_electrode = {"layer": 0}

# Layout
cell = lib.new_cell('Electrode')
rectangle = gdspy.Rectangle((0, 0), (w, h), **ld_electrode)
cell.add(rectangle)

cell2 = lib.new_cell('Cross')
cross = gdspy.polygon(())


lib.write_gds('BottomElectrode.gds')

# Display
cell.write_svg('first.svg')
gdspy.LayoutViewer()


