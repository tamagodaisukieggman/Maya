import maya.cmds as cmds

def create_curve_from_selected_objects():
    # Get selected objects
    selected_objects = cmds.ls(os=True, type='transform')
    if not selected_objects:
        cmds.error("No objects selected.")
        return
    
    # Get positions of selected objects
    positions = []
    for obj in selected_objects:
        pos = cmds.xform(obj, query=True, translation=True, worldSpace=True)
        positions.append(pos)
    
    # Create curve from positions with degree 1
    curve = cmds.curve(point=positions, degree=1)
    
    return curve

def apply_sweep_mesh_to_curve(curve):
    # Apply sweep mesh to the curve
    sweep_mesh = cmds.sweepMeshFromCurve(curve)
    
    # Get the shape node of the curve
    curve_shape = cmds.listRelatives(curve, shapes=True)[0]
    
    # Get the connection to the sweepMeshCreator node
    connections = cmds.listConnections(curve_shape + '.worldSpace[0]', source=False, destination=True, type='sweepMeshCreator')
    if not connections:
        cmds.error("No sweepMeshCreator node found.")
        return
    
    sweep_mesh_creator = connections[0]
    
    # Set the desired attributes
    cmds.setAttr(sweep_mesh_creator + '.interpolationMode', 2)
    cmds.setAttr(sweep_mesh_creator + '.interpolationSteps', 2)
    
    return sweep_mesh

def create():
    # Create curve from selected objects
    curve = create_curve_from_selected_objects()
    
    # Apply sweep mesh to curve
    sweep_mesh = apply_sweep_mesh_to_curve(curve)
    
    print(f"Sweep mesh created: {sweep_mesh}")

# Run the script
# main()
