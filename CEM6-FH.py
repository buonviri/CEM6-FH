
fn = 'C:/EdgeCortix/CEM6/CEM6-FH.FCStd'  # set filename

panel_x_both = 7.50                      # x dimension of both PCIe bracket mounting holes
panel_y_lower = 9.35                     # y dimension of lower PCIe bracket mounting hole
panel_y_upper = 9.35 + 85.4              # y dimension of upper PCIe bracket mounting hole
panel_tab_width = 7.95                   # width of PCIe bracket mounting tab
panel_tab_length = panel_tab_width       # length (but really, half of this value past the mounting hole)
panel_tab_radius = 1.27                  # corner radius of PCIe bracket mounting tab

pwb_thickness = 1.57  # should not change

doc = App.newDocument()  # create empty doc

pwb = doc.addObject("Sketcher::SketchObject", "Sketch")  # create sketch for PWB boundary
pwb.addGeometry(Part.LineSegment(App.Vector( 0.0,   4.50, 0), App.Vector(15.0,   4.50, 0)), False)
pwb.addGeometry(Part.LineSegment(App.Vector(15.0,   4.50, 0), App.Vector(15.0, 111.15, 0)), False)
pwb.addGeometry(Part.LineSegment(App.Vector(15.0, 111.15, 0), App.Vector( 0.0, 111.15, 0)), False)
pwb.addGeometry(Part.LineSegment(App.Vector( 0.0, 111.15, 0), App.Vector( 0.0,   4.50, 0)), False)
pwb.Label = "PWB"

s = panel_y_lower - panel_tab_width/2
n = panel_y_upper + panel_tab_width/2
w = 0.0  # aligned with card edge
e = panel_x_both + panel_tab_length/2
tabs = doc.addObject("Sketcher::SketchObject", "Sketch")  # create sketch for tabs boundary
tabs.addGeometry(Part.LineSegment(App.Vector(w, s, 0), App.Vector(e, s, 0)), False)
tabs.addGeometry(Part.LineSegment(App.Vector(e, s, 0), App.Vector(e, n, 0)), False)
tabs.addGeometry(Part.LineSegment(App.Vector(e, n, 0), App.Vector(w, n, 0)), False)
tabs.addGeometry(Part.LineSegment(App.Vector(w, n, 0), App.Vector(w, s, 0)), False)
tabs.Label = "Tab Sketch"

bracket = doc.addObject('PartDesign::Body','Body')  # add body
bracket.Label = "Bracket"  # label body

tabs.adjustRelativeLinks(bracket)  # start of move (sketch to body)
bracket.ViewObject.dropObject(tabs,None,'',[])  # end of move (sketch to body)
ptabs = bracket.newObject('PartDesign::Pad','Tabs')  # create Pad
ptabs.Profile = tabs  # set profile to sketch
ptabs.Length = 0.68  # set thickness
ptabs.Reversed = 1  # extrude downward
tabs.Visibility = False  # hide sketch

doc.recompute()  # redraw

Gui.SendMsgToActiveView("ViewFit")  # fit all

doc.saveAs(fn)

# end of CEM6-FH
