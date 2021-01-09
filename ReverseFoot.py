#------------------------------------------------------------------------------------------------------------------------
# Automatic  rig in maya. 
# Reverse foot after deleting parent constraints on ankle
#
#-------------------------------------------------------------------------------------------------------------------------


#L_rear_Ball L_rear_Ball_end


#importing command files for python
import maya.cmds as cmds

def ReverseFoot():
    
    # Is this the front or rear leg?
    isRearLeg = 0
    
    #How many joints are we working with?
    limbJoints = 3
    
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
    ballendName = limbName + "_Ball_end"
    ballName = limbName + "_Ball"
    ankleName = limbName + "_Ankle"
    metaControlName = limbName + "_MetaTarsus_ik_cntrl"
    
    #selcting ballend joint and duplicate and renaming it 
    
    cmds.select (ballendName)
    heelName=cmds.duplicate (rr=0,n=(limbName+"_Heel"))
    
    #moving the heel joint in correct position
    cmds.move(  0, 0, -34.449414,r=1)
    cmds.parent( heelName,ballendName)
    
    #reeroot from the heel joint
    cmds.reroot( heelName) 
    
    #parent the heel joint to the foot ik control
    cmds.parent(heelName,metaControlName )
    
    #parenting the ikHandles to specific joints 
    cmds.parent((limbName + "_ball_ikHandle"),ballName)
    cmds.parent((limbName + "_ball_end_ikHandle"),ballendName)
    
    #parent the main ik handle to ankle joint so it moves with it 
    cmds.parent((limbName + "_metatarsus_ikHandle"),ballName)
    
    #group the ball_end ikhandle
    cmds.group((limbName + "_ball_end_ikHandle"),n=(limbName + "_ball_end_ikHandle")+"_grp")
    
    # Find the ballJoint pivot
    ballPivot = cmds.xform( ballName ,q=1,ws =1,piv=1) # xform is used for getting and setting the values
    
    # Set the pivot to match the metatarsus cntrl position grp 
    cmds.xform((limbName + "_ball_end_ikHandle_grp"),ws=1,piv=(ballPivot[0],ballPivot[1],ballPivot[2]))
    
    # group 2 times the heel joint for banking functionality
    cmds.group(heelName,n=(limbName + "_Bank_inner_grp"))
    cmds.group((limbName + "_Bank_inner_grp"),n=(limbName + "_Bank_outer_grp"))
    
    # Find the ballJoint pivot
    BankPivot = cmds.xform( heelName ,q=1,ws =1,piv=1) # xform is used for getting and setting the values
    
    # Set the pivot to match the bank grps 
    cmds.xform((limbName + "_Bank_inner_grp"),(limbName + "_Bank_outer_grp"),ws=1,piv=(BankPivot[0],BankPivot[1],BankPivot[2]))
    
    #moving the pivot of bank groups pivot to x axis:32.394744 z axis:20.396693
    cmds.move (32.394744,0,20.396693,(limbName + "_Bank_inner_grp.scalePivot"),(limbName + "_Bank_inner_grp.rotatePivot"),(limbName + "_Bank_outer_grp.rotatePivot"),(limbName + "_Bank_inner_grp.scalePivot"),r=1)
    cmds.move (-55.389316,0,0,(limbName + "_Bank_inner_grp.rotatePivot"),(limbName + "_Bank_inner_grp.scalePivot"),r=1)
    
    # selecting the metatarsus ik_cntrl
    cmds.select (metaControlName)
    attribute=cmds.ls(metaControlName)
    
    #adding attribute CONTROLS 
    for i in attribute:
        print (i)
        cmds.addAttr (i,longName="CONTROLS",at="enum",en="----------")
        cmds.setAttr (i+".CONTROLS",e=1,keyable =1,l=1)
        
        cmds.addAttr (i,longName="Bank",at="float")
        cmds.setAttr (i+".Bank",e=1,keyable =1)
        
        cmds.addAttr (i,longName="Heel_Twist",at="float")
        cmds.setAttr (i+".Heel_Twist",e=1,keyable =1)
        
        cmds.addAttr (i,longName="Toe_Twist",at="float")
        cmds.setAttr (i+".Toe_Twist",e=1,keyable =1)
        
        cmds.addAttr (i,longName="Toe_Tap",at="float")
        cmds.setAttr (i+".Toe_Tap",e=1,keyable =1)   
    
    # connect attributes with specific attibutes 
    cmds.connectAttr ((metaControlName+".Toe_Tap"),(limbName + "_ball_end_ikHandle_grp.rotateX"))
    cmds.connectAttr ((metaControlName+".Toe_Twist"),(limbName + "_Ball_end.rotateY"))
    cmds.connectAttr ((metaControlName+".Heel_Twist"),( limbName+"_Heel.rotateY"))
    
    # creating the condition node
    cmds.shadingNode ("condition",au =1,n=(limbName + "_MetaTarsus_ik_cntrl_condition"))
    
    # connecting the condition nodes with bank attribute
    cmds.connectAttr ((metaControlName+".Bank"),(limbName + "_MetaTarsus_ik_cntrl_condition.firstTerm"))
    
    #connecting attributes 
    cmds.connectAttr ((metaControlName+".Bank"),(limbName + "_MetaTarsus_ik_cntrl_condition.colorIfTrueR"),f=1)
    cmds.connectAttr ((metaControlName+".Bank"),(limbName + "_MetaTarsus_ik_cntrl_condition.colorIfFalseG"),f=1)
    
    cmds.setAttr ((limbName + "_MetaTarsus_ik_cntrl_condition.operation") ,2)
    cmds.setAttr ((limbName + "_MetaTarsus_ik_cntrl_condition.colorIfFalseB") ,0)
    cmds.setAttr ((limbName + "_MetaTarsus_ik_cntrl_condition.colorIfFalseR") ,0)
    
    cmds.connectAttr ((limbName + "_MetaTarsus_ik_cntrl_condition.outColorG"),(limbName + "_Bank_inner_grp.rotateZ"),f=1)
    cmds.connectAttr ((limbName + "_MetaTarsus_ik_cntrl_condition.outColorR"),(limbName + "_Bank_outer_grp.rotateZ"),f=1)
    
    # hiding the heel joint 
    cmds.setAttr ((limbName+"_Heel")+".visibility",0)
    
    # add Attr
    cmds.addAttr (i,longName="ROLL",at="enum",en="----------")
    cmds.setAttr (i+".ROLL",e=1,keyable =1,l=1)
    
    # add attr for footRoll
    cmds.addAttr (i,longName="Foot_Roll",at="float",defaultValue=0.0, minValue=-10.0, maxValue=10.0)
    cmds.setAttr (i+".Foot_Roll",keyable =1)
    
    #Setting drivenkey on heel ,ball_end,Ball for foot roll
    cmds.select ((limbName + "_Ball"),r=1)
    cmds.setDrivenKeyframe (at="rotateZ",cd=metaControlName+".Foot_Roll", dv=0,v=0)
    
    cmds.select ((limbName + "_Ball_end"),r=1)
    cmds.setDrivenKeyframe (at="rotateX",cd=metaControlName+".Foot_Roll", dv=0,v=0)
    
    cmds.select ((limbName + "_Heel"),r=1)
    cmds.setDrivenKeyframe (at="rotateX",cd=metaControlName+".Foot_Roll", dv=0,v=0)
    
    #setting values for footRoll value 10
    
    cmds.select ((limbName + "_Ball"),r=1)
    cmds.setDrivenKeyframe (at="rotateZ",cd=metaControlName+".Foot_Roll", dv=10,v=-45)
    
    cmds.select ((limbName + "_Ball_end"),r=1)
    cmds.setDrivenKeyframe (at="rotateX",cd=metaControlName+".Foot_Roll", dv=10,v=0)
    
    cmds.select ((limbName + "_Heel"),r=1)
    cmds.setDrivenKeyframe (at="rotateX",cd=metaControlName+".Foot_Roll", dv=10,v=-75)
    
    #setting values for footRoll value -5
    
    cmds.select ((limbName + "_Ball"),r=1)
    cmds.setDrivenKeyframe (at="rotateZ",cd=metaControlName+".Foot_Roll", dv=-5,v=-75)
    
    cmds.select ((limbName + "_Ball_end"),r=1)
    cmds.setDrivenKeyframe (at="rotateX",cd=metaControlName+".Foot_Roll", dv=-5,v=0)
    
    cmds.select ((limbName + "_Heel"),r=1)
    cmds.setDrivenKeyframe (at="rotateX",cd=metaControlName+".Foot_Roll", dv=-5,v=0)
    
    
    #setting values for footRoll value -10
    
    cmds.select ((limbName + "_Ball"),r=1)
    cmds.setDrivenKeyframe (at="rotateZ",cd=metaControlName+".Foot_Roll", dv=-10,v=-15)
    
    cmds.select ((limbName + "_Ball_end"),r=1)
    cmds.setDrivenKeyframe (at="rotateX",cd=metaControlName+".Foot_Roll", dv=-10,v=30)
    
    cmds.select ((limbName + "_Heel"),r=1)
    cmds.setDrivenKeyframe (at="rotateX",cd=metaControlName+".Foot_Roll", dv=-10,v=0)
    
    '''jointHierarchy = cmds.listRelatives((limbName + "_Heel"),ad= 1,type ="joint")
    jointHierarchy.append((limbName + "_Heel"))
    jointHierarchy.reverse()
    jointHierarchy.pop(3)
    print jointHierarchy
    d=[0,10,-5,-10]
    for i in range (3):
        print jointHierarchy[i]
        cmds.select (jointHierarchy[i],r=1)
        cmds.setDrivenKeyframe (at="rotateZ",cd=metaControlName+".Foot_Roll", dv=-10,v=-15)
    
        cmds.select ((limbName + "_Ball_end"),r=1)
        cmds.setDrivenKeyframe (at="rotateX",cd=metaControlName+".Foot_Roll", dv=-10,v=30)
    
        cmds.select ((limbName + "_Heel"),r=1)
        cmds.setDrivenKeyframe (at="rotateX",cd=metaControlName+".Foot_Roll", dv=-10,v=0)
        i+=1'''  
    
    
     