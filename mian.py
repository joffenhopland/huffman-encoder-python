import heapq
from collections import Counter


# Huffman tree node
class Node:
    def __init__(self, char, freq):
        self.char = char  # Character stored in the node
        self.freq = freq  # Frequency of the character
        self.left = None  # Left child
        self.right = None  # Right child

    # For heap operations we define a less than ('<') operator
    # The node with lower frequency will be considered 'smaller'
    def __lt__(self, other):
        return self.freq < other.freq


# Generate Huffman codes
def generate_huffman_codes(root, code, huffman_codes):
    if root is None:  # Base case: If root is None, return
        return

    # If it's a leaf node, store the Huffman code
    if root.left is None and root.right is None:
        huffman_codes[root.char] = code

    # Recursive calls for left and right subtrees
    generate_huffman_codes(root.left, code + "0", huffman_codes)
    generate_huffman_codes(root.right, code + "1", huffman_codes)


# Huffman encoding
def huffman_encoding(s):
    # Count frequency of each character
    frequency = Counter(s)

    # Initialize priority queue
    priority_queue = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    # Build the Tree
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)  # Node with smallest frequency
        right = heapq.heappop(priority_queue)  # Node with second smallest frequency

        # Create a new node with these two nodes as children and push it back into the queue
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(priority_queue, merged)

    # The remaining node is the root of the Tree
    root = heapq.heappop(priority_queue)

    # Generate Huffman codes using the Tree
    huffman_codes = {}
    generate_huffman_codes(root, "", huffman_codes)

    # Compress the string
    compressed_data = "".join([huffman_codes[char] for char in s])

    return compressed_data, huffman_codes, root


# Huffman decoding
def huffman_decoding(compressed_data, root):
    decoded_data = []  # To store the decompressed string
    current = root  # Initialize current node to the root

    # Decode the compressed data
    for bit in compressed_data:
        if bit == "0":
            current = current.left
        else:
            current = current.right

        # If leaf node, add character to the decoded data
        if current.left is None and current.right is None:
            decoded_data.append(current.char)
            current = root  # Reset the current node to root for the next character

    return "".join(decoded_data)


if __name__ == "__main__":
    s = "Huffman"
    compressed_data, huffman_codes, root = huffman_encoding(s)

    print("Huffman Codes:", huffman_codes)
    print("Compressed Data:", compressed_data)
    print("Original Size:", len(s) * 8, "bits")
    print("Compressed Size:", len(compressed_data), "bits")

    decoded_data = huffman_decoding(compressed_data, root)
    print("Decoded Data:", decoded_data)
