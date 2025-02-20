"""
Author : Nicolas Avellan Marin
Title : IDTs
Date : 19.02.2025
"""
import gdspy
gdspy.current_library = gdspy.GdsLibrary()
lib = gdspy.GdsLibrary()

# Variables
w_i = 2 # IDT width [um]
w_e = 120 # electrode width [um]
w_c = 30 # G connectors width [um]
p_GSG = 150 # GSG probe pitch [um]
l_i = 100 # IDT length [um]
l_r = 100 # reflector length [um]
l_is = 10 # IDT-S distance [um]
l_ig = 500 # IDT-G distance [um]
x1 = 5   # IDT lateral interdistance [um]
x2 = 10 # IDT vertical interdistance [um]
M = 10 # IDT number per electrode
N = 10 # reflector number per side


if any(x<=0 for x in [w_i, w_e, w_c, p_GSG, l_i, l_r, l_is, l_ig, x1, x2, M, N]):
    raise TypeError("Parameters must be strictly positive.")    
if w_c > w_e :
    raise TypeError("Connector larger than electrode (w_c > w_e).")
if w_e < 120 :
    raise TypeError("Electrode width too small to accept multiple GSG pitches (w_e < 150).")
if w_e > p_GSG :
    raise TypeError("Electrode width too large for current GSG pitch (w_e > p_GSG).")
if (w_i + x1)*(M + N) > 0.5*w_e + p_GSG - w_c:
    raise TypeError("Reflectors are in contact with G electrode connectors.")


# Reflector
cell_R = lib.new_cell("Reflector") 
reflector = gdspy.Rectangle((0, 0), (w_i, l_r))
cell_R.add(reflector)

# Reflector Array
cell_RA = lib.new_cell("R_Array")

for n in range(N):
    cell_RA.add(gdspy.CellReference(cell_R, (n*(w_i+x1), 0)))

# IDT
cell_I = lib.new_cell("IDT") 
IDT = gdspy.Rectangle((0, 0), (w_i, l_i))
cell_I.add(IDT)
    
# IDT Array
cell_IA = lib.new_cell("IDT_Array")

for m in range(M):
    cell_IA.add(gdspy.CellReference(cell_I, (2*m*(w_i+x1), 0)))

# S-Electrode
cell_S = lib.new_cell("S-Electrode")
cell_S.add(gdspy.Rectangle((0, 0), (w_e, w_e)))

# G-Electrodes
cell_G = lib.new_cell("G-Electrode")
cell_G.add(gdspy.Rectangle((0, 0), (w_e, w_e)))
cell_G.add(gdspy.Polygon([(0, w_e), (0, w_e + l_i + x2 + l_is + l_ig), (w_e*0.5 + p_GSG, w_e + l_i + x2 + l_is + l_ig), (w_e*0.5 + p_GSG,  w_e + l_i + x2 + l_is + l_ig - w_c), (w_c, w_e + l_is + l_i + x2 + l_ig - w_c), (w_c, w_e)]))
cell_G.add(gdspy.Rectangle((w_e*0.5 + p_GSG - (w_i + x1)*M + x1, w_e + l_is + l_i + x2), (w_e*0.5 + p_GSG, w_e + l_is + l_i + x2 + l_ig)))

# Device
Device = lib.new_cell("Device")
Device.add(gdspy.CellReference(cell_IA, (0, l_is)))
Device.add(gdspy.CellReference(cell_IA, (2*M*(w_i+x1)-x1, l_is + l_i + x2), rotation=180))
Device.add(gdspy.CellReference(cell_RA, (-N*(w_i+x1), l_is + (l_i + x2 - l_r)*0.5)))
Device.add(gdspy.CellReference(cell_RA, (2*M*(w_i+x1), l_is + (l_i + x2 - l_r)*0.5)))
Device.add(gdspy.Rectangle((0,0), (2*M*(w_i+x1) - x1, l_is)))
Device.add(gdspy.CellReference(cell_S, (-0.5*w_e + (w_i + x1)*M, -w_e)))
Device.add(gdspy.CellReference(cell_G, (-0.5*w_e - p_GSG + (w_i + x1)*M, -w_e)))
Device.add(gdspy.CellReference(cell_G, (0.5*w_e + p_GSG + (w_i + x1)*M, -w_e), rotation=180, x_reflection=True))


    
lib.write_gds('IDT.gds')

gdspy.LayoutViewer()