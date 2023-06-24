
fn = 'C:/EdgeCortix/CEM6/CEM6-FH.FCStd'  # set filename

panel_x_both = 7.50                      # x dimension of both PCIe bracket mounting holes
panel_y_lower = 9.35                     # y dimension of lower PCIe bracket mounting hole
panel_y_upper = 9.35 + 85.4              # y dimension of upper PCIe bracket mounting hole
panel_tab_width = 7.95                   # width of PCIe bracket mounting tab
panel_tab_length = panel_tab_width       # length (but really, half of this value past the mounting hole)
panel_tab_radius = 1.27                  # corner radius of PCIe bracket mounting tab
panel_pilot_dia = 2.05                   # pilot hole diameter
panel_TAE_OD = 4.00                      # tap and extrude outside diameter
panel_TAE_length = 2.50                  # length below PWB surface (2.67 max)
panel_pwb_overlap = 1.00                 # distance that the web between tabs extends past the PWB outline
panel_bend_radius = 0.3                  # inside radius of 'square' sheet metal bend
panel_outer_face = 1.90                  # controlling dimension in CEM6

# defined in spec, do not edit
pwb_thickness = 1.57
panel_thickness = 0.86
panel_tab_to_upper = 17.15

# calculated from other parameters
panel_bend_outside = panel_bend_radius + panel_thickness
panel_inner_face = panel_outer_face - panel_thickness

# constants
py = 3.14159265358979323846
v0 = App.Vector(0,0,0)   # fixed vector, origin
vz = App.Vector(0,0,1)   # fixed vector, +z

doc = App.newDocument()  # create empty doc

# PWB outline
pwb = doc.addObject("Sketcher::SketchObject", "Sketch")  # create sketch for PWB boundary
pwb.addGeometry(Part.LineSegment(App.Vector( 0.0,   4.50, 0), App.Vector(15.0,   4.50, 0)), False)  # south edge
pwb.addGeometry(Part.LineSegment(App.Vector(15.0,   4.50, 0), App.Vector(15.0, 111.15, 0)), False)  # east edge
pwb.addGeometry(Part.LineSegment(App.Vector(15.0, 111.15, 0), App.Vector( 0.0, 111.15, 0)), False)  # north edge
pwb.addGeometry(Part.LineSegment(App.Vector( 0.0, 111.15, 0), App.Vector( 0.0,   4.50, 0)), False)  # west edge
pwb.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_lower, 0), vz, panel_pilot_dia/2), False)  # lower hole
pwb.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_upper, 0), vz, panel_pilot_dia/2), False)  # upper hole
pwb.Label = "PWB"  # relabel
pwb.Visibility = True  # set to False to hide sketch

# part
bracket = doc.addObject('PartDesign::Body','Body')  # add body for entire part
bracket.Label = "Bracket"  # relabel

# bracket area
s = panel_y_lower - panel_tab_width/2  # min y
n = panel_y_upper + panel_tab_width/2  # max y
w = 0.0                                # aligned with card edge
e = panel_x_both + panel_tab_length/2  # max x
eminus = e - panel_tab_radius          # max x minus radius
splus = s + panel_tab_radius           # min y plus radius
nminus = n - panel_tab_radius          # max y minus radius
sk = doc.addObject("Sketcher::SketchObject", "sketch_Tab")  # create sketch
sk.addGeometry(Part.LineSegment(App.Vector(w, s, 0), App.Vector(eminus, s, 0)), False)  # south edge
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(eminus, splus, 0), vz, panel_tab_radius), -py/2.0, 0.0),False)  # corner arc
sk.addGeometry(Part.LineSegment(App.Vector(e, splus, 0), App.Vector(e, nminus, 0)), False)  # east edge
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(eminus, nminus, 0), vz, panel_tab_radius), 0.0, +py/2.0),False)  # corner arc
sk.addGeometry(Part.LineSegment(App.Vector(eminus, n, 0), App.Vector(w, n, 0)), False)  # north edge
sk.addGeometry(Part.LineSegment(App.Vector(w, n, 0), App.Vector(w, s, 0)), False)  # west edge
sk.adjustRelativeLinks(bracket)  # start of sketch move to body
sk.Visibility = False  # hide sketch
bracket.ViewObject.dropObject(sk,None,'',[])  # end of sketch move to body
ptabs = bracket.newObject('PartDesign::Pad','Tabs')  # create new Pad
ptabs.Profile = sk  # set Pad profile to sketch
ptabs.Length = panel_thickness  # set thickness of Pad
ptabs.Reversed = 1  # extrude Pad downward

# tap and extrude
sk = doc.addObject("Sketcher::SketchObject", "sketch_TapAndExtrude")  # create sketch
sk.Placement = App.Placement(App.Vector(0.00, 0.00, -0.860000), App.Rotation(0.0, 0.0, 0.0, 1.0))
sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_lower, 0), vz, panel_TAE_OD/2), False)  # lower hole
sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_upper, 0), vz, panel_TAE_OD/2), False)  # upper hole
sk.adjustRelativeLinks(bracket)  # start of sketch move to body
sk.Visibility = False  # hide sketch
bracket.ViewObject.dropObject(sk,None,'',[])  # end of sketch move to body
ptap_and_extrude = bracket.newObject('PartDesign::Pad','TapAndExtrude')  # create new Pad
ptap_and_extrude.Profile = sk  # set Pad profile to sketch
ptap_and_extrude.Length = panel_TAE_length - panel_thickness  # set thickness of Pad
ptap_and_extrude.Reversed = 1  # extrude Pad downward

