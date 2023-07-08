
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
panel_pwb_overlap = 1.00                 # distance that the web between tabs extends into the PWB outline
panel_bend_inside_radius = 0.3           # inside radius of 'square' sheet metal bend
panel_outer_face = 1.90                  # controlling dimension in CEM6
panel_strain_relief = 0.5                # radius of strain relief notches
panel_strain_relief_offset = 0.1         # start of strain relief above tab bend

# defined in spec, do not edit
pwb_thickness = 1.57
panel_thickness = 0.86
panel_tab_to_upper = 17.15
chassis_datum = 104.86
OAL = 120.02
OAW = 18.42
bracket_tip_to_intercept = 5.07
narrow_forty_five = 112.75
height_of_forty_five = 4.115  # 4.11 in spec but that adds up to 18.41 instead of 18.42
width_of_five_bend = 14.30 - height_of_forty_five

# calculated from other parameters
panel_bend_outside_radius = panel_bend_inside_radius + panel_thickness
panel_inner_face = panel_outer_face - panel_thickness
pwb_sides = {"Top": 0.00, "Bot": -pwb_thickness}

# constants
py = 3.14159265358979323846
v0 = App.Vector(0,0,0)   # fixed vector, origin
vz = App.Vector(0,0,1)   # fixed vector, +z
planeXY = App.Rotation(0.0, 0.0, 0.0, 1.0)
planeXZ = App.Rotation(0,0,90)  # requires ', v0' to be appended
planeYZ = App.Rotation(0.5, 0.5, 0.5, 0.5)

# quadrants
Q0 = 0.0
Q1 = py/2
Q2 = py
Q3 = -py/2

doc = App.newDocument()  # create empty doc

# PWB outline(s)
for name in pwb_sides:
    sk = doc.addObject('Sketcher::SketchObject', 'sketch' + name)  # create sketch for PWB boundary
    sk.Placement = App.Placement(App.Vector(0.00, 0.00, pwb_sides[name]), planeXY)  # place sketch
    sk.addGeometry(Part.LineSegment(App.Vector( 0.0,   4.50, 0), App.Vector(15.0,   4.50, 0)), False)  # south edge
    sk.addGeometry(Part.LineSegment(App.Vector(15.0,   4.50, 0), App.Vector(15.0, 111.15, 0)), False)  # east edge
    sk.addGeometry(Part.LineSegment(App.Vector(15.0, 111.15, 0), App.Vector( 0.0, 111.15, 0)), False)  # north edge
    sk.addGeometry(Part.LineSegment(App.Vector( 0.0, 111.15, 0), App.Vector( 0.0,   4.50, 0)), False)  # west edge
    sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_lower, 0), vz, panel_pilot_dia/2), False)  # lower hole
    sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_upper, 0), vz, panel_pilot_dia/2), False)  # upper hole
    sk.Label = 'PWB (' + name + ')'  # relabel
    sk.Visibility = False  # show or hide PWB sketch

# part
bracket = doc.addObject('PartDesign::Body','Body')  # add body for entire part
bracket.Label = "Bracket"  # relabel

# vertices
v = {'Tabs':
    [
        [ -(panel_inner_face - panel_bend_inside_radius),
          panel_pwb_overlap,
          panel_pwb_overlap + panel_tab_radius,
          panel_x_both + panel_tab_length/2 - panel_tab_radius,
          panel_x_both + panel_tab_length/2 ],
        [ panel_y_lower - panel_tab_width/2,
          panel_y_lower - panel_tab_width/2 + panel_tab_radius,
          panel_y_lower + panel_tab_width/2 - panel_tab_radius,
          panel_y_lower + panel_tab_width/2,
          panel_y_lower + panel_tab_width/2 + panel_tab_radius,
          panel_y_upper - panel_tab_width/2 - panel_tab_radius,
          panel_y_upper - panel_tab_width/2,
          panel_y_upper - panel_tab_width/2 + panel_tab_radius,
          panel_y_upper + panel_tab_width/2 - panel_tab_radius,
          panel_y_upper + panel_tab_width/2 ],
    ],
    'BendForTabs':
    [
        [ -panel_outer_face,
          -panel_inner_face,
          -panel_inner_face + panel_bend_inside_radius ],
        [ -pwb_thickness-panel_thickness,
          -pwb_thickness,
          -pwb_thickness + panel_bend_inside_radius ],
    ],
    'Panel':
    [
        [ chassis_datum - OAL + bracket_tip_to_intercept,  # 5 bend
          chassis_datum - narrow_forty_five,  # narrow 45
          chassis_datum - narrow_forty_five + height_of_forty_five,  # end of 45
          panel_y_lower - panel_tab_width/2 - 2*panel_strain_relief,  # s1
          panel_y_lower + panel_tab_width/2 + 2*panel_strain_relief,  # s2
          panel_y_upper - panel_tab_width/2 - 2*panel_strain_relief,  # s3
          panel_y_upper + panel_tab_width/2 + 2*panel_strain_relief, ], # s4
# need weird stuff 
        [ 0,  # min
          0,  # lower tiny 45
          -pwb_thickness + panel_tab_to_upper - OAW,  # flange
          -pwb_thickness + panel_bend_inside_radius,  # strain relief
          -pwb_thickness + panel_tab_to_upper - height_of_forty_five - width_of_five_bend,  # 45
          -pwb_thickness + panel_tab_to_upper - height_of_forty_five,  # 45
          0,  # upper tiny 45
          -pwb_thickness + panel_tab_to_upper, ],
    ],
    }

