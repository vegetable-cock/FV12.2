# 位置信息传进来，进行CRC32编码
def mycrc32(position):
    m_pdwCrc32Table = [0 for x in range(0,256)]
    dwPolynomial = 0xEDB88320;
    dwCrc = 0
    for i in range(0,255):
        dwCrc = i
        for j in [8,7,6,5,4,3,2,1]:
            if dwCrc & 1:
                dwCrc = (dwCrc >> 1) ^ dwPolynomial
            else:
                dwCrc >>= 1
        m_pdwCrc32Table[i] = dwCrc
    dwCrc32 = 0xFFFFFFFF
    for p in position:
        b = ord(p)
        dwCrc32 = ((dwCrc32) >> 8) ^ m_pdwCrc32Table[(b) ^ ((dwCrc32) & 0x000000FF)]
    dwCrc32 = dwCrc32 ^ 0xFFFFFFFF
    dwCrc32_bin = bin(dwCrc32)
    return dwCrc32_bin

print(mycrc32("03016613412000608151858269910"))