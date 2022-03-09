import meter

def overlapTest(l1, r1, l2, r2):
    # To check if either rectangle is actually a line
    # For example :  l1 ={-1,0}  r1={1,1}  l2={0,-1}  r2={0,1}
    print("me = " + str(l1[0]))

    if (l1[0] == r1[0] or l1[1] == r1[1] or l2[0] == r2[0] or l2[1] == r2[1]):
        # the line cannot have positive overlap
        print("a")
        return 0

    # If one rectangle is on left side of other
    if (l1[0] >= r2[0] or l2[0] >= r1[0]):
        print("b")
        return 0

    # If one rectangle is above other
    if (r1[1] >= l2[1] or r2[1] >= l1[1]):
        print("c" + str(r1[1]) + ":" + str(l2[1]) + ":")
        return 0

    print("d")
    return 1
