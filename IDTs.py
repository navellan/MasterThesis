"""
Author : Nicolas Avellan Marin
Title : IDTs
Date : 19.02.2025
"""
import gdspy
gdspy.current_library = gdspy.GdsLibrary()
lib = gdspy.GdsLibrary()

# Variables
w_i = 5 # IDT width [um]
w_e = 1000 # electrode width [um]
l_i = 100 # IDT length [um]
l_e = 1000 # electrode length [um]
l_ie = 200 # IDT-electrode distance [um]
x1 = 10   # IDT lateral interdistance [um]
x2 = 10 # IDT vertical interdistance [um]
M = 20 # IDT number
N = 10 # reflector number 


# Reflector
cell_R = lib.new_cell("Reflector") 
reflector = gdspy.Rectangle((0,0), (w_i, l_i+x2))
cell_R.add(reflector)

# Reflector Array
cell_RA = lib.new_cell("R_Array")

for n in range(N):
    cell_RA.add(gdspy.CellReference(cell_R, (n*(w_i+x1), 0)))

# IDT
cell_I = lib.new_cell("IDT") 
IDT = gdspy.Rectangle((0,0), (w_i, l_i))
cell_I.add(IDT)
    
# IDT Array + Electrode
cell_IE = lib.new_cell("IDT&Electrode")

for m in range(M):
    cell_IE.add(gdspy.CellReference(cell_I, (m*(2*w_i+2*x1), 0)))

cell_IE.add(gdspy.Rectangle((0,0), (M*(2*w_i+2*x1) - x1, - l_ie)))
cell_IE.add(gdspy.Rectangle(((M*(2*w_i+2*x1) - w_e)*0.5, -l_ie), ((M*(2*w_i+2*x1) + w_e)*0.5, - l_ie - l_e)))

# Device

Device = lib.new_cell("Device")

Device.add(gdspy.CellReference(cell_IE, (0, 0)))
Device.add(gdspy.CellReference(cell_IE, (M*(2*w_i+2*x1)-x1, l_i+x2), rotation=180))
Device.add(gdspy.CellReference(cell_RA, (-N*(w_i+x1), 0)))
Device.add(gdspy.CellReference(cell_RA, (M*(2*w_i+2*x1), 0)))


    
lib.write_gds('IDT.gds')

gdspy.LayoutViewer()