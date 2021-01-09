#-----------------------------------------------------------------------------------------------------------------------
#Stretchy limbs 
#-----------------------------------------------------------------------------------------------------------------------

import maya.cmds as cmds

def stretchyLimbs():
    # Setup the variables which could come from the UI    
    # Is this the front or rear leg?
    isRearLeg = 1
    
    #How many joints are we working with?
    limbJoints = 7
    
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
        
    # now we have a selected joint we can check for the prefix to see which side it is 
    whichSide =jointRoot[0:2]
    
    #make sure the prefix is usable 
    if not "L_" in whichSide:
        if not "R_" in whichSide:
            cmds.error("Please set a joint with a usable prefix of either L_ or R_")
            
    # Now build the names we need 
    
    limbName = whichSide +limbType

    mainControl = limbName + "_cntrl"
    metaControlName = limbName + "_MetaTarsus_ik_cntrl"

    #-------------------------------------------------------------------------------------------------------
    
    # Build the list of joints we are working with ,using the root or first joint as a start point 
   
    # find its children 
    jointHierarchy = cmds.listRelatives(jointRoot,ad= 1,type ="joint")
   
    # add the selected joint into the front of the list
    jointHierarchy.append(jointRoot)
       
    # reverse the list 
    jointHierarchy.reverse() 
    
    
    #------------------------------------------------------------------------------------------------------------    
    #Make Stretchy
    #------------------------------------------------------------------------------------------------------------
    
    #create the locator for te end of the leg
    space=cmds.spaceLocator( n=(limbName +"_stretchEndPos_loc"))
    # Move it to the end joint,and parent it to the new control
    cmds.matchTransform(space,jointHierarchy[4])
    cmds.parent(space,metaControlName)
    
    #Start to build the distance nodes 
    #First,We will need to add all the distance nodes together ,so we need a plusminusAverage node
    
    cmds.shadingNode("plusMinusAverage",au=1,n=(limbName +"_length"))
    
    #Build the distance nodes for each section
    for i in range(limbJoints-2):
        
        #if it is the last joint ignore or it will try to use the toes 
        if i is not limbJoints-3:
            cmds.shadingNode("distanceBetween",au=1,n=(jointHierarchy[i] +"_distnode"))
            
            cmds.connectAttr((jointHierarchy[i]+"_stretch.worldMatrix"),(jointHierarchy[i]+"_distnode.inMatrix1"),f=1)
            cmds.connectAttr((jointHierarchy[i+1]+"_stretch.worldMatrix"),(jointHierarchy[i]+"_distnode.inMatrix2"),f=1) 
            
            cmds.connectAttr((jointHierarchy[i]+"_stretch.rotatePivotTranslate"),(jointHierarchy[i]+"_distnode.point1"),f=1)
            cmds.connectAttr((jointHierarchy[i+1]+"_stretch.rotatePivotTranslate"),(jointHierarchy[i]+"_distnode.point2"),f=1) 
                 
            cmds.connectAttr((jointHierarchy[i]+"_distnode.distance"),(limbName +"_length.input1D["+str(i)+"]"),f=1) 
    
    # Now get the distance from the root to the stretch and locator - we use this to check the leg is stretching     
    cmds.shadingNode("distanceBetween",au=1,n=( limbName+"_stretch_distnode"))
            
    cmds.connectAttr((jointHierarchy[0]+"_stretch.worldMatrix"),(limbName+"_stretch_distnode.inMatrix1"),f=1)
    cmds.connectAttr((limbName+"_stretchEndPos_loc.worldMatrix"),(limbName+"_stretch_distnode.inMatrix2"),f=1) 
            
    cmds.connectAttr((jointHierarchy[0]+"_stretch.rotatePivotTranslate"),(limbName+"_stretch_distnode.point1"),f=1)
    cmds.connectAttr((limbName+"_stretchEndPos_loc.rotatePivotTranslate"),(limbName+"_stretch_distnode.point2"),f=1)
    
    #Create nedes to check for stretching,and to control how the stretch works
    
    #Scale factor compares the length of the leg with the stretch locator,so we can see when the leg is actually stretching 
    
    cmds.shadingNode("multiplyDivide",au=1,n=(limbName +"_scaleFactor"))
    
    #we use the condition node to pass this onto the joints,so the leg only stretches the way we want it to
    cmds.shadingNode("condition",au=1,n=(limbName +"_condition")) 
    
    #adjust the node settings
    cmds.setAttr ((limbName +"_scaleFactor.operation"),2)
    
    cmds.setAttr ((limbName +"_condition.operation"),2)
    cmds.setAttr ((limbName +"_condition.secondTerm"),1)
    cmds.setAttr ((limbName +"_condition.colorIfTrueR"),1)
    
    #Connect the stretch didtance to the scaleFactor multiply divide node
    cmds.connectAttr((limbName+"_stretch_distnode.distance"),(limbName+"_scaleFactor.input1X"),f=1)
    
    #Connect the stretch didtance to the scaleFactor multiply divide node
    cmds.connectAttr((limbName +"_length.output1D"),(limbName+"_scaleFactor.input2X"),f=1)
    
    #Connect the stretch didtance to the scaleFactor multiply divide node
    cmds.connectAttr((limbName+"_scaleFactor.outputX"),(limbName+"_condition.firstTerm"),f=1)
    
    #Also connect it to the color is true attribute,so we can use this as stretch value 
    cmds.connectAttr((limbName+"_scaleFactor.outputX"),(limbName+"_condition.colorIfTrueR"),f=1)
    
    # Now connect the stretch value to the ik and driver joints,so they stretch
    for i in range(limbJoints-1):
        cmds.connectAttr((limbName+"_condition.outColorR"),(jointHierarchy[i]+"_ik.scaleX"),f=1)
        
        # Also effect the driver skeleton, if this is the rear leg 
        if isRearLeg:
            cmds.connectAttr((jointHierarchy[i]+"_ik.scaleX"),(jointHierarchy[i]+"_driver.scaleX"),f=1)
    