def viso(year):
    if year % 4 == 0:
    
        if year % 100 == 0 and year % 400 != 0:
            return False
        
        else: return True

    return False

year = int(input())

print(viso(year))
