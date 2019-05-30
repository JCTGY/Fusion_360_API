#Author-JC
#Description-Two circle

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def createParam(design, name, value, units, comment):
   userValue = adsk.core.ValueInput.createByString(value)
   newParam = design.userParameters.add(name, userValue, units, comment)
   return newParam

Cir_R_O = 13.1/2
Cir_R_I = Cir_R_O / 13.1 * 6
Cir_R_TO = 3.1
Cir_R_TI = Cir_R_TO / 3.1 / 2 * 2.5
Curve_const = Cir_R_O / 13.1 * 20
Top_deg = 165
Bot_deg = 150

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
        lines = sketch.sketchCurves.sketchLines
        arcs = sketch.sketchCurves.sketchArcs


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

       # Cir_Out = circles.addByCenterRadius(Cir_In.centerSketchPoint, Cir_R_O)
       # Draw the X_Y line
        x_line = lines.addByTwoPoints(adsk.core.Point3D.create(-Cir_R_O * 4, 0, 0), adsk.core.Point3D.create(Cir_R_O * 4, 0, 0))
        y_line = lines.addByTwoPoints(adsk.core.Point3D.create(0, -Cir_R_O * 4, 0), adsk.core.Point3D.create(0, Cir_R_O * 4, 0))
        constraints.addPerpendicular(x_line, y_line)
        constraints.addCoincident(o, x_line)
        constraints.addCoincident(o, y_line)
        constraints.addVertical(y_line)
        x_line.isConstruction = True
        y_line.isConstruction = True
        
        # Set point of center of Circle
        #_Point_Curve = adsk.core.Point3D.create()
        # Top_point
        Point_TCurve = points.add(_center_point)
        constraints.addCoincident(Point_TCurve, y_line)
        constraints.addCoincident(Point_TCurve, Cir_Out)
        
        # Set 15 degree line
        line_top = lines.addByTwoPoints(Point_TCurve, adsk.core.Point3D.create(-Cir_R_O, Cir_R_O * 3, 0))
        line_top.isConstruction = True
        Top_angel = dims.addAngularDimension(line_top, y_line, adsk.core.Point3D.create(-10, -10, 0))       
        Top_angel.parameter.expression = "{} deg".format(Top_deg)
        
        # Set 30 deg line
        line_bot = lines.addByTwoPoints(Point_TCurve, adsk.core.Point3D.create(-Cir_R_O, -Cir_R_O * 3, 0))
        line_bot.isConstruction = True
        Bot_angel = dims.addAngularDimension(y_line, line_bot, adsk.core.Point3D.create(10, -10, 0))
        Bot_angel.parameter.expression = "{} deg".format(Bot_deg)
        
        
        # Set point for center of little circle at the bottom
        _Center_B_L = adsk.core.Point3D.create(-Cir_R_O, -Cir_R_O, 0)
        Center_B_L = points.add(_Center_B_L)
        constraints.addCoincident(Center_B_L, line_bot)
        len_bcir_center = dims.addDistanceDimension(Center_B_L, Point_TCurve, 0, adsk.core.Point3D.create(-5, -5, 0))
        len_bcir_center.parameter.expression = "{} cm".format(Curve_const)
        
       
        # Set the Arc of the construction line
        arc_cons = arcs.addByCenterStartSweep(Point_TCurve, Center_B_L, ((180 - (Top_deg + Bot_deg)) / 180 * math.pi ))
        constraints.addCoincident(arc_cons.centerSketchPoint, Point_TCurve)
        arc_cons.isConstruction = True
       
       # Set the Point Top
        _Big_Curve_point = adsk.core.Point3D.create(0, -Cir_R_O * 2, 0)
        Big_Curve_point = points.add(_Big_Curve_point)
        constraints.addCoincident(Big_Curve_point, y_line)
        len_Big_curve = dims.addDistanceDimension(Big_Curve_point, Point_TCurve, 0, adsk.core.Point3D.create(-3, -3, 0))
        len_Big_curve.parameter.expression = "{} cm".format(Cir_R_O * 2)
        
        # Draw the lower arc
        Big_curve = arcs.addByCenterStartSweep(Point_TCurve, Big_Curve_point, -Top_deg / 180 * math.pi)
        constraints.addCoincident(Big_curve.centerSketchPoint, Point_TCurve)
        
        # Draw Two Top circle
        _Point_Top_Cir = adsk.core.Point3D.create(-Cir_R_O, Cir_R_O, 0)
        Point_Top_Cir = points.add(_Point_Top_Cir)
        constraints.addCoincident(Point_Top_Cir, line_top)
        constraints.addCoincident(Point_Top_Cir, arc_cons)
        Cir_Top = circles.addByCenterRadius(Point_Top_Cir, Cir_R_TO)
        dims.addRadialDimension(Cir_Top, adsk.core.Point3D.create(-5, -5, 0))
        Cir_Top_In = circles.addByCenterRadius(Cir_Top.centerSketchPoint, Cir_R_TI)
        dims.addRadialDimension(Cir_Top_In, adsk.core.Point3D.create(-5, -10, 0))
        Cir_Top.isConstruction = True
        
        _Point_Mid_Cir = adsk.core.Point3D.create(-Cir_R_O *2 / 131 * 15.664, Cir_R_O *2 / 131 * 98.081, 0)
        Point_Mid_Cir = points.add(_Point_Mid_Cir)
        Cir_Mid = circles.addByCenterRadius(Point_Mid_Cir, Cir_R_O *2 / 131 * 33.823)
        Cir_Mid.isConstruction = True
        constraints.addTangent(Cir_Top, Cir_Mid)
        constraints.addTangent(Cir_Out, Cir_Mid)
        _Point_Mid_Y = adsk.core.Point3D.create(0, Cir_R_O *2 / 131 * 98.081, 0)
        Point_Mid_Y = points.add(_Point_Mid_Y)
        len_Mid_Y = dims.addDistanceDimension(Point_Mid_Y, center_point, 0, adsk.core.Point3D.create(-8, 8, 0))
        len_Mid_Y.parameter.expression = "{} cm".format(Cir_R_O * 2 / 131 * 98.081)
        constraints.addCoincident(Point_Mid_Y, y_line)
        len_Mid_center = dims.addDistanceDimension(Cir_Mid.centerSketchPoint, Point_Mid_Y, 0, adsk.core.Point3D.create(-8, 8, 0))
        len_Mid_center.parameter.expression = "{} cm".format(Cir_R_O * 2 / 131 * 15.664)
        
        # Set Connection Point
        _Point_CirO_M = adsk.core.Point3D.create(-Cir_R_O *2 / 131 * 15.664, Cir_R_O, 0)
        Point_CirO_M = points.add(_Point_CirO_M)
        constraints.addCoincident(Point_CirO_M, Cir_Mid)
        constraints.addCoincident(Point_CirO_M, Cir_Out)
        Curve_CirO = arcs.addByThreePoints(Big_Curve_point, adsk.core.Point3D.create(Cir_R_O, 0, 0), Point_CirO_M)
        dims.addRadialDimension(Curve_CirO, adsk.core.Point3D.create(5, -5, 0))
        
        _Point_CirT1 = adsk.core.Point3D.create(-Cir_R_O , Cir_R_O * 2, 0)
        Point_CirT1 = points.add(_Point_CirT1)
        constraints.addCoincident(Point_CirT1, Cir_Top)
        constraints.addCoincident(Point_CirT1, y_line)
        #_Point_CirT2 = adsk.core.Point3D.create(-Cir_R_O , Cir_R_O * 2, 0)
        #Point_CirT2 = points.add(_Point_CirT2)
        #constraints.addCoincident(Point_CirT2, Big_curve)
        #constraints.addCoincident(Point_CirT2, Cir_Top)
        _Point_CirT3 = adsk.core.Point3D.create(-Cir_R_O , Cir_R_O * 2, 0)
        Point_CirT3 = points.add(_Point_CirT3)
        constraints.addCoincident(Point_CirT3, Cir_Top)
        constraints.addCoincident(Point_CirT3, Cir_Mid)
        Curve_CirT = arcs.addByThreePoints(Big_curve.startSketchPoint, Point_CirT1.geometry, Point_CirT3)
        dims.addRadialDimension(Curve_CirT, adsk.core.Point3D.create(-Cir_R_O, Cir_R_O, 0))
        constraints.addCoincident(Curve_CirT.centerSketchPoint, Point_Top_Cir)
        #Tangent line for finding the point
        line_Mtan = lines.addByTwoPoints(adsk.core.Point3D.create(-Cir_R_O, Cir_R_I, 0), adsk.core.Point3D.create(-Cir_R_O, Cir_R_O + Cir_R_I, 0))
        constraints.addTangent(line_Mtan, Cir_Mid)
        constraints.addParallel(line_Mtan, y_line)
        _Point_MT_Cir = adsk.core.Point3D.create(-Cir_R_O, Cir_R_O + Cir_R_I, 0)
        Point_MT_Cir = points.add(_Point_MT_Cir)
        constraints.addCoincident(Point_MT_Cir, line_Mtan)
        constraints.addCoincident(Point_MT_Cir, Cir_Mid)
        Curve_MT = arcs.addByThreePoints(Curve_CirT.startSketchPoint, Point_MT_Cir.geometry, Point_CirO_M)
        constraints.addCoincident(Curve_MT.centerSketchPoint, Point_Mid_Cir)        
        

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

