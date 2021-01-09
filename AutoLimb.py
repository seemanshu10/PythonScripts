#------------------------------------------------------------------------------------------------------------------------
# Automatic  rig in maya. 
#
#
#-------------------------------------------------------------------------------------------------------------------------

#importing command files for python
import maya.cmds as cmds 

def autolimbTool():
    # Setup the variables which could come from the UI
    
    # Is this the front or rear leg?
    isRearLeg = 0
    
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
    pawControlName = limbName + "_MetaTarsus_ik_cntrl"
    tarsusControlName = limbName + "_Tarsus_ik_cntrl"
    #footControlName = limbName + "_Foot_ik_cntrl"
    femurControl = limbName + "_Femur_cntrl"
    pelvisControl = limbName + "_Pelvis_ik_cntrl"
    fibulaControl = limbName + "_Fibula_ik_cntrl"

    #-------------------------------------------------------------------------------------------------------
    
    # Build the list of joints we are working with ,using the root or first joint as a start point 
   
    # find its children 
    jointHierarchy = cmds.listRelatives(jointRoot,ad= 1,type ="joint")
   
    # add the selected joint into the front of the list
    jointHierarchy.append(jointRoot)
       
    # reverse the list 
    jointHierarchy.reverse() 
      
    # clear the selection 
    cmds.select(cl =1)
    
    #-------------------------------------------------------------------------------------------------------
    # Duplicate the main joint chain and rename each joint 
     
    # First define what joint chains we need 
    newJointList = ["_ik","_fk","_stretch"]
    
    # Add the extra driver joints 
    
    newJointList.append("_driver")
        
    #build the joint
    for newJoint in newJointList:
        for i in range (limbJoints):
            newJointName = jointHierarchy[i]+newJoint
            
            #print newJointName
            
            cmds.joint(n=newJointName)
            cmds.matchTransform(newJointName,jointHierarchy[i])
            cmds.makeIdentity(newJointName, a=1,t=0,r=1,s=0)
            
        cmds.select(cl=1)
        
    #--------------------------------------------------------------------------------------------------------------- 
    # contraints the main joints to the ik and fk joints so we can blend between them 
    
    for i in range(limbJoints):
        cmds.parentConstraint((jointHierarchy[i] + "_ik"),(jointHierarchy[i] + "_fk"),jointHierarchy[i],w=1,mo=0)

    #----------------------------------------------------------------------------------------------------------------
    # Setup FK

    # Connect the Fk Controls to the new joints 
    for i in range(limbJoints-1):
        cmds.parentConstraint((jointHierarchy[i] + "_fk_cntrl"),(jointHierarchy[i] + "_fk"),w=1,mo=0 )

    # ----------------------------------------------------------------------------------------------------------------
    # Setup IK

    # if its the rear leg,create the ik handle from the fibula to the metatarpus
   
    cmds.ikHandle(n=(limbName + "_fibula_ikHandle"),sol ="ikRPsolver",sj=(jointHierarchy[0] + "_ik"),ee=(jointHierarchy[2]+"_ik"))
    cmds.ikHandle(n=(limbName + "_metatarsus_ikHandle"),sol ="ikRPsolver",sj=(jointHierarchy[2] + "_ik"),ee=(jointHierarchy[4]+"_ik"))
    cmds.ikHandle(n=(limbName + "_ball_ikHandle"),sol ="ikSCsolver",sj=(jointHierarchy[4] + "_ik"),ee=(jointHierarchy[5]+"_ik"))
    cmds.ikHandle(n=(limbName + "_ball_end_ikHandle"),sol ="ikSCsolver",sj=(jointHierarchy[5] + "_ik"),ee=(jointHierarchy[6]+"_ik"))
        
    # create the tarsus cntrl offset group
    cmds.group((limbName + "_metatarsus_ikHandle"),n=(limbName + "_metatarsus_grp"))
    cmds.group((limbName + "_metatarsus_grp"),n=(limbName + "_metatarsus_cntrl_offset"))
    
    # find the 
    cmds.orientConstraint((limbName + "_MetaTarsus_ik_cntrl"),(limbName + "_MetaTarsus_ik"),mo=1)
    
    # Find the metatarsus pivot
    metatarsusPivot = cmds.xform(jointHierarchy[4],q=1,ws =1,piv=1) # xform is used for getting and setting the values
    
    # Set the pivot to match the metatarsus cntrl position grp 
    cmds.xform(((limbName + "_metatarsus_grp"),(limbName + "_metatarsus_cntrl_offset")),ws=1,piv=(metatarsusPivot[0],metatarsusPivot[1],metatarsusPivot[2]))
    
    # parent the ikhandle and the group to the foot control
    cmds.parent((limbName + "_metatarsus_cntrl_offset"),pawControlName)
    
    #pole contraints of tarsus and femur ik controls 
    cmds.poleVectorConstraint((limbName + "_Femur_ik_cntrl"),(limbName + "_fibula_ikHandle"))
    cmds.poleVectorConstraint((limbName + "_Tarsus_ik_cntrl"),(limbName + "_metatarsus_ikHandle"))
    
    # adding parent constraints fibula and pelvis ik cntrl to respective
    
    cmds.parentConstraint(pelvisControl,(limbName + "_Pelvis_ik"))
    cmds.parent((limbName + "_fibula_ikHandle"),fibulaControl) 
    #cmds.parent ((limbName + "_ik_grp"),"Rig_systems_grp")
     
    #-----------------------------------------------------------------------------------------------------------------
    # Add the IK and FK blending
    
    for i in range(limbJoints):
        getConstraint = cmds.listConnections(jointHierarchy[i],type ="parentConstraint")[0]
        getHeights = cmds.parentConstraint(getConstraint, q=1, wal=1)
        
        cmds.connectAttr(( mainControl + ".IK_FK_Switch" ),(getConstraint + "." + getHeights[0]), f =1 )
        cmds.connectAttr(( limbName + "_cntrl_switch.outputX" ), (getConstraint + "." + getHeights[1]) ,f=1)
        
        
    # Update the hierarchy 
    # Add a group for the limb 
    
    cmds.group( em =1,n=(limbName + "_grp"))
    
    # move it to the root position and freeze the transform 
    cmds.matchTransform ((limbName + "_grp"), jointRoot )
    cmds.makeIdentity ((limbName + "_grp"), a=1,t=1,r=1,s=0)
    
    # Parent the joints to the new group
    cmds.parent ( (jointRoot + "_ik"),(jointRoot + "_fk"),(jointRoot + "_stretch"),(limbName + "_grp"))
    
    cmds.parent (( jointRoot + "_driver" ),(limbName + "_grp"))
    cmds.parent ((limbName + "_grp"),"Rig_systems_grp")
    
    cmds.select (cl = 1)
    
    #selecting the metatarsus and 
    cmds.select ((limbName + "_MetaTarsus"),r=1)
    cmds.duplicate (n=(limbName + "_MetaTarsus"))
    cmds.matchTransform((limbName + "_MetaTarsus1"),(limbName + "_MetaTarsus"))
    cmds.parent(( limbName + "_MetaTarsus1") ,w=1)
    cmds.rename(( limbName + "_MetaTarsus1"),( limbName + "_Ankle"))
    
    cmds.setAttr(( limbName + "_fibula_ikHandle.visibility"),0)
    
    #parentcontoDelete = cmds.listRelatives(( limbName + "_Ankle"),ad=1)
    #parentcontoDelete=cmds.select(( limbName + "_MetaTarsus1"),ad= 1,type ="parentConstraint")
    #print parentcontoDelete
    #for i in parentcontoDelete:
        #cmds.delete (parentcontoDelete[0])
        #cmds.rename(parentcontoDelete[i],"prive")
    #cmds.rename(parentcontoDelete[0],"prive")
    #cmds.delete (parentcontoDelete[0])
    #cmds.rename()
    
    #cmds.select (( limbName + "_Ankle"),r=1)
    #cmds.pickWalk (d='down')
    #cmds.pickWalk (d='down')
    #cmds.pickWalk (d='down') 
    #d=cmds.pickWalk (d='down')
    #cmds.delete (d)
    
    #cmds.select(( limbName + "_Ankle")|( limbName + "_Foot")|( limbName + "_Foot_parentConstraint1")))