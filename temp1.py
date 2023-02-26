vaults = [1,2,3,4,5,6,7,8,9]
for i in range(0,len(vaults)):
    if vaults[i]>4:
        del vaults[i]
        continue
    else:
        pass

print(vaults)