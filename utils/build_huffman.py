from typing import Dict
import heapq
import utils.huffman_class as huffman_class


def build_huffman_tree(data:Dict[str, int]):

    heap = []

    for key, value in data.items():
        node = huffman_class.HuffNode(value)
        node.left = key
        node.isLeaf = True
        heapq.heappush(heap, node)
    
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merger_node = huffman_class.HuffNode(node1.value + node2.value)
        merger_node.left = node1
        merger_node.right = node2
        heapq.heappush(heap, merger_node)

    return heap[0]


def generate_huffman_codes(tree:huffman_class.HuffNode, code:str, codes:Dict[str, str]):
    if not tree:
        return 

    if tree.isLeaf:
        codes[tree.left] = code
    else:
        generate_huffman_codes(tree.left, code + "0", codes)
    
    generate_huffman_codes(tree.right, code + "1", codes)


