def swap(a,b,array):
    array[a], array[b]=array[b],array[a]
    return array

def pick(array):
    first=array[0]
    last=array[-1]
    mid=array[round(len(array)/2)]

    if first<=last>=mid<=first or first>=last<=mid>=first:
        swap(0,-1,array)
    elif mid<=first>=last<=mid or mid>=first<=last>=mid:
        swap(round(len(array)/2),-1,array)
    return array

def quicksort(array):
    last=array[-1]
    itemsleft, itemsright=[],[]
    count=0
    for i in range(len(array)):
        print(array)
        if array[i]>last:
            itemsleft.append(i)
        if array[i*-1]<last and i!=0:
            itemsright.append(i*-1)
        if itemsleft!=[]and itemsright!=[] and not count > len(itemsleft) and not count > len(itemsright):
            print(len(array)+itemsright[count])
            if count+1<=len(itemsleft) and count+1<=len(itemsright):
                count+=1
    print(array)

tester=[81,2,122,4,11]
quicksort(tester)