# bracket cutout
s = panel_y_lower + panel_tab_width/2  # min y
n = panel_y_upper - panel_tab_width/2  # max y
w = panel_pwb_overlap                  # min x
e = panel_x_both + panel_tab_length/2  # max x
eminus = e - panel_tab_radius          # max x minus radius
nplus = n + panel_tab_radius           # max y plus radius
sminus = s - panel_tab_radius          # min y minus radius
sk = doc.addObject("Sketcher::SketchObject", "sketch_TabCut")  # create sketch
sk.addGeometry(Part.LineSegment(App.Vector(w, s, 0), App.Vector(eminus, s, 0)), False)  # south edge
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(eminus, sminus, 0), vz, panel_tab_radius), 0.0, py/2.0),False)  # corner arc
sk.addGeometry(Part.LineSegment(App.Vector(e, sminus, 0), App.Vector(e, nplus, 0)), False)  # east edge
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(eminus, nplus, 0), vz, panel_tab_radius), -py/2.0, 0.0),False)  # corner arc
sk.addGeometry(Part.LineSegment(App.Vector(eminus, n, 0), App.Vector(w, n, 0)), False)  # north edge
sk.addGeometry(Part.LineSegment(App.Vector(w, n, 0), App.Vector(w, s, 0)), False)  # west edge
sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_lower, 0), vz, panel_pilot_dia/2), False)  # lower hole
sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_upper, 0), vz, panel_pilot_dia/2), False)  # upper hole
sk.adjustRelativeLinks(bracket)  # start of sketch move to body
sk.Visibility = False  # hide sketch
bracket.ViewObject.dropObject(sk,None,'',[])  # end of sketch move to body
ptabcut = bracket.newObject('PartDesign::Pocket','TabCut')  # create new Pocket
ptabcut.Profile = sk  # set Pocket profile to sketch
ptabcut.Length = panel_TAE_length  # set thickness of Pocket
ptabcut.Reversed = 0  # not sure why Pocket doesn't need to be reversed like Pad

# tab radius
s = -panel_thickness
n = 0.0
w = -(panel_inner_face - panel_bend_radius)
e = 0.0
ni =  n + panel_bend_radius  # north after inside radius
wi =  w - panel_bend_radius  # west after inside radius

sk = doc.addObject("Sketcher::SketchObject", "sketch_TabRadius")  # create sketch
# sk.Placement = App.Placement(App.Vector(0.0, panel_y_lower - panel_tab_width/2, 0.0),  App.Rotation(0.707107, 0.000000, 0.000000, 0.707107))
sk.Placement = App.Placement(App.Vector(0.0, panel_y_lower - panel_tab_width/2, 0.0),  App.Rotation(0,0,90), v0)
sk.addGeometry(Part.LineSegment(App.Vector(w, s, 0), App.Vector(e, s, 0)), False)  # south edge
sk.addGeometry(Part.LineSegment(App.Vector(e, s, 0), App.Vector(e, n, 0)), False)  # east edge
sk.addGeometry(Part.LineSegment(App.Vector(e, n, 0), App.Vector(w, n, 0)), False)  # north edge
# sk.addGeometry(Part.LineSegment(App.Vector(w, n, 0), App.Vector(wi, ni, 0)), False)  # inside radius, diagonal
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(w, ni, 0), vz, panel_bend_radius), -py, -py/2),False)  # inside radius, arc
sk.addGeometry(Part.LineSegment(App.Vector(wi, ni, 0), App.Vector(wi, panel_tab_to_upper, 0)), False)  # vertical segment to top of spec (inner face)
sk.addGeometry(Part.LineSegment(App.Vector(wi, panel_tab_to_upper, 0), App.Vector(wi - panel_thickness, panel_tab_to_upper, 0)), False)  # horizontal segment at top of spec
sk.addGeometry(Part.LineSegment(App.Vector(wi - panel_thickness, panel_tab_to_upper, 0), App.Vector(wi - panel_thickness, ni, 0)), False)  # outer face
# sk.addGeometry(Part.LineSegment(App.Vector(wi - panel_thickness, ni, 0), App.Vector(w, s, 0)), False)  # outside radius, diagonal
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(w, ni, 0), vz, panel_bend_outside), -py, -py/2),False)  # outside radius, arc
sk.adjustRelativeLinks(bracket)  # start of sketch move to body
sk.Visibility = False  # hide sketch
bracket.ViewObject.dropObject(sk,None,'',[])  # end of sketch move to body
ptab_radius = bracket.newObject('PartDesign::Pad','TabRadius')  # create new Pad
ptab_radius.Profile = sk  # set Pad profile to sketch
ptab_radius.Length = panel_y_upper - panel_y_lower + panel_tab_width  # set thickness of Pad
ptab_radius.Reversed = 1  # extrude Pad downward

doc.recompute()  # redraw
Gui.SendMsgToActiveView("ViewFit")  # fit all
doc.saveAs(fn)  # save file for the first time

# end of CEM6-FH script
