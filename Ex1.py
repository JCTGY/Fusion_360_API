#Author-JC
#Description-Two circle

import adsk.core, adsk.fusion, adsk.cam, traceback

#def createParam(design, name, value, units, comment):
 #   userValue = adsk.core.ValueInput.createByString(value)
#    newParam = design.userParameters.add(name, userValue, units, comment)
#    
#    return newParam
    
Cir_R_I = 3
Cir_R_O = 13.1/2

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        o = sketch.originPoint
        
        #sketch.geometricConstraints_var.addCoincident(origin, Cir_In.centerSketchPoint)
        dims = sketch.sketchDimensions
        points = sketch.sketchPoints
        
        help(points)
        
        #createParam(design, "test", "10", "mm", "comment test")
        constraints = sketch.geometricConstraints
        
        # Draw bot two circles.
        circles = sketch.sketchCurves.sketchCircles
        _center_point=adsk.core.Point3D.create(0, 0, 0)
        center_point=points.add(_center_point)
        
        Cir_In = circles.addByCenterRadius(center_point, Cir_R_I)
        dims.addRadialDimension(Cir_In, adsk.core.Point3D.create(5, 3, 0))
        constraints.addCoincident(o, center_point)
        Cir_Out = circles.addByCenterRadius(Cir_In.centerSketchPoint, Cir_R_O)
        dims.addRadialDimension(Cir_Out, adsk.core.Point3D.create(10, 3, 0))
        Cir_Out.isConstruction = True
        Cir_In.isConstruction = True

       # Cir_Out = circles.addByCenterRadius(Cir_In.centerSketchPoint, Cir_R_O)
       # Draw the X_Y line
        lines = sketch.sketchCurves.sketchLines;
        x_line = lines.addByTwoPoints(adsk.core.Point3D.create(-Cir_R_O * 3, 0, 0), adsk.core.Point3D.create(Cir_R_O * 3, 0, 0))
        y_line = lines.addByTwoPoints(adsk.core.Point3D.create(0, -Cir_R_O * 3, 0), adsk.core.Point3D.create(0, Cir_R_O * 3, 0))
        constraints.addPerpendicular(x_line, y_line)
        constraints.addCoincident(o, x_line)        
        constraints.addCoincident(o, y_line)
        constraints.addVertical(y_line)
        x_line.isConstruction = True        
        y_line.isConstruction = True
        
        

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

