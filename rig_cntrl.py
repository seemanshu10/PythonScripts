# -----------------------------------------------------------------------------------------------------------
# Create GUI
#
# ------------------------------------------------------------------------------------------------------------
import maya.cmds as cmds

scriptName = __name__
newWindow = 'Auto_rigMaker'


def gui():
    if (cmds.window(newWindow, q=True, exists=True)):
        cmds.deleteUI(newWindow)
    if (cmds.windowPref(newWindow, q=True, exists=True)):
        cmds.windowPref(newWindow, r=True)

    myWindow = cmds.window(newWindow, t='Auto Arm Rig', w=180, h=320)
    main_Layout = cmds.columnLayout('Main Header')

    # naming options (option menu)
    cmds.text('naming_Text', l='Step 1: Set name options ')
    cmds.rowColumnLayout(nc=4, cw=[(1, 20), (2, 70), (3, 40), (4, 50)])
    cmds.text('oriText', label='Ori:')
    cmds.optionMenu('ori_Menu', changeCommand=scriptName + '.colorChange()')
    cmds.menuItem(label='left_')
    cmds.menuItem(label='right_')
    cmds.menuItem(label='centre_')

    cmds.text('labelText', label='Label:')
    cmds.optionMenu('Label_Menu')
    cmds.menuItem(label="arm")
    cmds.menuItem(label="leg")
    cmds.setParent(main_Layout)
    cmds.separator('name_sep', w=180, h=5)

    # set the rig type (radio button)
    cmds.text('rigType_Text', l='Step 2: Set rig type')
    cmds.radioButtonGrp("armType_Btn", labelArray3=('IK', 'FK', 'IK/FK'), numberOfRadioButtons=3,
                        columnWidth3=[50, 50, 50], select=3, cc=scriptName + '.armTypeVis()')
    cmds.separator("type_Sep", w=150, h=5)

    # set icon options (options menu)
    cmds.text('conSet_Text', l='Step 3: Set icon options ')
    cmds.rowColumnLayout(nc=2, cw=[(1, 90), (2, 80)])
    cmds.text('ikStyle_Text', label='IK Icon Style: ')
    cmds.optionMenu('ikIcon_Menu', cc=scriptName + '.iconChanger("ik")')
    cmds.menuItem(label="Box")
    cmds.menuItem(label="4 Arrows")
    cmds.menuItem(label="4 Pin")

    cmds.text('fkStyle_Text', label='FK Icon Style: ')
    cmds.optionMenu('fkIcon_Menu', cc=scriptName + '.iconChanger("fk")')
    cmds.menuItem(label="Circle")
    cmds.menuItem(label="Turn Arrows")

    cmds.text('handStyle_Text', label='Hand Icon Style: ')
    cmds.optionMenu('handIcon_Menu', cc=scriptName + '.iconChanger("hand")')
    cmds.menuItem(label="Circle")
    cmds.menuItem(label="COG")

    cmds.text('pvStyle_Text', label='PV Icon Style: ')
    cmds.optionMenu('pvIcon_Menu', cc=scriptName + '.iconChanger("pv")')
    cmds.menuItem(label="Diamond")
    cmds.menuItem(label="Arrow")

    cmds.setParent(main_Layout)
    cmds.button('testIcon_Btn', l="Make test icons to set scale", w=180, c=scriptName + ".armIconScale()")
    cmds.separator('style_Sep', w=180, h=5)

    # pick the color (iconTextButton and colorSlider)
    cmds.text('armSet_Text', l='Step 4: pick icon color ')
    cmds.gridLayout(nr=1, nc=5, cellWidthHeight=[35, 20])
    cmds.iconTextButton('darkBlue_Btn', bgc=[.000, .016, .373])
    cmds.iconTextButton('lightBlue_Btn', bgc=[0, 0, 1])
    cmds.iconTextButton('brown_Btn', bgc=[0.537, 0.278, .2])
    cmds.iconTextButton('red_Btn', bgc=[1, 0, 0])
    cmds.iconTextButton('yellow_Btn', bgc=[1, 1, 0])

    cmds.setParent(main_Layout)
    cmds.colorIndexSliderGrp('armColor', w=180, h=20, cw2=(150, 0), min=0, max=31, value=7)
    cmds.separator('color_Sep', w=180, h=5)

    # pole Vector options ( radio button)
    cmds.text('pv_Text', label='Step 5: Set IK elbow options')
    cmds.radioButtonGrp('addPVElbow_Btn', labelArray2=('Twist', 'PoleVector'), numberOfRadioButtons=2,
                        columnWidth2=[65, 85], select=2, cc=scriptName + ".pvChange()")
    cmds.separator('pv_Sep', w=180, h=5)

    cmds.button('final_Btn', l="Finalize the Rig", w=180, c=scriptName + ".armRigFinalize()")

    # displaying Window
    cmds.showWindow()

    # function for the color change for changing the orientation or ori