# mounting tabs
name = 'Tabs'
thickness = panel_thickness
x = v[name][0]
y = v[name][1]
sk = doc.addObject('Sketcher::SketchObject', 'sketch' + name)  # create sketch
sk.Placement = App.Placement(App.Vector(0.00, 0.00, -pwb_thickness), planeXY)  # place sketch
sk.addGeometry(Part.LineSegment(App.Vector(x[0], y[0], 0),
                                App.Vector(x[3], y[0], 0)), False)  # south edge
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x[3], y[1], 0), vz, panel_tab_radius), Q3, Q0), False)  # corner arc
sk.addGeometry(Part.LineSegment(App.Vector(x[4], y[1], 0),
                                App.Vector(x[4], y[2], 0)), False)  # east edge, lower tab
sk.addGeometry(Part.LineSegment(App.Vector(x[4], y[2], 0),
                                App.Vector(x[3], y[3], 0)), True)  # r, diagonal
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x[3], y[2], 0), vz, panel_tab_radius), Q0, Q1), False)  # end of tab
sk.addGeometry(Part.LineSegment(App.Vector(x[3], y[3], 0),
                                App.Vector(x[2], y[3], 0)), False)  # cutout
sk.addGeometry(Part.LineSegment(App.Vector(x[2], y[3], 0),
                                App.Vector(x[1], y[4], 0)), True)  # r, diagonal
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x[2], y[4], 0), vz, panel_tab_radius), Q2, Q3), False)  # start of web
sk.addGeometry(Part.LineSegment(App.Vector(x[1], y[4], 0),
                                App.Vector(x[1], y[5], 0)), False)  # web
sk.addGeometry(Part.LineSegment(App.Vector(x[1], y[5], 0),
                                App.Vector(x[2], y[6], 0)), True)  # r, diagonal
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x[2], y[5], 0), vz, panel_tab_radius), Q1, Q2), False)  # end of web
sk.addGeometry(Part.LineSegment(App.Vector(x[2], y[6], 0),
                                App.Vector(x[3], y[6], 0)), False)  # cutout
sk.addGeometry(Part.LineSegment(App.Vector(x[3], y[6], 0),
                                App.Vector(x[4], y[7], 0)), True)  # r, diagonal
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x[3], y[7], 0), vz, panel_tab_radius), Q3, Q0), False)  # start of tab
sk.addGeometry(Part.LineSegment(App.Vector(x[4], y[7], 0),
                                App.Vector(x[4], y[8], 0)), False)  # east edge, upper tab
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x[3], y[8], 0), vz, panel_tab_radius), Q0, Q1), False)  # corner arc
sk.addGeometry(Part.LineSegment(App.Vector(x[3], y[9], 0),
                                App.Vector(x[0], y[9], 0)), False)  # north edge
sk.addGeometry(Part.LineSegment(App.Vector(x[0], y[9], 0),
                                App.Vector(x[0], y[0], 0)), False)  # west edge
sk.adjustRelativeLinks(bracket)  # start of sketch move to body
sk.Visibility = False  # hide sketch
bracket.ViewObject.dropObject(sk,None,'',[])  # end of sketch move to body
feature = bracket.newObject('PartDesign::Pad', name)  # create new Pad
feature.Profile = sk  # set Pad profile to sketch
feature.Length = thickness  # set thickness of Pad
feature.Reversed = 1  # extrude Pad downward

# tap and extrude
name = 'TapAndExtrude'
thickness = panel_TAE_length - panel_thickness
sk = doc.addObject('Sketcher::SketchObject', 'sketch' + name)  # create sketch
sk.Placement = App.Placement(App.Vector(0.00, 0.00, -pwb_thickness - panel_thickness), planeXY)
sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_lower, 0), vz, panel_TAE_OD/2), False)  # lower hole
sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_upper, 0), vz, panel_TAE_OD/2), False)  # upper hole
sk.adjustRelativeLinks(bracket)  # start of sketch move to body
sk.Visibility = False  # hide sketch
bracket.ViewObject.dropObject(sk,None,'',[])  # end of sketch move to body
feature = bracket.newObject('PartDesign::Pad','TapAndExtrude')  # create new Pad
feature.Profile = sk  # set Pad profile to sketch
feature.Length = thickness  # set thickness of Pad
feature.Reversed = 1  # extrude Pad downward

