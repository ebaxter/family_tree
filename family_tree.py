import numpy as np
import pdb
import matplotlib.pyplot as pl
import networkx as nx

class Person:

    def __init__(self):
        print "Person created"

def connect_tree(family_tree):
    for ii in xrange(0,len(family_tree)):
        aperson = family_tree[ii]
#        if (hasattr(aperson,'father')):
#            aperson.father.children = 2
    
def print_tree(family_tree):
    for ii in xrange(0,len(family_tree)):
        aperson = family_tree[ii]
        if hasattr(aperson, 'first_name'):
            print "Person: ", aperson.first_name

def get_node_name(person):
    if (0):
        output = ''
        if (hasattr(person,'first_name')):
            output += person.first_name
        if (hasattr(person,'last_name')):
            output += person.last_name
        return output
    if (1):
        if (not hasattr(person,'id')):
            print "id not found!"
            pdb.set_trace()
            print "name = ", person.first_name
        return person.id


class family_tree:
    def __init__(self):
        print "tree initialized"

    def read_tree(self, file):
        person_index = -1
        # First pass gets names and info
        with open(file,'r') as f:
            for line in f:
                if (line != '\n'):
                    split_index = line.find(' = ')
                    end_index = line.rfind('\'')
                    key = line[:split_index]
                    value = line[split_index+4:end_index]
                    if (key == 'id'):
                        new_person = Person()
                        person_index += 1
                        if (person_index != 0):
                            self.family_tree.append(new_person)
                        if (person_index == 0):
                            self.family_tree = [new_person]
                    if (key != 'father' and key != 'mother'):
                        setattr(self.family_tree[person_index],key,value)
        id_list = [self.family_tree[i].id for i in xrange(0,len(self.family_tree))]

        # Second pass sets up mother/father relationships
        person_index = -1
        with open(file,'r') as f:
            for line in f:
                if (line != '\n'):
                    split_index = line.find(' = ')
                    end_index = line.rfind('\'')
                    key = line[:split_index]
                    value = line[split_index+4:end_index]
                    if (key == 'id'):
                        person_index += 1
                    if (key == 'father' or key == 'mother'):
                        parent_index = id_list.index(value)
                        setattr(self.family_tree[person_index],key,self.family_tree[parent_index])

    def draw_tree_python(self):
        G = nx.Graph()
        # add people
        for ni in xrange(0,len(self.family_tree)):
            G.add_node(get_node_name(self.family_tree[ni]))
#            print "ni = ", ni
#            print "name = ", get_node_name(self.family_tree[ni])
        # Add father/mother relationships
        for ni in xrange(0,len(self.family_tree)):
#            print "bi = ", ni
#            print "name = ", self.family_tree[ni].first_name
            if (hasattr(self.family_tree[ni],'father')):
                G.add_edge(get_node_name(self.family_tree[ni]),get_node_name(self.family_tree[ni].father))
            if (hasattr(self.family_tree[ni],'mother')):
                G.add_edge(get_node_name(self.family_tree[ni]),get_node_name(self.family_tree[ni].mother))
        nx.draw(G)
        pdb.set_trace()


data_file = '../data/family_data.txt'

tree = family_tree()
tree.read_tree(data_file)
tree.draw_tree_python()

pdb.set_trace()

connect_tree(family_tree)
print_tree(family_tree)
draw_tree_python(family_tree)


pdb.set_trace()

