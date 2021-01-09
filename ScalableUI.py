# -----------------------------------------------------------------------------------------------------------
# Create UI
#
# ------------------------------------------------------------------------------------------------------------

import maya.cmds as cmds


def AutoLimbToolUI():
    
    # First We Check if the window exists if it does,delete it 
    if cmds.window ("AutolimbToolUI",ex=1): cmds.deleteUI ("AutolimbToolUI")
    
    # Create the Window
    windows = cmds.window("AutolimbToolUI",t ="Auto Limb Tool v1.0", w=200, h=200, mnb=0 , mxb=0)
    
    # Show the Window
    cmds.showWindow (windows)

    # Choice to commit