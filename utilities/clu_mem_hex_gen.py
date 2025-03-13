def hex_to_bin(hex_num):
    return bin(int(hex_num, 16))[2:].zfill(16)

def create_hashmap(addr, data):
    hashmap = {}
    for i in range(len(addr)):
        hashmap[addr[i]] = data[i]
    
    return hashmap

def create_hex_file(hashmap):
    with open('clu-hex.hex', 'w') as file:
        for i in range(128):
            k = f"0x{i:04X}"
            data = hashmap.get(k, "0x0000")
            file.write(data + '\n')
                


def main():
    addr = [
    "0x0040",
    "0x0050",
    "0x0048",
    "0x0058",
    "0x0060",
    "0x0068",
    "0x0078",
    "0x0070",
    "0x0000",
    "0x0002",
    "0x0003",
    "0x0001",
    "0x0004",
    "0x004C",
    "0x007F"
    ]
    data = [
    "0x3000",
    "0x3080",
    "0x3040",
    "0x7200",
    "0xBC00",
    "0x1CC8",
    "0x1D00",
    "0x2C04",
    "0x3000",
    "0x1080",
    "0x10C0",
    "0x1040",
    "0x1180",
    "0x9C01",
    "0x5202"
]
    m = create_hashmap(addr, data)
    output = create_hex_file(m)
    print(output)

if __name__ == "__main__":
    main()