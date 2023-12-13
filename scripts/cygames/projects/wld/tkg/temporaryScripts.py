# world temporary scripts
from maya import cmds, mel

sel = cmds.ls(os=1, dag=1, type='joint')
for obj in sel:
    print(obj)


sel = cmds.ls(type='expression')
cmds.select(sel)


sel = cmds.ls(os=1, type='joint')
for obj in sel:
    cmds.color(rgb=[0, 0.5, 0.5])
