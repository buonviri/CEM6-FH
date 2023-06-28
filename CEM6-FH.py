
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
panel_strain_relief = 0.5                # radius of strain relief notches

# defined in spec, do not edit
pwb_thickness = 1.57
panel_thickness = 0.86
panel_tab_to_upper = 17.15

# calculated from other parameters
panel_bend_outside = panel_bend_radius + panel_thickness
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

# PWB outline
for side in pwb_sides:
    sk = doc.addObject("Sketcher::SketchObject", "sketch_"+ side)  # create sketch for PWB boundary
    sk.Placement = App.Placement(App.Vector(0.00, 0.00, pwb_sides[side]), planeXY)  # place sketch
    sk.addGeometry(Part.LineSegment(App.Vector( 0.0,   4.50, 0), App.Vector(15.0,   4.50, 0)), False)  # south edge
    sk.addGeometry(Part.LineSegment(App.Vector(15.0,   4.50, 0), App.Vector(15.0, 111.15, 0)), False)  # east edge
    sk.addGeometry(Part.LineSegment(App.Vector(15.0, 111.15, 0), App.Vector( 0.0, 111.15, 0)), False)  # north edge
    sk.addGeometry(Part.LineSegment(App.Vector( 0.0, 111.15, 0), App.Vector( 0.0,   4.50, 0)), False)  # west edge
    sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_lower, 0), vz, panel_pilot_dia/2), False)  # lower hole
    sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_upper, 0), vz, panel_pilot_dia/2), False)  # upper hole
    sk.Label = 'PWB (' + side + ')'  # relabel
    sk.Visibility = True  # set to False to hide sketch

# part
bracket = doc.addObject('PartDesign::Body','Body')  # add body for entire part
bracket.Label = "Bracket"  # relabel

# vertices
v = {'bracket':
    [
        [ -(panel_inner_face - panel_bend_radius),
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
    }

# bracket area
x = v['bracket'][0]
y = v['bracket'][1]
name = 'Tabs'
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
feature.Length = panel_thickness  # set thickness of Pad
feature.Reversed = 1  # extrude Pad downward

# tap and extrude
name = 'TapAndExtrude'
sk = doc.addObject('Sketcher::SketchObject', 'sketch' + name)  # create sketch
sk.Placement = App.Placement(App.Vector(0.00, 0.00, -pwb_thickness - panel_thickness), planeXY)
sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_lower, 0), vz, panel_TAE_OD/2), False)  # lower hole
sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_upper, 0), vz, panel_TAE_OD/2), False)  # upper hole
sk.adjustRelativeLinks(bracket)  # start of sketch move to body
sk.Visibility = False  # hide sketch
bracket.ViewObject.dropObject(sk,None,'',[])  # end of sketch move to body
feature = bracket.newObject('PartDesign::Pad','TapAndExtrude')  # create new Pad
feature.Profile = sk  # set Pad profile to sketch
feature.Length = panel_TAE_length - panel_thickness  # set thickness of Pad
feature.Reversed = 1  # extrude Pad downward

# mounting holes
name = 'Holes'
sk = doc.addObject('Sketcher::SketchObject', 'sketch' + name)  # create sketch
sk.Placement = App.Placement(App.Vector(0.00, 0.00, -pwb_thickness), planeXY)  # place sketch
sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_lower, 0), vz, panel_pilot_dia/2), False)  # lower hole
sk.addGeometry(Part.Circle(App.Vector(panel_x_both, panel_y_upper, 0), vz, panel_pilot_dia/2), False)  # upper hole
sk.adjustRelativeLinks(bracket)  # start of sketch move to body
sk.Visibility = False  # hide sketch
bracket.ViewObject.dropObject(sk,None,'',[])  # end of sketch move to body
pholes = bracket.newObject('PartDesign::Pocket', name)  # create new Pocket
pholes.Profile = sk  # set Pocket profile to sketch
pholes.Length = panel_TAE_length  # set thickness of Pocket
pholes.Reversed = 0  # not sure why Pocket doesn't need to be reversed like Pad

doc.recompute()  # redraw
Gui.SendMsgToActiveView("ViewFit")  # fit all
doc.saveAs(fn)  # save file for the first time

# end of CEM6-FH script
