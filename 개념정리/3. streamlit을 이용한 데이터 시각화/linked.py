# Linked List class
# Node class
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    # Append a new node to the end of the list
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    # Prepend a new node to the beginning of the list
    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    # Delete a node with the given data
    def delete(self, data):
        if not self.head:
            return

        if self.head.data == data:
            self.head = self.head.next
            return

        current_node = self.head
        while current_node.next and current_node.next.data != data:
            current_node = current_node.next

        if current_node.next:
            current_node.next = current_node.next.next

    # Display the linked list
    def display(self):
        elements = []
        current_node = self.head
        while current_node:
            elements.append(str(current_node.data))
            current_node = current_node.next
        return " -> ".join(elements) if elements else "비어 있음"
