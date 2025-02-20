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
l_ie = 10 # IDT-electrode distance [um]
l_ic = 500 # IDT-connector distance [um]
x1 = 5   # IDT lateral interdistance [um]
x2 = 10 # IDT vertical interdistance [um]
M = 1 # IDT number per electrode
N = 1 # reflector number per side

# For Thales theorem check (possible connector-reflector contact)
ratio_1 = (w_e*0.5 - w_c + p_GSG -(2*w_i + 2*x1)*M)/(N*(w_i+x1))
ratio_2 = (l_ie + l_ic + l_i + x2 - w_e)/(l_ic - w_c)


if any(x<=0 for x in [w_i, w_e, w_c, p_GSG, l_i, l_ie, x1, x2, M, N]):
    raise TypeError("Parameters must be strictly positive.")    
if w_c > w_e :
    raise TypeError("Connector larger than electrode (w_c > w_e).")
if w_e < 120 :
    raise TypeError("Electrode width too small to accept multiple GSG pitches (w_e < 150).")
if w_e > p_GSG:
    raise TypeError("Electrode width too large for current GSG pitch (w_e > p_GSG).")
"""
if ~(ratio_1 > ratio_2):
    raise TypeError("G-electrode connector is in contact with reflectors.\n Possible Solutions : 1. Increase l_ic 2. Decrease w_c 3. Increase p_GSG.")
"""   

    

# Reflector
cell_R = lib.new_cell("Reflector") 
reflector = gdspy.Rectangle((0, 0), (w_i, l_i+x2))
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
    cell_IA.add(gdspy.CellReference(cell_I, (m*(2*w_i+2*x1), 0)))
    
cell_IA.add(gdspy.Rectangle((0,0), (M*(2*w_i+2*x1) - x1, -l_ie)))


# S-Electrode
cell_S = lib.new_cell("S-Electrode")
cell_S.add(gdspy.Rectangle((0, 0), (w_e, w_e)))

# G-Electrodes
cell_G = lib.new_cell("G-Electrode")
cell_G.add(gdspy.Rectangle((0, 0), (w_e, w_e)))
cell_G.add(gdspy.Polygon([(0, w_e), (w_e*0.5 + p_GSG - (M*(2*w_i+2*x1) - x1)*0.5, w_e + l_i + x2 + l_ie + l_ic), (w_e*0.5 + p_GSG - (M*(2*w_i+2*x1) - x1)*0.5, w_e + l_i + x2 + l_ie + l_ic - w_c), (w_c, w_e)]))

# Device
Device = lib.new_cell("Device")
Device.add(gdspy.CellReference(cell_IA, (0, 0)))
Device.add(gdspy.CellReference(cell_IA, (M*(2*w_i+2*x1)-x1, l_i+x2), rotation=180))
Device.add(gdspy.Rectangle((0, l_i + x2 + l_ie), ((2*w_i +2*x1)*M, l_i + x2 + l_ic)))
Device.add(gdspy.CellReference(cell_RA, (-N*(w_i+x1), 0)))
Device.add(gdspy.CellReference(cell_RA, (M*(2*w_i+2*x1), 0)))


    
lib.write_gds('IDT.gds')

gdspy.LayoutViewer()