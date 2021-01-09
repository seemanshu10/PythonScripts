import maya.cmds as cmds

def Car_Create(name, length =2, width =1):
    #print ("Car Created")
    # creating Car Body
    body = create_body (length, width)
    tires = create_tires (length, width)
    
    final_name = assemble_car (name,body,tires)
    
    cmds.select (clear =True)
    return final_name
    
def create_body(length,width):
    body = cmds.polyPlane (w=length,h=width,name ="body")
    return body[0]
    
def create_tires(body_length, body_width):
    tire_width = 0.25 * body_width
    tire_radius = 0.25 * body_length
    x_pos = 0.5 * body_length
    z_pos = 0.5 * body_width + (0.5 * tire_width)
    
    f1_tire = create_tire("front_left_tire", tire_width, tire_radius, x_pos, 0, -z_pos)
    f2_tire = create_tire("front_right_tire", tire_width, tire_radius, x_pos, 0, z_pos)
    f3_tire = create_tire("rear_left_tire", tire_width, tire_radius, -x_pos, 0, -z_pos)
    f4_tire = create_tire("rear_right_tire", tire_width, tire_radius, -x_pos, 0, z_pos)
    
    return (f1_tire, f2_tire, f3_tire, f4_tire)
    
    
def create_tire(name, width, radius, tx, ty, tz):
    tire = cmds.polyCylinder (h =width, r=radius,ax= (0,0,1),sc =True,name = name)
    cmds.setAttr("{0}.translate".format(tire[0]), tx, ty, tz)
    return tire[0]    

def assemble_car (name,body,tires):
    body_grp = cmds.group (body, name ="body_grp")
    tire_grp = cmds.group (tires, name ="tires_grp")
    
    car_grp = cmds.group (body_grp, tire_grp,name =name)
    return car_grp

if __name__== "__main__":
    final_name = Car_Create("test_car")
    print ("Car Created: {0}".format(final_name)) 
    