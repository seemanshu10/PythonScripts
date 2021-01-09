#------------------------------------------------------------------------------------------------------------------------
# Automatic  leg rig in maya. 
# 
#
#-------------------------------------------------------------------------------------------------------------------------

#importing command files for python
import maya.cmds as cmds

def Fk_Ik_Leg_Tool():
    # Setup the Variables which could come from the UI
    
    
    # Is this the front or rear leg?
    isRearLeg = 0
    
    #How many joints are we working with?
    limbJoints = 4
    
    # use this information to start to generate the news we need 
    if isRearLeg:
        limbType= "rear"
        print "working in REAR Leg"
        
    else:
        limbType= "front"
        print "working in FRONT Leg"
    
    #check the selection is valid
    selectionCheck = cmds.ls(sl =1,type ="joint")
    
    #check if something is selected 
    if not selectionCheck:
        cmds.error("Please select any joint")
    else:
        jointRoot= cmds.ls(sl =1,type ="joint")[0]
     
 