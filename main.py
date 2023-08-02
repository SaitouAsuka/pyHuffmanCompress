import mushroom
from utils import decompress, compress


# if __name__ == "__main__":
#     string = "agaskdfasdfasbkbvapdfgoadfjalkgnlasdjfol"
#     data = Counter(string)
#     huffman_tree = build_huffman_tree(data)
#     huffman_codes = dict()
#     generate_huffman_codes(huffman_tree, "", huffman_codes)
#     print(data)
#     print("Huffman Codes:", huffman_codes)
#     print("encoding seq: 1011001100")
#     print("decoding seq: {}".format(''.join(huffman_tree.search("1011001100"))))

def main(input, output, dec:bool=False):
    """
    对文件进行压缩或者解压

    @para:input:输入文件
    @para:output:输出文件
    @para:dec:是否为解压[flag]
    """
    if dec:
        decompress(input, output)
    else:
        compress(input, output)


if __name__ == "__main__":
    mushroom.Mushroom(main)