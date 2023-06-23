
fn = 'C:/EdgeCortix/CEM6/CEM6-FH.FCStd'  # set filename

panel_x_both = 7.50                      # x dimension of both PCIe bracket mounting holes
panel_y_lower = 9.35                     # y dimension of lower PCIe bracket mounting hole
panel_y_upper = 9.35 + 85.4              # y dimension of upper PCIe bracket mounting hole
panel_tab_width = 7.95                   # width of PCIe bracket mounting tab
panel_tab_length = panel_tab_width       # length (but really, half of this value past the mounting hole)
panel_tab_radius = 1.27                  # corner radius of PCIe bracket mounting tab
panel_pilot_dia = 2.05                   # pilot hole diameter

pwb_thickness = 1.57  # should not change

doc = App.newDocument()  # create empty doc

pwb = doc.addObject("Sketcher::SketchObject", "Sketch")  # create sketch for PWB boundary
pwb.addGeometry(Part.LineSegment(App.Vector( 0.0,   4.50, 0), App.Vector(15.0,   4.50, 0)), False)  # south edge
pwb.addGeometry(Part.LineSegment(App.Vector(15.0,   4.50, 0), App.Vector(15.0, 111.15, 0)), False)  # east edge
pwb.addGeometry(Part.LineSegment(App.Vector(15.0, 111.15, 0), App.Vector( 0.0, 111.15, 0)), False)  # north edge
pwb.addGeometry(Part.LineSegment(App.Vector( 0.0, 111.15, 0), App.Vector( 0.0,   4.50, 0)), False)  # west edge
pwb.Label = "PWB"  # relabel
pwb.Visibility = False  # hide sketch

s = panel_y_lower - panel_tab_width/2  # min y
n = panel_y_upper + panel_tab_width/2  # max y
w = 0.0                                # aligned with card edge
e = panel_x_both + panel_tab_length/2  # max x
tabs = doc.addObject("Sketcher::SketchObject", "Sketch")  # create sketch for tabs boundary
tabs.addGeometry(Part.LineSegment(App.Vector(w, s, 0), App.Vector(e, s, 0)), False)  # south edge
tabs.addGeometry(Part.LineSegment(App.Vector(e, s, 0), App.Vector(e, n, 0)), False)  # east edge
tabs.addGeometry(Part.LineSegment(App.Vector(e, n, 0), App.Vector(w, n, 0)), False)  # north edge
tabs.addGeometry(Part.LineSegment(App.Vector(w, n, 0), App.Vector(w, s, 0)), False)  # west edge
tabs.Label = "Tab Sketch"  # relabel

bracket = doc.addObject('PartDesign::Body','Body')  # add body for entire part
bracket.Label = "Bracket"  # relabel

tabs.adjustRelativeLinks(bracket)  # start of sketch move to body
bracket.ViewObject.dropObject(tabs,None,'',[])  # end of sketch move to body
ptabs = bracket.newObject('PartDesign::Pad','Tabs')  # create new Pad
ptabs.Profile = tabs  # set Pad profile to sketch
ptabs.Length = 0.68  # set thickness of Pad
ptabs.Reversed = 1  # extrude Pad downward
tabs.Visibility = False  # hide sketch

doc.recompute()  # redraw

Gui.SendMsgToActiveView("ViewFit")  # fit all

doc.saveAs(fn)  # save file for the first time

# end of CEM6-FH script
