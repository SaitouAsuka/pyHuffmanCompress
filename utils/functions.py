import six
from collections import Counter
from utils.build_huffman import build_huffman_tree, generate_huffman_codes


def write_int2bytes(out_f, number:int):
    a4 = number&255
    number = number>>8
    a3 = number&255
    number = number>>8
    a2 = number&255
    number = number>>8
    a1 = number&255
    out_f.write(six.int2byte(a1))
    out_f.write(six.int2byte(a2))
    out_f.write(six.int2byte(a3))
    out_f.write(six.int2byte(a4))


def read_int2bytes(data):
    a1 = data[0]
    a2 = data[1]
    a3 = data[2]
    a4 = data[3]
    j = 0
    j |= a1
    j <<= 8
    j |= a2
    j <<= 8
    j |= a3
    j <<= 8
    j |= a4
    return j, data[4:]


def chunck_save_8bit(data:str, output_f):
    idx = 0
    n = len(data)
    while idx + 8 <= n:
        out = 0
        for dx in range(8):
            out <<= 1
            if data[idx + dx] == '1':
                out |= 1
        
        output_f.write(six.int2byte(out))
        idx += 8
    return data[idx:] 


def convert2int(data):
    code = ""
    for ch in data:
        for _ in range(8):
            if ch & 128:
                code += '1'
            else:
                code += '0'
            ch <<= 1

    return code


def compress(input_file:str, output_file:str):
    with open(input_file, 'rb') as f:
        filedata = f.read()

    # 统计byte取值范围0-255的每个值得出现频率
    char_freq = Counter(filedata)
    length = len(char_freq)
    output_f = open(output_file, 'wb')

    # 一个int型得数有四个字节，所以分为四个字节写入输出文件中
    write_int2bytes(output_f, length)
    
    for key, value in char_freq.items():        
        output_f.write(six.int2byte(key))
        write_int2bytes(output_f, value)

    huffman_tree = build_huffman_tree(char_freq)
    huffman_codes = dict()
    generate_huffman_codes(huffman_tree, "", huffman_codes)


    code = ''
    for data in filedata:
        code += huffman_codes[data]
    
    code_len = len(code)

    write_int2bytes(output_f, code_len)
    code = chunck_save_8bit(code, output_f)
    if code:
        # 剩余不满8位的code
        code += "0" * (8 - len(code))
        chunck_save_8bit(code, output_f)
    
    output_f.close()


def decompress(input_file:str, output_file:str):
    with open(input_file, 'rb') as f:
        filedata = f.read()
    
    # 读取叶子节点的个数
    leaf_node_size, filedata = read_int2bytes(filedata)
    # 重新读取频率表
    char_freq = dict() 
    for _ in range(leaf_node_size):
        key = filedata[0]
        # print(key)
        filedata = filedata[1:]
        value, filedata = read_int2bytes(filedata)
        char_freq[key] = value

    # 根据频率表重构哈夫曼编码
    huffman_tree = build_huffman_tree(char_freq)
    huffman_codes = dict()
    generate_huffman_codes(huffman_tree, "", huffman_codes)

    # 获取压缩文件正体
    # 需要叫bytes转换为int
    code_len, filedata = read_int2bytes(filedata)
    data_stream = convert2int(filedata)[:code_len]

    with open(output_file, 'wb') as output_f:
        for ch in huffman_tree.search(data_stream):
            output_f.write(six.int2byte(ch))

