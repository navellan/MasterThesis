"""
Author : Nicolas Avellan Marin
Title : IDTs
Date : 19.02.2025
"""
import gdspy
gdspy.current_library = gdspy.GdsLibrary()
lib = gdspy.GdsLibrary()

# Governing Dimensions 
duty_factor = 0.5 # IDT metalization ratio [-]
lambda_ = 1 # IDT wavelength [um]
lambda_r = 1 # reflector wavelength [um]
l_gap = 10 # IDT-bus gap [um]
l_aperture = 15*lambda_ # IDT length [um]
w_e = 120 # electrode width [um]
w_c = 30 # G connectors width [um]
delta = 2*lambda_ # lateral offset between reflectors and IDTs [um]
p_GSG = 150 # GSG probe pitch [um]
N_i = 10 # IDT number per electrode [-]
N_r = 10 # reflector number per side [-]

# Options
dummy_fingers = False
shorted_reflectors = False

# Derived parameters for readability
w_i = duty_factor*lambda_ # IDT width [um]
w_gap = (1-duty_factor)*lambda_ # IDT lateral gap [um]
w_r = duty_factor*lambda_r # reflector width [um]
w_gap_r = (1-duty_factor)*lambda_r # reflector lateral gap [um]
l_dummy = dummy_fingers*0.5*l_gap # dummy finger length [um]
l_r = l_aperture + l_gap # reflector length [um]
l_short = shorted_reflectors*w_r # shorted reflector path width [um]
l_is = l_gap # IDT-S distance [um]
l_ig = 5*l_aperture # IDT-G distance [um]

# Collision errors
if any(x<=0 for x in [w_i, w_e, w_c, p_GSG, l_aperture, l_r, l_is, l_ig, w_gap, l_gap, N_i, N_r]):
    raise TypeError("Parameters must be strictly positive.")    
if w_c > w_e :
    raise TypeError("Connector larger than electrode (w_c > w_e).")
if w_e < 120 :
    raise TypeError("Electrode width too small to accept multiple GSG pitches (w_e < 150).")
if w_e > p_GSG :
    raise TypeError("Electrode width too large for current GSG pitch (w_e > p_GSG).")
if (w_i + w_gap)*(N_i + N_r) > 0.5*w_e + p_GSG - w_c:
    raise TypeError("Reflectors are in contact with G electrode connectors.")


# Reflector
cell_R = lib.new_cell("Reflector") 
reflector = gdspy.Rectangle((0, 0), (w_r, l_r))
cell_R.add(reflector)

# Reflector Array
cell_RA = lib.new_cell("R_Array")

if shorted_reflectors : 
    cell_RA.add(gdspy.Rectangle((0,l_r), ((N_r - 1)*(w_r + w_gap_r) + w_r, l_r + l_short)))
    cell_RA.add(gdspy.Rectangle((0,0), ((N_r - 1)*(w_r + w_gap_r) + w_r, -l_short)))

for n in range(N_r):
    cell_RA.add(gdspy.CellReference(cell_R, (n*(w_r + w_gap_r), 0)))

# IDT fingers
cell_I = lib.new_cell("IDT") 
IDT = gdspy.Rectangle((0, 0), (w_i, l_aperture))
cell_I.add(IDT)

if dummy_fingers :
    dummy_finger = gdspy.Rectangle((0, l_r - l_dummy), (w_i, l_r))
    cell_I.add(dummy_finger)
    
# IDT Array
cell_IA = lib.new_cell("IDT_Array")

for m in range(N_i):
    cell_IA.add(gdspy.CellReference(cell_I, (2*m*(w_i+w_gap), 0)))

# S-Electrode
cell_S = lib.new_cell("S-Electrode")
cell_S.add(gdspy.Rectangle((0, 0), (w_e, w_e)))

# G-Electrodes
cell_G = lib.new_cell("G-Electrode")
cell_G.add(gdspy.Rectangle((0, 0), (w_e, w_e)))
cell_G.add(gdspy.Polygon([(0, w_e), (0, w_e + l_aperture + l_gap + l_is + l_ig), (w_e*0.5 + p_GSG, w_e + l_aperture + l_gap + l_is + l_ig), (w_e*0.5 + p_GSG,  w_e + l_aperture + l_gap + l_is + l_ig - w_c), (w_c, w_e + l_is + l_aperture + l_gap + l_ig - w_c), (w_c, w_e)]))

# Device
Device = lib.new_cell("Device")
Device.add(gdspy.CellReference(cell_IA, (0, l_is)))
Device.add(gdspy.CellReference(cell_IA, (2*N_i*(w_i+w_gap) - w_gap, l_is + l_aperture + l_gap), rotation=180))
Device.add(gdspy.CellReference(cell_RA, (-N_r*(w_r+w_gap_r) - delta, l_is + (l_aperture + l_gap - l_r)*0.5)))
Device.add(gdspy.CellReference(cell_RA, (2*(N_i + 0.5)*(w_i+w_gap) + delta, l_is + (l_aperture + l_gap - l_r)*0.5)))
Device.add(gdspy.Rectangle((0,0), (2*(N_i)*(w_i+w_gap) + w_i , l_is)))
Device.add(gdspy.CellReference(cell_I, (2*(N_i)*(w_i+w_gap), l_is))) # additional bottom finger to make IDTs symmetric
Device.add(gdspy.Rectangle((0, l_is + l_r), (2*N_i*(w_i+w_gap) + w_i, l_is + l_r + l_ig)))
Device.add(gdspy.CellReference(cell_S, (-0.5*w_e + (w_i + w_gap)*N_i, -w_e)))
Device.add(gdspy.CellReference(cell_G, (-0.5*w_e - p_GSG + (w_i + w_gap)*N_i, -w_e)))
Device.add(gdspy.CellReference(cell_G, (0.5*w_e + p_GSG + (w_i + w_gap)*N_i, -w_e), rotation=180, x_reflection=True))

    
lib.write_gds('IDT.gds')

gdspy.LayoutViewer()