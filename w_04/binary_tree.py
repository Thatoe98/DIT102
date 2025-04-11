class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def inorder_traversal(root):
    """
    Performs an inorder traversal of a binary tree.

    Args:
        root: The root node of the binary tree.
    """
    if root:
        # Traverse the left subtree
        inorder_traversal(root.left)

        # Visit the current node
        print(root.data, end=" ")  # Or do whatever you want with the node's data

        # Traverse the right subtree
        inorder_traversal(root.right)



# Example usage:
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
root.right.left = Node(6)
root.right.right = Node(7)

print("Inorder traversal:")
inorder_traversal(root)  # Output: 4 2 5 1 6 3 7
print()  # Add a newline for better formatting


#Another example demonstrating an empty tree
empty_tree_root = None
print("Inorder traversal of an empty tree:")
inorder_traversal(empty_tree_root) #Output: (nothing printed)
print()



# Example using a different data type (e.g., characters)
char_root = Node('A')
char_root.left = Node('B')
char_root.right = Node('C')

print("Inorder traversal with characters:")
inorder_traversal(char_root) # Output: B A C
print()

# Example with just a single node
single_node_root = Node(100)
print("Inorder traversal of a single node tree:")
inorder_traversal(single_node_root) #Output: 100
print()