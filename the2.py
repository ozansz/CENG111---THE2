def justify_block(block):
    if (block[3]-block[1]) / (block[2]-block[0]) < 0:
        if block[2] < block[0]:
            #print "Justified:", [block[2], block[1], block[0], block[3]]
            return [block[2], block[1], block[0], block[3]]
        else:
            #print "Justified:", [block[0], block[3], block[2], block[1]]
            return [block[0], block[3], block[2], block[1]]
    else:
        #print "Justified:", block
        return block

def is_overlapping(block1, block2):
    bl1_justified = justify_block(block1)
    bl2_justified = justify_block(block2)

    if (bl1_justified[0] > bl2_justified[2]) or (bl2_justified[0] > bl1_justified[2]):
        return False

    if (bl1_justified[1] > bl2_justified[3]) or (bl2_justified[1] > bl1_justified[3]):
        return False

    return True

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
    #print "[CALL] return_addendum"
    mc_down = mass_center(down_block)
    mc_up = mass_center(up_block)

    bd_justified = justify_block(down_block)
    bu_justified = justify_block(up_block)

    if mc_up[0] > mc_down[0]:
        pivot = 2*bd_justified[2] - bu_justified[2]
        return ["ADDENDUM", [pivot, bu_justified[1], bu_justified[0], bu_justified[3]]]
    elif mc_up[0] < mc_down[0]:
        pivot = 2*bd_justified[0] - bu_justified[0]
        return ["ADDENDUM", [pivot, bu_justified[3], bu_justified[2], bu_justified[1]]]


def return_damnare(block1, block2):
    area1 = get_area(block1)
    area2 = get_area(block2)

    total_area = area1 + area2

    if is_overlapping(block1, block2):
        intersect_area = get_intersection_area(block1, block2)
        #print "Overlapping"
        #print "Intersect:", intersect_area
        total_area -= intersect_area

    return ["DAMNARE", total_area]

def is_on_top(down_block, up_block):
    y2_bottom = min(up_block[1], up_block[3])
    x2_max = max(up_block[0], up_block[2])
    x2_min = min(up_block[0], up_block[2])

    y1_top = max(down_block[1], down_block[3])
    x1_max = max(down_block[0], down_block[2])
    x1_min = min(down_block[0], down_block[2])

    if y2_bottom == y1_top:
        if (x2_min > x1_max) or (x2_max < x1_min):
            return False
        else:
            return True

    return False

def mass_center(block):
    return ((block[0]+block[2])/2.0, (block[1]+block[3])/2.0)

def is_firmus(block1, block2):
    #block1 = list(map(float, block1))
    #block2 = list(map(float, block2))

    #print "Block1:", block1
    #print "Block2:", block2

    _bl_is_down = [False, False]

    if (block1[1] < 0.001 or block1[3] < 0.001):
        down_block = block1
        up_block = block2
        _bl_is_down[0] = True
        #print "Block 1 is down"

    if (block2[1] < 0.001 or block2[3] < 0.001):
        down_block = block2
        up_block = block1
        _bl_is_down[1] = True
        #print "Block 2 is down"

    if sum(_bl_is_down) != 1:
        return return_damnare(block1, block2)

    #print "Constraint I OK"

    if not is_on_top(down_block, up_block):
        return return_damnare(block1, block2)

    #print "Constraint II OK"

    mc_up = mass_center(up_block)
    x1_max = max(down_block[0], down_block[2])
    x1_min = min(down_block[0], down_block[2])

    if not (x1_min <= mc_up[0] <= x1_max):
        return return_addendum(down_block, up_block)

    #print "Constraint III OK"

    return return_firmus(block1, block2)

print(is_firmus([-0.5,10,-6,13],[-7,0,3,10]))
print(is_firmus([0.5,19,9.5,9],[3.8,9,5.5,0]))
print(is_firmus([-8,11,2,5],[1,0,-2,5]))
print(is_firmus([-7,5,7,10],[9.5,12.6,-1,10]))
print(is_firmus([-3,7,5,15],[-7,0,7,5]))
print(is_firmus([6,4,3.9,-1],[0.5,14.2,9.5,4]))
print(is_firmus([72.11457801300483, 0.0009278006095441509, 96.46821644264067, 11.41073681683352], [90.33338495031424, 11.41073681683352, 99.53782510601454, 51.757381633844034]))
print(is_firmus([-57.30296954290279, -76.9556065246399, 35.123226833542525, -38.045075158958156], [94.9718151068868, 96.49881592323095, 98.34375538389037, 98.51750453720882]))
print(is_firmus([0,0,4,4],[0,0,2,2]))
print(is_firmus([0,0,4,4], [5,5,8,8]))
print(is_firmus([-57,-77,35,-38],[95,96,98,99]))
print(is_firmus([0,0,4,4], [-1,-1,-11,-11]))
print(is_firmus([0,0,4,4],[1,2,3,-6]))
print(is_firmus([44.90263592623438, 0.0006640932879104016, 75.86631697783034, 44.89076110759692],[60.107722876955016, 44.89076110759692, -72.38851549457394, 88.80605016354143]))
print(is_firmus([0,0,4,4],[4,4,8,8]))