def colorChange():
    ori_opt = cmds.optionMenu('ori_Menu', q=True, sl=True)
    if ori_opt == 1:
        ori_color = 7
    if ori_opt == 2:
        ori_color = 14
    if ori_opt == 3:
        ori_color = 18
    cmds.colorIndexSliderGrp('armColor', e=True, v=ori_color)

    # function for switching on and off when changing setting rig type


def armTypeVis():
    armType = cmds.radioButtonGrp("armType_Btn", q=True, sl=True)
    if armType == 1:
        ik_val = 1
        fk_val = 0
        ikfk_val = 0

    if armType == 2:
        ik_val = 0
        fk_val = 1
        ikfk_val = 0

    if armType == 3:
        ik_val = 1
        fk_val = 1
        ikfk_val = 1

    cmds.text('ikStyle_Text', e=True, vis=ik_val)
    cmds.optionMenu('ikIcon_Menu', e=True, vis=ik_val)

    cmds.text('fkStyle_Text', e=True, vis=fk_val)
    cmds.optionMenu('fkIcon_Menu', e=True, vis=fk_val)

    cmds.text('handStyle_Text', e=True, vis=ikfk_val)
    cmds.optionMenu('handIcon_Menu', e=True, vis=ikfk_val)

    cmds.text('pvStyle_Text', e=True, vis=ik_val)
    cmds.optionMenu('pvIcon_Menu', e=True, vis=ik_val)

    cmds.text('pv_Text', e=True, vis=ik_val)
    cmds.radioButtonGrp('addPVElbow_Btn', e=True, vis=ik_val)

    cmds.separator('pv_Sep', e=True, vis=ik_val)

    # function to change the pv


def pvChange():
    pvType = (cmds.radioButtonGrp('addPVElbow_Btn', q=True, sl=True)) - 1
    if (cmds.objExists('ARM_PV_SCALE_TEST_DONT_DELETE') == True):
        cmds.setAttr('ARM_PV_SCALE_TEST_DONT_DELETE.v', pvType)


def iconChanger(icon_type):
    menu_opt = cmds.optionMenu(icon_type + 'Icon_Menu', q=True, sl=True)
    upper_Text = icon_type.upper()
    if (cmds.objExists('ARM_' + upper_Text + '_SCALE_TEST_DONT_DELETE') == True):
        shape_list = cmds.ls('ARM_' + upper_Text + '_SCALE_TEST_DONT_DELETE', dag=True, type='nurbsCurve')
        shape_len = len(shape_list)
        counter = 1
        while (counter < (shape_len + 1)):
            if (counter == menu_opt):
                cmds.setAttr(shape_list[counter - 1] + '.v', 1)
            else:
                cmds.setAttr(shape_list[counter - 1] + '.v', 0)
            counter = counter + 1


