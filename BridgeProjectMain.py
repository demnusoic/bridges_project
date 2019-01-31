####
# Date Created: 1.25.19
# Date Modified: 1.31.19
# Author: Nick Leyson
# 
# This file contains: 
#    A singly linked list class utilizing the Bridges CS API
#       The class implements methods for working with the Bridges IMBD dataset
#    A main driver to edit the list through the command line and update the bridges visualizer
#
# Original assignment details: http://bridgesuncc.github.io/project_data/assignments/s15/1.pdf
# Generated bridges visualization: http://bridges-cs.herokuapp.com/assignments/0/nleyson
#
####


from bridges.bridges import *
from bridges.sl_element import *


class SList:
    """ A single linked list with methods for working with the bridges IMBD dataset.
        Internally all actor and movie names are stored with spaces represented as underscores.
    """

    def __init__(self):
        self.size = 0
        self.head = None
        self.tail = None
        self.current = None
        self.highlighted = None
        self.traversed_on_insert = 0

        self.default_node_color = "blue"
        self.current_node_color = "red"
        self.head_color = "orange"
        self.tail_color = "yellow"
        self.highlight_color = "green"

    def push_front(self, value):
        """ Create a new node with the given value,
            insert it at the head position.
        """
        node = SLelement(e=value)
        if self.size == 0:
            self.set_head(node)
            self.set_tail(node)
        else:
            node.set_next(self.head)
            self.set_head(node)
        self.size += 1
        return node

    def push_back(self, value):
        """ Create a new node with the given value,
            insert it at the tail position.
        """
        node = SLelement(e=value)
        if self.size == 0:
            return self.push_front(value)
        else:
            self.tail.set_next(node)
            self.set_tail(node)
        self.size += 1
        return node

    def empty(self):
        "Return true if the list is empty, else return false."
        if self.size == 0:
            return True
        else:
            return False

    def pop_front(self):
        "Remove the head node."
        if self.empty():
            raise Exception("List Empty")
        to_delete = self.head
        self.set_head(to_delete.get_next())
        del to_delete
        self.size -= 1

    def pop_back(self):
        "Remove the tail node."
        if self.empty():
            raise Exception("List Empty")
        to_delete = self.tail
        self.set_tail(self.get_prev(self.tail))
        if self.tail is not None:
            self.tail.set_next(None)
        else:
            self.head = None
        del to_delete
        self.size -= 1

    def get_prev(self, node):
        """ Return the node previous to the given node or None if
            there are no previous nodes.
        """
        if self.empty():
            raise Exception("List Empty")
        elif node == self.head:
            return None
        current = self.head
        while node != current.get_next():
            current = current.get_next()
        return current

    def remove_node(self, node):
        "Remove @node from the list."
        before = self.get_prev(node)
        after = node.get_next()
        if before is None:
            self.pop_front()
            return True
        elif after is None:
            self.pop_back()
            return True
        else:
            before.set_next(after)
        del node
        self.set_current(before)
        self.size -= 1
        return True

    def insert_after(self, before, value):
        "Insert a new node with @value after the node @before."
        if before.get_next() is None:
            return self.push_back(value)
        else:
            node = SLelement(e=value)
            after = before.get_next()
            before.set_next(node)
            node.set_next(after)
            self.size += 1
            self.set_current(node)
            return node

    def insert_before(self, after, value):
        "Insert a new node with @value before the node @after."
        if self.get_prev(after) is None:
            return self.push_front(value)
        else:
            node = SLelement(e=value)
            before = self.get_prev(after)
            before.set_next(node)
            node.set_next(after)
            self.size += 1
            self.set_current(node)
            return node

    def find_actor(self, actor_name):
        """ Find an entry for the actor based on their name.
            @actor_name (string): The actors name. Spaces should be represented
                as underscores. Case sensitive.
            @return: Return the SLelement of the actor or None if not found.
        """
        # iterate through elements
        current = self.head
        while current is not None:
            node_actor = self.get_actor_name(current)
            if node_actor == actor_name:
                return current
            current = current.get_next()
        return None

    def show_actor(self, actor_name):
        """ Highlight the actor in the visualization.
            @actor_name (string): The actors name. Spaces should be represented
                as underscores. Case sensitive.
            @return: True if the actor was found else false.
        """
        actor_node = self.find_actor(actor_name)
        if actor_node is not None:
            if self.highlighted is not None:
                # reset the original color for the current highlighted node
                if self.highlighted == self.head:
                    self.highlighted.get_visualizer().set_color(self.head_color)
                elif self.highlighted == self.tail:
                    self.highlighted.get_visualizer().set_color(self.tail_color)
                else:
                    self.highlighted.get_visualizer().set_color(self.default_node_color)
                self.highlighted = None
            actor_node.get_visualizer().set_color(self.highlight_color)
            self.highlighted = actor_node
            return True
        else:
            return False

    def get_actor_name(self, node):
        "Get the actors name from a node by obtaining the slelement's string value up to the first line break."
        return node.get_value()[0:node.get_value().find("\n")]

    def remove_actor(self, actor_name):
        """ Remove an entry for the actor based on their name.
            @actor_name (string): The actors name. Spaces should be represented
                as underscores. Case insensitive.
            @return: Return true if the actor is found and removed else false.
        """
        node = self.find_actor(actor_name)
        if node is None:
            return False
        else:
            self.remove_node(node)
            return True

    def insert(self, value):
        """Insert a new node into the list in desc order."""
        current = self.head
        if current is None:
            return self.push_front(value)
        while current is not None:
            self.traversed_on_insert += 1
            # Continue until a greater valued node is found, then insert a new node before it.
            if value < current.get_value():
                return self.insert_before(current, value)
            current = current.get_next()
        # If no greater value is found, then insert at the tail
        return self.push_back(value)

    def insert_film(self, actor_film):
        """ Insert an actor or film into the list. If the actor is not in the list, insert a new node for them.
            If the actor is in the list, append the film to their node's string.
            @actor_film (list): a tuple containing [ActorFirst_ActorLast, Film_Title]
        """
        actor_name = actor_film[0].strip()
        film_name = actor_film[1].strip()
        actor_node = self.find_actor(actor_name)
        if actor_node is None:
            actor_node = self.insert(actor_name)
        actor_node.set_value(actor_node.get_value()+"\n"+film_name)
        # update the node label
        actor_node.set_label(actor_node.get_value().replace("\n", "<br>").replace("_", " "))

    def to_str(self):
        """Generate a string representation of the object"""
        obj_str = ""
        current = self.head
        while current is not None:
            obj_str += str(current.get_value())+"\n\n"
            current = current.get_next()
        return obj_str

    def set_current(self, node):
        """ Set the visual parameters for the current node and reset the former current if needed.
            Head and tail should not be set as current.
        """
        if self.current is not None:
            self.current.get_visualizer().set_color(self.default_node_color)
        self.current = node
        self.current.get_visualizer().set_color(self.current_node_color)

    def set_head(self, node):
        "Set the head node and reset visual properties if needed."
        if node is None:
            self.head = None
            return True
        if self.head is not None:
            self.head.get_visualizer().set_color(self.default_node_color)
        self.head = node
        self.head.get_visualizer().set_color(self.head_color)
        return True

    def set_tail(self, node):
        "Set the tail node and reset visual properties if needed."
        if node is None:
            self.tail = None
            return True
        if self.tail is not None:
            self.tail.get_visualizer().set_color(self.default_node_color)
        self.tail = node
        self.tail.get_visualizer().set_color(self.tail_color)
        return True

    def update_visual(self):
        bridges = Bridges(0, "nleyson", "134563925230")
        bridges.set_data_structure(self.head)
        # Show the Json sent to the server
        bridges.set_visualize_JSON(True)
        bridges.visualize()


