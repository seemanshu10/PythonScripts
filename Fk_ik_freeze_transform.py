import maya.cmds as cmds

def Fk_Ik_grps():
    name_Cntrl=cmds.ls(sl=1)
    cmds.makeIdentity (apply =True, t=1, r=1, s=0, n=0, pn=1)
    cmds.group( )   
    name_grp=cmds.rename("group1",name_Cntrl)
    print (name_grp)