def armIconScale():
    global arm_RefRig_offset
    # variables Initialization
    armType = cmds.radioButtonGrp("armType_Btn", q=True, sl=True)
    ikShape = cmds.optionMenu('ikIcon_Menu', q=True, sl=True)
    fkShape = cmds.optionMenu('fkIcon_Menu', q=True, sl=True)
    pvShape = cmds.optionMenu('pvIcon_Menu', q=True, sl=True)
    handShape = cmds.optionMenu('handIcon_Menu', q=True, sl=True)
    pvType = (cmds.radioButtonGrp('addPVElbow_Btn', q=True, sl=True)) - 1

    selected = cmds.ls(sl=True, dag=True, type='joint')
    # check the selection is valid
    selectionCheck = cmds.ls(sl=1, type="joint")

    # check if something is selected
    if not selectionCheck:
        cmds.error("Please select any joint")
    # creating a temporary list
    transform_list = []
    icon_test_list = []

    # creating the ik icon
    # cube
    ik_box = cmds.curve(n='ik_arm_box_curve', d=1,
                        p=[(1, 1, -1), (1, 1, 1), (1, -1, 1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
                           (-1, -1, 1), (-1, 1, 1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, -1, 1),
                           (-1, -1, 1), (-1, 1, 1), (1, 1, 1)])

    # cmds.rename (ik_box, 'ik_arm_box_curve')
    ik_box_List = cmds.ls(ik_box, dag=True)

    # 4 Arrows
    ik_arrows = cmds.curve(n='ik_arm_4arrows_curve', d=1,
                           p=[(-1, 0, -3), (-2, 0, -3), (0, 0, -5), (2, 0, -3), (1, 0, -3), (1, 0, -1), (3, 0, -1),
                              (3, 0, -2), (5, 0, 0), (3, 0, 2), (3, 0, 1), (1, 0, 1), (1, 0, 3),
                              (2, 0, 3), (0, 0, 5), (-2, 0, 3), (-1, 0, 3), (-1, 0, 1), (-3, 0, 1), (-3, 0, 2),
                              (-5, 0, 0), (-3, 0, -2), (-3, 0, -1), (-1, 0, -1), (-1, 0, -3)])

    ik_arrows_List = cmds.ls(ik_arrows, dag=True)
    cmds.setAttr(ik_arrows_List[0] + '.rotateZ', -90)
    cmds.scale(0.2, 0.2, 0.2, ik_arrows_List[0], scaleXYZ=True)
    cmds.makeIdentity(ik_arrows_List[0], apply=True, t=1, r=1, s=1, pn=1)

    # 4 Pin
    ik_4pin = cmds.curve(n='ik_arm_4pin_curve', d=1,
                         p=[(0, 0, 0), (0, 0, -2), (-1, 0, -2), (-1, 0, -4), (1, 0, -4), (1, 0, -2), (0, 0, -2),
                            (0, 0, 0), (2, 0, 0), (2, 0, -1), (4, 0, -1), (4, 0, 1), (2, 0, 1), (2, 0, 0),
                            (0, 0, 0), (0, 0, 2), (1, 0, 2), (1, 0, 4), (-1, 0, 4), (-1, 0, 2), (0, 0, 2), (0, 0, 0),
                            (-2, 0, 0), (-2, 0, 1), (-4, 0, 1), (-4, 0, -1), (-2, 0, -1), (-2, 0, 0)])

    ik_4pin_List = cmds.ls(ik_4pin, dag=True)
    cmds.setAttr(ik_4pin_List[0] + '.rotateY', 90)
    cmds.scale(0.2, 0.2, 0.2, ik_4pin_List[0], scaleXYZ=True)
    cmds.makeIdentity(ik_4pin_List[0], apply=True, t=1, r=1, s=1, pn=1)

    # Empty Groups Creation to put all the shapes for contrls in the parent
    ik_cntrl = cmds.group(empty=True, n='ARM_IK_SCALE_TEST_DONT_DELETE')
    curveIK = cmds.parent(ik_box_List[1], ik_arrows_List[1], ik_4pin_List[1], ik_cntrl, r=True, s=True)
    transform_list.append(ik_box_List[0])
    transform_list.append(ik_arrows_List[0])
    transform_list.append(ik_4pin_List[0])

    # setting Visibility to just show what shape is selected in the UI

    if ikShape == 1:
        cmds.setAttr('curveShape2.v', 0)
        cmds.setAttr('curveShape3.v', 0)

    if ikShape == 2:
        cmds.setAttr('curveShape1.v', 0)
        cmds.setAttr('curveShape3.v', 0)
    if ikShape == 3:
        cmds.setAttr('curveShape1.v', 0)
        cmds.setAttr('curveShape2.v', 0)

    # positioning the control
    tempCONST = cmds.parentConstraint(selected[1], ik_cntrl, mo=False)
    cmds.delete(tempCONST)
    tempCONST = cmds.pointConstraint(selected[-1], ik_cntrl, mo=False)
    cmds.delete(tempCONST)
    cmds.parentConstraint(ik_cntrl, selected[-1], mo=True)
    icon_test_list.append(ik_cntrl)

    # create the FK Icon
    fk_circle = cmds.circle(n='fk_arm_circle_curve', c=(0, 0, 0), nr=(1, 0, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=1)[
        0]
    fk_circle_List = cmds.ls(fk_circle, dag=True)

    # 180 Arrows
    fk_turn = cmds.curve(n='fk_arm_turnarrows_curve', d=1, bez=False,
                         p=[(0, 0, 0), (0, 0, 1), (0, 0, 2), (1, 0, 2), (0, 0, 3), (-1, 0, 2), (0, 0, 2), (0, 0, 1),
                            (0, 0, 0), (0, 0, -1), (0, 0, -2), (-1, 0, -2), (0, 0, -3), (1, 0, -2), (0, 0, -2)])
    fk_turn_List = cmds.ls(fk_turn, dag=True)
    cmds.setAttr(fk_turn_List[0] + '.rotateY', -90)
    cmds.setAttr(fk_turn_List[0] + '.rotateX', 90)
    cmds.makeIdentity(fk_turn_List[0], apply=True, t=1, r=1, s=1, n=0, pn=1)

    # empty group creation
    fk_cntrl = cmds.group(empty=True, n='ARM_FK_SCALE_TEST_DONT_DELETE')
    cmds.parent(fk_circle_List[1], fk_turn_List[1], fk_cntrl, r=True, s=True)

    transform_list.append(fk_circle_List[0])
    transform_list.append(fk_turn_List[0])

    # visibility to switch off the controls which are not selected in the gui
    if fkShape == 1:
        cmds.setAttr('curveShape4.v', 0)
    if fkShape == 2:
        cmds.setAttr(fk_circle + 'Shape.v', 0)

    # positioning the cntrl
    tempCONST = cmds.parentConstraint(selected[0], fk_cntrl, mo=False)
    cmds.delete(tempCONST)
    tempCONST = cmds.parentConstraint(fk_cntrl, selected[0], mo=True)
    icon_test_list.append(fk_cntrl)

    # creating the PV Icon
    # pv diamond
    pvDmnd = cmds.curve(d=1, n='pv_dmnd_curve', p=[(0.00664267, -0.0106004, 1), (1, -0.00526262, 0), (0, 2, 0),
                                                   (0.00088465, -0.0106004, 1), (-1, -0.0106004, 0.0127566),
                                                   (-0.00050717, 2, 0), (0.00088465, -0.0106004, -1),
                                                   (-1, -0.0220406, 0),
                                                   (0.00088465, -0.0106004, -1), (1.000885, -0.0106004, 0),
                                                   (0.00176521, -2, -0.00452318), (0.00088465, -0.0106004, -1),
                                                   (0.00176921, -2, 0), (-1, -0.0106004, 0),
                                                   (0.00176771, -2, 0.00170249),
                                                   (-0.00080412, -0.0106004, 1)])
    pv_dmnd_List = cmds.ls(pvDmnd, dag=True)

    # pv Arrow creation
    pvArrow = cmds.curve(d=1, n='pv_arrow_curve',
                         p=[(-2, 0, -1), (1, 0, -1), (1, 0, -2), (3, 0, 0), (1, 0, 2), (1, 0, 1), (-2, 0, 1),
                            (-2, 0, -1)])
    pv_arrow_List = cmds.ls(pvArrow, dag=True)
    cmds.xform(pvArrow, pivots=[0, 0, 0], ws=True)
    cmds.makeIdentity(pv_arrow_List[0], apply=True, t=1, r=1, s=1, n=0, pn=1)

    # empty group creation
    pvIcon = cmds.group(empty=True, n='ARM_PV_SCALE_TEST_DONT_DELETE')
    cmds.parent(pv_dmnd_List[1], pv_arrow_List[1], pvIcon, r=True, s=True)

    transform_list.append(pv_dmnd_List[0])
    transform_list.append(pv_arrow_List[0])

    # shape curve name
    # visibility to switch off the controls which are not selected in the gui
    if pvShape == 1:
        cmds.setAttr('curveShape6.v', 0)
    if pvShape == 2:
        cmds.setAttr('curveShape5.v', 0)
    icon_test_list.append(pvIcon)

    # making hand controls
    # circle Creation
    handCircle = cmds.circle(n='hand_circle_curve', c=(0, 0, 0), nr=(1, 0, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=1)[0]
    handCircle_List = cmds.ls(handCircle, dag=True)
    cmds.setAttr(handCircle + '.rotateX', 90)
    cmds.makeIdentity(handCircle, apply=True, t=1, r=1, s=1, n=0, pn=1)

    # cog Creation
    handCOG = cmds.circle(n='hand_cog_curve', c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=16)[0]
    handCOG_List = cmds.ls(handCOG, dag=True)
    cmds.select(handCOG + ".cv[0]", handCOG + ".cv[2]", handCOG + ".cv[4]", handCOG + ".cv[6]", handCOG + ".cv[8]",
                handCOG + ".cv[10]", handCOG + ".cv[12]", handCOG + ".cv[14]")
    cmds.scale(0.480612, 0.480612, 0.480612)
    cmds.xform(handCOG, pivots=[0, 0, 0], ws=True)
    cmds.makeIdentity(handCOG, apply=True, t=1, r=1, s=1, n=0, pn=1)

    # empty group creation
    handIcon = cmds.group(empty=True, n='ARM_HAND_SCALE_TEST_DONT_DELETE')
    cmds.parent(handCircle_List[1], handCOG_List[1], handIcon, r=True, s=True)

    transform_list.append(handCircle_List[0])
    transform_list.append(handCOG_List[0])

    # visibility to switch off the controls which are not selected in the gui
    if handShape == 1:
        cmds.setAttr(handCOG + 'Shape.v', 0)
    if handShape == 2:
        cmds.setAttr(handCircle + 'Shape.v', 0)
    # positioning the control
    tempCONST = cmds.parentConstraint(selected[1], handIcon, mo=False)
    cmds.delete(tempCONST)
    tempCONST = cmds.parentConstraint(selected[-1], handIcon, mo=False)
    cmds.delete(tempCONST)
    icon_test_list.append(handIcon)

    # getting the pole vector location
    pvLoc = cmds.spaceLocator(p=(0, 0, 0), name='pv_local_loc')
    cmds.setAttr('pv_local_locShape.visibility', 0)
    pvgrp = cmds.group(pvLoc, name='pv_local_grp')
    pvoffset = cmds.group(pvIcon, name='pv_pos_grp')
    pvGrpMain = cmds.group(pvgrp, pvoffset, name='pv_main_grp')

    cmds.pointConstraint(selected[0], selected[-1], pvgrp, mo=False)
    cmds.aimConstraint(selected[0], pvgrp, mo=False, weight=1, aimVector=(1, 0, 0), upVector=(0, 1, 0),
                       worldUpType="objectrotation")
    cmds.pointConstraint(selected[1], pvLoc, skip=["y", "z"], mo=False)
    cmds.pointConstraint(selected[1], pvoffset, mo=False)
    cmds.parentConstraint(selected[0], pvGrpMain, mo=True)
    cmds.aimConstraint(pvLoc, pvoffset, mo=False, aimVector=(0, 0, 1), upVector=(0, 0, 1), worldUpType="objectrotation")

    for each in ['.tx', '.ty', '.rx', '.ry', '.rz']:
        cmds.setAttr(pvIcon + each, lock=True, keyable=False, channelBox=False)

    # visiblity for the main controls
    if armType == 1:
        cmds.setAttr(ik_cntrl + '.v', 1)
        cmds.setAttr(fk_cntrl + '.v', 0)
        cmds.setAttr(handIcon + '.v', 0)
        cmds.setAttr(pvIcon + '.v', pvType)
    if armType == 2:
        cmds.setAttr(ik_cntrl + '.v', 0)
        cmds.setAttr(fk_cntrl + '.v', 1)
        cmds.setAttr(handIcon + '.v', 0)
        cmds.setAttr(pvIcon + '.v', 0)
    if armType == 3:
        cmds.setAttr(ik_cntrl + '.v', 1)
        cmds.setAttr(fk_cntrl + '.v', 1)
        cmds.setAttr(handIcon + '.v', 1)
        cmds.setAttr(pvIcon + '.v', pvType)

    # parenting all the preset arm rig
    armRefOffset = cmds.group(empty=True, n='arm_RefRig_offset')
    cmds.parent(ik_cntrl, fk_cntrl, handIcon, pvGrpMain, armRefOffset)

    # deleting old transform nodes
    for each in transform_list:
        cmds.delete(each)

    # setting the cntrl in refrence to length of joint
    jointVal = cmds.getAttr(selected[1] + '.tx')
    finalVal = (jointVal / 8)
    for each in icon_test_list:
        cmds.scale(finalVal, finalVal, finalVal, each)

    # setup for switch to ik rig


def ikSetup(armType, oriName, labelName, iconColor, selected1):
    # variables initializations
    global ik_joints, ikIconPick, newPVIcon
    pvType = cmds.radioButtonGrp('addPVElbow_Btn', q=True, sl=True)

    if offset == 3:
        ik_joints = []
        new_dup = cmds.duplicate(selected1[0])
        dup_list = cmds.ls(new_dup, dag=True, type='joint')
        counter = 1
        for each in dup_list:
            new_name = cmds.rename(each, oriName + labelName + '_IK', str(counter) + 'Waist')
            ik_joints.append(new_name)
            counter = counter + 1
        else:
            ik_joints = selected1

    # set up the new ik control
    cmds.setAttr('ARM_IK_SCALE_TEST_DONT_DELETE.overrideEnabled', 1)
    cmds.setAttr('ARM_IK_SCALE_TEST_DONT_DELETE.overrideEnabled', (iconColor - 1))
    for each in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz']:
        cmds.setAttr('ARM_IK_SCALE_TEST_DONT_DELETE' + each, lock=False, channelBox=True)
        cmds.setAttr('ARM_IK_SCALE_TEST_DONT_DELETE' + each, keyable=True)
    findConst = cmds.listConnection('ARM_IK_SCALE_TEST_DONT_DELETE.tx')
    cmds.delete(findConst)
    cmds.makeIdentity('ARM_IK_SCALE_TEST_DONT_DELETE', apply=True, t=1, s=1, n=0, pn=1)
    ikIconPick = cmds.rename('ARM_IK_SCALE_TEST_DONT_DELETE', oriName + labelName + '_IK_icon')

    # ik Setup handle
    ikGrpTest = cmds.objExists('ikHandles_offset')
    if ikGrpTest == 0:
        ikHandles_offset = cmds.group(empty=True, n='ikHandles_offset')
    if ikGrpTest == 1:
        ikHandles_offset = 'ikHandles_offset'
    cmds.setAttr(ikHandles_offset + '.v', 0)
    ik = cmds.ikhandle(sj=ik_joints[0], ee=ik_joints[-1], sol="ikRPsolver", name=oriName + labelName + '_IK_Handle')
    cmds.seAttr(ik[0] + ".snapEnable", 0)
    cmds.parent(ikIconPick, w=True)

    # st up pole vector/Twist
    if pvType == 1:
        cmds.addAttr(ikIconPick, ln='PV_Twist', at='double', dv=0, k=True)
        cmds.connectAttr(ikIconPick + 'PV_Twist', ik[0] + '.twist', force=True)
    if pvType == 2:
        cmds.addAttr('ARM_PV_SCALE_TEST_DONT_DELETE.overrideEnabled', 1)
        cmds.addAttr('ARM_PV_SCALE_TEST_DONT_DELETE.overrideColor', (iconColor - 1))
        for each in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.v']:
            cmds.setAttr('ARM_PV_SCALE_TEST_DONT_DELETE' + each, lock=False, channelBox=True)
            cmds.setAttr('ARM_PV_SCALE_TEST_DONT_DELETE' + each, keyable=True)
        cmds.parent('ARM_PV_SCALE_TEST_DONT_DELETE', w=True)
        cmds.delete('pv1_main_pad')
        newPVIcon = cmds.rename('ARM_PV_SCALE_TEST_DONT_DELETE', oriName + labelName + '_PV_icon')
        cmds.makeIdentity(newPVIcon, apply=True, t=1, r=1, s=1, pn=1)

        cmds.poleVectorConstraint(newPVIcon, ik[0])
        for each in ['.tx', '.ty', '.tz', '.sx', '.sy', '.sz']:
            cmds.setAttr(newPVIcon + '.' + each, lock=True, keyable=False, channelBox=False)

    # connecting the ikHandle the icon
    cmds.parentConstraint(ikIconPick, ik[0], mo=True)
    cmds.parent(ik[0], ikHandles_offset)
    for each in [".sx", ".sx", ".sx"]:
        cmds.setAttr(ikIconPick + '.' + each, lock=True, keyable=False, channelBox=False)

    # setup for switch to fk rig


def fkSetup(offset, oriName, labelName, iconColor, selected1):
    # naming the joints
    if offset == 3:
        fk_joints = []
        new_dup = cmds.duplicate(selected1[0])
        dup_list = cmds.ls(new_dup, dag=True, type='joint')
        counter = 1
        for each in dup_list:
            new_name = cmds.rename(each, oriName + labelName + '_FK', str(counter) + 'Waist')
            fk_joints.append(new_name)
            counter = counter + 1
    else:
        fk_joints = cmds.ls(sl=True, dag=True, type='joint')

    # identifying the fk icon if it's there
    cmds.addAttr('ARM_FK_SCALE_TEST_DONT_DELETE.overrideEnabled', 1)
    cmds.addAttr('ARM_FK_SCALE_TEST_DONT_DELETE.overrideColor', (iconColor - 1))
    for each in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']:
        cmds.setAttr('ARM_FK_SCALE_TEST_DONT_DELETE' + each, lock=False, channelBox=True)
        cmds.setAttr('ARM_FK_SCALE_TEST_DONT_DELETE' + each, keyable=True)
    testScale = cmds.getAttr('ARM_FK_SCALE_TEST_DONT_DELETE.scaleY')
    findCONST = cmds.listConnections('ARM_FK_SCALE_TEST_DONT_DELETE.tx')
    cmds.delete(findCONST)
    cmds.makeIdentity('ARM_FK_SCALE_TEST_DONT_DELETE.scaleY', apply=True, t=1, r=1, s=1, n=0, pn=1)
    fkIconPick = cmds.rename('ARM_FK_SCALE_TEST_DONT_DELETE', oriName + labelName + '_FK1_icon')

    # offset the contrl
    fk1_offset = cmds.group(empty=True, name=oriName + labelName + '_FK1_control_offset0')
    temp_Const = cmds.parentConstraint(fk_joints[0], fk1_offset, mo=False)
    cmds.delete(temp_Const)
    cmds.parent(fkIconPick, fk1_offset)
    cmds.makeIdentity(fkIconPick, fk_joints[0])

    # create the 2nd control
    fk_dup = cmds.duplicate(fkIconPick)
    fk2_icon = cmds.parentConstraint(fk_dup[0], oriName + labelName + '_FK2_icon')
    fk2_offset = cmds.group(empty=True, name=oriName + labelName + '_FK1_control_offset0')

    temp_Const = cmds.parentConstraint(fk_joints[1], fk2_offset, mo=False)
    cmds.delete(temp_Const)
    cmds.parent(fk2_icon + '.t', (0, 0, 0))
    cmds.parent(fk2_icon + '.r', (0, 0, 0))
    cmds.makeIdentity(fk2_icon, fk_joints[1])

    for each in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']:
        cmds.setAttr(fk2_icon + '.' + each, lock=True, keyable=False, channelBox=False)
    cmds.parent(fk2_offset, fkIconPick)

    for each in ['tx', 'ty', 'tz', 'sx', 'sy', 'sz']:
        cmds.setAttr(fkIconPick + '.' + each, lock=True, keyable=False, channelBox=False)


# finalize the rig button
def armRigFinalize():
    # initialization
    armType = cmds.radioButtonGrp("armType_Btn", q=True, sl=True)
    selected1 = cmds.ls(dag=True, type='joint')
    oriName = cmds.optionMenu('ori_Menu', q=True, sl=True)
    labelName = cmds.optionMenu('Label_Menu', q=True, sl=True)
    iconColor = cmds.colorIndexSliderGrp('armColor', q=True, v=True)
    new_list = []
    print(oriName)
    # naming
    counter = 1
    for each in selected1:
        newJoint = cmds.rename(each, oriName + labelName + str(counter) + '_bind')
        counter = counter + 1
        new_list.append(newJoint)

    # print (new_list)
    waistName = new_list[-1].replace('_bind', '_waist')
    waistFinal = cmds.rename(new_list[0], waistName)
    selected = cmds.ls(new_list[0], dag=True, type='joint')

    # making a joint  offset
    offset = cmds.group(name=oriName + labelName + '_offset', empty=True)
    temp = cmds.pointConstraint(selected[0], offset, mo=False)
    cmds.delete(temp)
    cmds.makeIdentity(offset, apply=True, t=1, r=1, n=0, pn=1)
    cmds.parent(selected[0], offset)

    if armType == 1:
        ikSetup(armType, oriName, labelName, iconColor, selected1)
    if armType == 2:
        fkSetup(armType, oriName, labelName, iconColor, selected1)
    if armType == 3:
        ikSetup(armType, oriName, labelName, iconColor, selected1)
        fkSetup(armType, oriName, labelName, iconColor, selected1)

        # creating Switch
        ik_list = ik_joints
        fk_joints = fk_joints

        switchConst1 = cmds.orientConstraint(ik_list[0], fk_list[0], selected[0])
        switchConst2 = cmds.orientConstraint(ik_list[1], fk_list[1], selected[1])

        # adding hand icon and attr
        cmds.setAttr('ARM_HAND_SCALE_TEST_DONT_DELETE.overrideEnabled', 1)
        cmds.setAttr('ARM_HAND_SCALE_TEST_DONT_DELETE.overrideColor', (iconColor - 1))
        cmds.makeIdentity('ARM_HAND_SCALE_TEST_DONT_DELETE', apply=True, t=1, r=1, a=1, n=0, pn=1)
        handPick = cmds.rename('ARM_HAND_SCALE_TEST_DONT_DELETE', oriName + labelName + '_hand_icon')
        cmds.parent(handPick, w=True)
        cmds.addAttr(handPick, ln="IKFK_Switch", at='double', min=0, max=10, dv=0, k=True)

        sel_len = len(selected)
        counter = 0
        while (counter < (sel_len - 1)):
            cmds.setAttr(handPick + '.IKFK_Switch', 0)
            cmds.setAttr(selected[counter] + '_orientContraint1' + ik_list[counter] + 'W0', 1)
            cmds.setAttr(selected[counter] + '_orientContraint1' + fk_list[counter] + 'W1', 0)
            cmds.setDrivenKeyframe(selected[counter] + '_orientContraint1' + ik_list[counter] + 'W0',
                                   currentDriver=handPick + '.IKFK_Switch')
            cmds.setDrivenKeyframe(selected[counter] + '_orientContraint1' + fk_list[counter] + 'W1',
                                   currentDriver=handPick + '.IKFK_Switch')

            cmds.setAttr(handPick + '.IKFK_Switch', 10)
            cmds.setAttr(selected[counter] + '_orientContraint1' + ik_list[counter] + 'W0', 0)
            cmds.setAttr(selected[counter] + '_orientContraint1' + fk_list[counter] + 'W1', 1)
            cmds.setDrivenKeyframe(selected[counter] + '_orientContraint1' + ik_list[counter] + 'W0',
                                   currentDriver=handPick + '.IKFK_Switch')
            cmds.setDrivenKeyframe(selected[counter] + '_orientContraint1' + fk_list[counter] + 'W1',
                                   currentDriver=handPick + '.IKFK_Switch')

            cmds.setAttr(handPick + '.IKFK_Switch', 0)
            counter = counter + 1

        # adding the visibilty swap for ik and fk
        cmds.setAttr(handPick + '.IKFK_Switch', 0)
        cmds.setAttr(ikIconPick + '.visibility', 1)
        cmds.setAttr(newPVIcon + '.visibility', 1)
        cmds.setAttr(fk1_offset + '.visibility', 0)
        cmds.setDrivenKeyframe(fk1_offset + '.visibility', currentDriver=handPick + '.IKFK_Switch')
        cmds.setDrivenKeyframe(ikIconPick + '.visibility', currentDriver=handPick + '.IKFK_Switch')
        cmds.setDrivenKeyframe(newPVIcon + '.visibility', currentDriver=handPick + '.IKFK_Switch')
        cmds.setAttr(handPick + '.IKFK_Switch', 10)
        cmds.setAttr(ikIconPick + '.visibility', 0)
        cmds.setAttr(newPVIcon + '.visibility', 0)
        cmds.setAttr(fk1_offset + '.visibility', 1)
        cmds.setDrivenKeyframe(fk1_offset + '.visibility', currentDriver=handPick + '.IKFK_Switch')
        cmds.setDrivenKeyframe(ikIconPick + '.visibility', currentDriver=handPick + '.IKFK_Switch')
        cmds.setDrivenKeyframe(newPVIcon + '.visibility', currentDriver=handPick + '.IKFK_Switch')
        cmds.setAttr(handPick + '.IKFK_Switch', 0)

        cmds.setAttr(ikIconPick + '.visibility', lock=True, keyable=False, channelBox=False)
        cmds.setAttr(newPVIcon + '.visibility', lock=True, keyable=False, channelBox=False)

    # if(cmds.objExists(armRefOffset)==True)
    #   cmds.delete(armRefOffset)
        
