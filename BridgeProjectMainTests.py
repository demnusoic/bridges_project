####
# Date Created: 1.30.19
# Date Modified: 1.30.19
# Author: Nick Leyson
#
# This file contains unit tests for the SList class contained in BridgeProjectMain
#
####


import unittest
import BridgeProjectMain


class BridgeProjectMainTest(unittest.TestCase):

    def setUp(self):
        li = BridgeProjectMain.SList()

    def test_push_front(self):
        "It should add an item to the head of the list."
        li = BridgeProjectMain.SList()
        li.push_front("first")
        self.assertEqual(li.head.get_value(), "first")
        self.assertEqual(li.tail.get_value(), "first")
        li.push_front("second")
        li.push_front("third")
        self.assertEqual(li.head.get_value(), "third")
        self.assertEqual(li.head.get_next().get_value(), "second")
        self.assertEqual(li.head.get_next().get_next().get_value(), "first")
        self.assertEqual(li.tail.get_value(), "first")

    def test_push_back(self):
        "It should add an item to the tail of the list."
        li = BridgeProjectMain.SList()
        li.push_back("first")
        self.assertEqual(li.head.get_value(), "first")
        self.assertEqual(li.tail.get_value(), "first")
        li.push_back("second")
        li.push_back("third")
        self.assertEqual(li.head.get_value(), "first")
        self.assertEqual(li.head.get_next().get_value(), "second")
        self.assertEqual(li.head.get_next().get_next().get_value(), "third")
        self.assertEqual(li.tail.get_value(), "third")

    def test_pop_back(self):
        "It should remove an item from the tail of the list."
        li = BridgeProjectMain.SList()
        li.push_back("first")
        li.push_back("second")
        li.push_back("third")
        self.assertEqual(li.size, 3)
        self.assertEqual(li.tail.get_value(), "third")
        li.pop_back()
        self.assertEqual(li.size, 2)
        self.assertEqual(li.tail.get_value(), "second")
        li.pop_back()
        self.assertEqual(li.size, 1)
        self.assertEqual(li.tail.get_value(), "first")
        li.pop_back()
        self.assertTrue(li.empty())
        with self.assertRaises(Exception):
            li.pop_back()

    def test_pop_front(self):
        "It should remove an item from the head of the list."
        li = BridgeProjectMain.SList()
        li.push_front("first")
        li.push_front("second")
        li.push_front("third")
        self.assertEqual(li.size, 3)
        self.assertEqual(li.head.get_value(), "third")
        li.pop_front()
        self.assertEqual(li.size, 2)
        self.assertEqual(li.head.get_value(), "second")
        li.pop_front()
        self.assertEqual(li.size, 1)
        self.assertEqual(li.head.get_value(), "first")
        li.pop_front()
        self.assertTrue(li.empty())
        with self.assertRaises(Exception):
            li.pop_front()

    def test_get_prev(self):
        "When given a node, it should return the previous node in the list."
        li = BridgeProjectMain.SList()
        li.push_front("first")
        li.push_front("second")
        li.push_front("third")
        self.assertEqual(li.get_prev(li.tail).get_value(), "second")
        self.assertEqual(li.get_prev(li.head), None)

    def test_remove_node(self):
        "When given a node, it should remove the node from the list."
        li = BridgeProjectMain.SList()
        li.push_back("first")
        li.push_back("second")
        li.push_back("third")
        li.remove_node(li.head.get_next())
        self.assertEqual(li.head.get_next().get_value(), "third")
        li.remove_node(li.head)
        li.remove_node(li.tail)
        self.assertTrue(li.empty())

    def test_insert_after(self):
        "It should insert a new node with the given value after the given node."
        li = BridgeProjectMain.SList()
        li.push_back("first")
        li.insert_after(li.head, "second")
        self.assertEqual(li.tail.get_value(), "second")

        li = BridgeProjectMain.SList()
        li.push_back("first")
        li.push_back("third")
        li.insert_after(li.head, "second")
        self.assertEqual(li.head.get_next().get_value(), "second")

    def test_insert_before(self):
        "It should insert a new node with the given value before the given node."
        li = BridgeProjectMain.SList()
        li.push_back("first")
        li.insert_before(li.head, "second")
        self.assertEqual(li.head.get_value(), "second")

        li = BridgeProjectMain.SList()
        li.push_back("first")
        li.push_back("third")
        li.insert_before(li.tail, "second")
        self.assertEqual(li.head.get_next().get_value(), "second")

    def test_insert(self):
        "It should insert in desc alphabetical order."
        li = BridgeProjectMain.SList()
        li.insert("Aa")
        li.insert("Ab")
        li.insert("Ac")
        self.assertEqual(li.head.get_value(), 'Aa')
        self.assertEqual(li.head.get_next().get_value(), 'Ab')
        self.assertEqual(li.tail.get_value(), 'Ac')

    def test_get_actor_name(self):
        "It should return the actor's name when given a node."
        li = BridgeProjectMain.SList()
        li.insert_film("Kevin_Bacon_(I) Animal_House_(1978)".split(' '))
        li.insert_film("Winona_Ryder Being_John_Malkovich_(1999)".split(' '))
        self.assertEqual(li.get_actor_name(li.head), "Kevin_Bacon_(I)")
        self.assertEqual(li.get_actor_name(li.tail), "Winona_Ryder")

    def test_insert_film(self):
        "It should insert the actor and film, or add the film to the node value if the actor is already present."
        li = BridgeProjectMain.SList()
        li.insert_film("Kevin_Bacon_(I) Animal_House_(1978)".split(' '))
        self.assertEqual(li.head.get_value(), "Kevin_Bacon_(I)\nAnimal_House_(1978)")
        li.insert_film("Winona_Ryder Being_John_Malkovich_(1999)".split(' '))
        self.assertEqual(li.tail.get_value(), "Winona_Ryder\nBeing_John_Malkovich_(1999)")
        li.insert_film("Kevin_Bacon_(I) Air_Up_There,_The_(1994)".split(' '))
        self.assertEqual(li.head.get_value(), "Kevin_Bacon_(I)\nAnimal_House_(1978)\nAir_Up_There,_The_(1994)")

    def test_find_actor(self):
        "It should return a node for the actor or None if no matching node is found"
        li = BridgeProjectMain.SList()
        li.insert_film("Kevin_Bacon_(I) Animal_House_(1978)".split(' '))
        node = li.find_actor(("kevin bacon (I)".title().replace(" ", "_")))
        self.assertEqual(node, li.head)
        node = li.find_actor(("kevin bacon (XIV)".title().replace(" ", "_")))
        self.assertIsNone(node)

    def test_remove_actor(self):
        """ It should remove an actor when given their name.
            It should return True on success, False when actor is not found.
        """
        li = BridgeProjectMain.SList()
        li.insert_film("Kevin_Bacon_(I) Animal_House_(1978)".split(' '))
        removed = li.remove_actor(("kevin bacon (I)".title().replace(" ", "_")))
        self.assertTrue(removed)
        self.assertEqual(li.head, None)
        removed = li.remove_actor(("kevin bacon (I)".title().replace(" ", "_")))
        self.assertFalse(removed)

    def test_to_str(self):
        "It should return the value of each node separated by two new lines."
        li = BridgeProjectMain.SList()
        li.push_back("first")
        li.push_back("second")
        li.push_back("third")
        self.assertEqual(li.to_str(), "first\n\nsecond\n\nthird\n\n")


if __name__ == '__main__':
    unittest.main()
