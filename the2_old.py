def justify_block(block):
    if (block[3]-block[1]) / (block[2]-block[0]) < 0:
        if block[2] < block[0]:
            return [block[2], block[1], block[0], block[3]]
        else:
            return [block[0], block[3], block[2], block[1]]
    else:
        return block

def get_area(block):
    return abs(block[0]-block[2]) * abs(block[1]-block[3])

def get_intersection_area(block1, block2):
    bl1_justified = justify_block(block1)
    bl2_justified = justify_block(block2)

    x_dist = min(bl1_justified[2], bl2_justified[2]) - max(bl1_justified[0], bl2_justified[0])
    y_dist = min(bl1_justified[3], bl2_justified[3]) - max(bl1_justified[1], bl2_justified[1])

    return x_dist * y_dist

def return_firmus(block1, block2):
    area = get_area(block1) + get_area(block2)
    return ["FIRMUS", area]

def return_addendum(down_block, up_block):
    return ["ADDENDUM"]

def return_damnare(block1, block2):
    intersect_area = get_intersection_area(block1, block2)

    area1 = get_area(block1)
    area2 = get_area(block2)

    total_area = area1 + area2

    if intersect_area > 0:
        total_area -= intersect_area

    return ["DAMNARE", total_area]

def is_on_top(down_block, up_block):
    y2_bottom = min(up_block[1], up_block[3])
    x2_bottom = up_block[up_block.index(y2_bottom)-1]
    y1_top = max(down_block[1], down_block[3])
    x1_max = max(down_block[0], down_block[2])
    x1_min = min(down_block[0], down_block[2])

    if y2_bottom == y1_top:
        return True
        #if x1_min <= x2_bottom <= x1_max:
        #    return True

    return False

def mass_center(block):
    return ((block[0]+block[2])/2, (block[1]+block[3])/2)

def is_firmus(block1, block2):
    _bl_is_down = [False, False]

    if (block1[1] == 0 or block1[3] == 0):
        down_block = block1
        up_block = block2
        _bl_is_down[0] = True
        print("Block 1 is down")

    if (block2[1] == 0 or block2[3] == 0):
        down_block = block2
        up_block = block1
        _bl_is_down[1] = True
        print("Block 2 is down")

    if sum(_bl_is_down) != 1:
        return return_damnare(block1, block2)

    print("Constraint I OK")

    if not is_on_top(down_block, up_block):
        return return_damnare(block1, block2)

    print("Constraint II OK")

    mc_up = mass_center(up_block)
    x1_max = max(down_block[0], down_block[2])
    x1_min = min(down_block[0], down_block[2])

    if not (x1_min <= mc_up[0] <= x1_max):
        return return_addendum(down_block, up_block)

    print("Constraint III OK")

    return return_firmus(block1, block2)

print(is_firmus([-0.5,10,-6,13],[-7,0,3,10]))
print(is_firmus([0.5,19,9.5,9],[3.8,9,5.5,0]))
print(is_firmus([-8,11,2,5],[1,0,-2,5]))
print(is_firmus([-7,5,7,10],[9.5,12.6,-1,10]))
print(is_firmus([-3,7,5,15],[-7,0,7,5]))
print(is_firmus([6,4,3.9,-1],[0.5,14.2,9.5,4]))
print(is_firmus([72.11457801300483, 0.0009278006095441509, 96.46821644264067, 11.41073681683352], [90.33338495031424, 11.41073681683352, 99.53782510601454, 51.757381633844034]))