def main():
    """Read in 95 actors and their movies"""
    li = SList()

    # import raw actor data from the file
    with open("./dataset/large_imdb.txt", encoding="utf-8") as file:
        line = file.readline()
        while line and li.size <= 95:
            if line != "":
                li.insert_film(line.split(' '))
            line = file.readline()

    # accept command line input to find, add, and remove an actor
    li.update_visual()

    user_choice = ""
    while user_choice.capitalize() != "Exit":
        print("Enter one of the following commands or Exit to quit:\n"
              "Add: add an actor/movie pair\nRemove: remove an actor\nFind: find an actor's movie list\n")
        user_choice = input()
        if user_choice.capitalize() == "Add":
            actor_name = input("Enter the name of the actor appearing in the film\n")
            film_name = input("Enter the name of the film\n")
            actor_film = [actor_name.title().replace(' ', '_'), film_name.title().replace(' ', '_')]
            li.insert_film(actor_film)
            print("Actor added")
            li.update_visual()
        elif user_choice.capitalize() == "Remove":
            actor_name = input("Enter the name of the actor to remove from the list\n")
            removed = li.remove_actor(actor_name.title().replace(' ', '_'))
            if removed:
                print("Actor removed\n")
                li.update_visual()
            else:
                print("Actor not found\n")
        elif user_choice.capitalize() == "Find":
            actor_name = input("Enter the name of the actor\n")
            shown = li.show_actor(actor_name.title().replace(' ', '_'))
            if not shown:
                print("Actor not found\n")
            else:
                print("Actor Highlighted\n")
                li.update_visual()
        else:
            print("Command not recognized\n")


if __name__ == '__main__':
    main()