# mounting holes
name = 'Holes'
thickness = panel_TAE_length
sk = doc.addObject('Sketcher::SketchObject', 'sketch' + name)  # create sketch
sk.Placement = App.Placement(App.Vector(0.00, 0.00, -pwb_thickness), planeXY)  # place sketch
sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_lower, 0), vz, panel_pilot_dia/2), False)  # lower hole
sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_upper, 0), vz, panel_pilot_dia/2), False)  # upper hole
sk.adjustRelativeLinks(bracket)  # start of sketch move to body
sk.Visibility = False  # hide sketch
bracket.ViewObject.dropObject(sk,None,'',[])  # end of sketch move to body
feature = bracket.newObject('PartDesign::Pocket', name)  # create new Pocket
feature.Profile = sk  # set Pocket profile to sketch
feature.Length = thickness  # set thickness of Pocket
feature.Reversed = 0  # not sure why Pocket doesn't need to be reversed like Pad

# sheet metal bend for mounting tabs
name = 'BendForTabs'
thickness = panel_y_upper - panel_y_lower + panel_tab_width
x = v[name][0]
y = v[name][1]
sk = doc.addObject('Sketcher::SketchObject', 'sketch' + name)  # create sketch
sk.Placement = App.Placement(App.Vector(0.0, v['Tabs'][1][0], 0.0), planeXZ, v0)  # place sketch
# sk.addGeometry(Part.LineSegment(App.Vector(x[0], y[0], 0), App.Vector(x[-1], y[0], 0)), True)  # boundary
# sk.addGeometry(Part.LineSegment(App.Vector(x[-1], y[0], 0), App.Vector(x[-1], y[-1], 0)), True)  # boundary
# sk.addGeometry(Part.LineSegment(App.Vector(x[-1], y[-1], 0), App.Vector(x[0], y[-1], 0)), True)  # boundary
# sk.addGeometry(Part.LineSegment(App.Vector(x[0], y[-1], 0), App.Vector(x[0], y[0], 0)), True)  # boundary
sk.addGeometry(Part.LineSegment(App.Vector(x[2], y[0], 0), App.Vector(x[2], y[1], 0)), False)  # vertical
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x[2], y[2], 0), vz, panel_bend_inside_radius), Q2, Q3), False)  # inside radius
sk.addGeometry(Part.LineSegment(App.Vector(x[1], y[2], 0), App.Vector(x[0], y[2], 0)), False)  # horizontal
sk.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x[2], y[2], 0), vz, panel_bend_outside_radius), Q2, Q3), False)  # outside radius
sk.adjustRelativeLinks(bracket)  # start of sketch move to body
sk.Visibility = False  # hide sketch
bracket.ViewObject.dropObject(sk,None,'',[])  # end of sketch move to body
feature = bracket.newObject('PartDesign::Pad',name)  # create new Pad
feature.Profile = sk  # set Pad profile to sketch
feature.Length = thickness  # set thickness of Pad
feature.Reversed = 1  # extrude Pad downward

# panel
name = 'Panel'
thickness = panel_thickness
x = v[name][0]
y = v[name][1]
sk = doc.addObject('Sketcher::SketchObject', 'sketch' + name)  # create sketch
sk.Placement = App.Placement(App.Vector(-panel_outer_face, 0.0, 0.0), planeYZ)  # place sketch
sk.addGeometry(Part.LineSegment(App.Vector(x[6], y[3], 0), App.Vector(x[3], y[3], 0)), False)  # boundary
sk.addGeometry(Part.LineSegment(App.Vector(x[3], y[3], 0), App.Vector(x[3], y[2], 0)), False)  # boundary
sk.addGeometry(Part.LineSegment(App.Vector(x[3], y[2], 0), App.Vector(x[2], y[2], 0)), False)  # boundary
sk.addGeometry(Part.LineSegment(App.Vector(x[2], y[2], 0), App.Vector(x[1], y[4], 0)), False)  # boundary
sk.addGeometry(Part.LineSegment(App.Vector(x[1], y[4], 0), App.Vector(x[0], y[4], 0)), False)  # boundary
sk.addGeometry(Part.LineSegment(App.Vector(x[0], y[4], 0), App.Vector(x[0], y[5], 0)), False)  # boundary
sk.addGeometry(Part.LineSegment(App.Vector(x[0], y[5], 0), App.Vector(x[1], y[5], 0)), False)  # boundary
sk.addGeometry(Part.LineSegment(App.Vector(x[1], y[5], 0), App.Vector(x[2], y[7], 0)), False)  # boundary
sk.addGeometry(Part.LineSegment(App.Vector(x[2], y[7], 0), App.Vector(x[6], y[7], 0)), False)  # boundary
sk.addGeometry(Part.LineSegment(App.Vector(x[6], y[7], 0), App.Vector(x[6], y[3], 0)), False)  # boundary
sk.adjustRelativeLinks(bracket)  # start of sketch move to body
sk.Visibility = False  # hide sketch
bracket.ViewObject.dropObject(sk,None,'',[])  # end of sketch move to body
feature = bracket.newObject('PartDesign::Pad',name)  # create new Pad
feature.Profile = sk  # set Pad profile to sketch
feature.Length = thickness  # set thickness of Pad
feature.Reversed = 0  # extrude Pad inward

doc.recompute()  # redraw
Gui.SendMsgToActiveView("ViewFit")  # fit all
doc.saveAs(fn)  # save file for the first time

# end of CEM6-FH script
