import numpy as np
import pdb
import networkx as nx
import json

def print_tree(family_tree):
    for ii in xrange(0,len(family_tree)):
        aperson = family_tree[ii]
        if hasattr(aperson, 'first_name'):
            print "Person: ", aperson.first_name

class Person:
    def __init__(self):
        #print "Person created"
        self.id = -1

    def get_dict(self):
        dict_data = {'id':self.id}
        if (hasattr(self,'first_name')):
            dict_data['first_name'] = self.first_name
        if (hasattr(self,'father')):
            dict_data['father'] = self.father.id
        if (hasattr(self,'mother')):
            dict_data['mother'] = self.mother.id
        if (hasattr(self,'generation_number')):
            dict_data['generation_number'] = self.generation_number
        return dict_data

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
            G.add_node(self.family_tree[ni].id)
        # Add father/mother relationships
        for ni in xrange(0,len(self.family_tree)):
            if (hasattr(self.family_tree[ni],'father')):
                G.add_edge(self.family_tree[ni].id,self.family_tree[ni].father.id)
            if (hasattr(self.family_tree[ni],'mother')):
                G.add_edge(self.family_tree[ni].id,self.family_tree[ni].mother.id)
        nx.draw(G)

    def assign_generation_numbers(self):
        id_list = [self.family_tree[pi].id for pi in xrange(0,len(self.family_tree))]
        father_id_list = []
        mother_id_list = []
        for pi in xrange(0,len(self.family_tree)):
            if (hasattr(self.family_tree[pi],'father')):
                father_id_list.append(self.family_tree[pi].father.id)
            else:
                father_id_list.append('none')
            if (hasattr(self.family_tree[pi],'mother')):
                mother_id_list.append(self.family_tree[pi].mother.id)
            else:
                mother_id_list.append('none')
        #convert to numpy arrays for using 'where' function
        father_id_list = np.array(father_id_list)
        mother_id_list = np.array(mother_id_list)
        id_list = np.array(id_list)
        
        badval = 1.0e10
        generation_number_list = np.zeros(len(id_list))+badval
        relations_already_assigned = [False for i in xrange(0,len(id_list))]
        previous_person_index = -1
        person_index = 0
        generation_number_list[0] = 0
        #as long as we still have relations to assign...
        while ((len(np.bitwise_not(relations_already_assigned)) > 0) and (person_index != previous_person_index)):
            #print "pervious_person_index = ", previous_person_index
            #print "person index = ", person_index
            children = np.where((father_id_list == id_list[person_index]) | (mother_id_list == id_list[person_index]))[0]
            if (len(children) > 0):
                generation_number_list[children] = generation_number_list[person_index]-1
            if (father_id_list[person_index] != 'none'):
                father_index = np.where(id_list == father_id_list[person_index])[0]
                generation_number_list[father_index] = generation_number_list[person_index]+1
            if (mother_id_list[person_index] != 'none'):
                mother_index = np.where(id_list == mother_id_list[person_index])[0]
                generation_number_list[mother_index] = generation_number_list[person_index]+1
            relations_already_assigned[person_index] = True
            possible_next_people = np.where((np.bitwise_not(relations_already_assigned)) & (generation_number_list != 1.0e10))[0]
            previous_person_index = person_index
            if (len(possible_next_people) > 0):
                person_index = possible_next_people[0]
        #Deal with people that have no connections
        bad = np.where(generation_number_list == badval)[0]
        good = np.where(generation_number_list != badval)[0]
        #make all positive
        generation_number_list -= np.min(generation_number_list[good])
        if (len(bad) > 0):
            generation_number_list[bad] = -1
        #Store generation number
        for pi in xrange(0,len(self.family_tree)):        
            self.family_tree[pi].generation_number = generation_number_list[pi]

    def get_simple_tree_dict(self):
        dict_list = []
        for pi in xrange(0,len(self.family_tree)):
            dict_list.append(self.family_tree[pi].get_dict())
        return dict_list

    def get_tree_dict(self):
        dict = []

data_file = '../data/family_data.txt'

tree = family_tree()
tree.read_tree(data_file)

tree.assign_generation_numbers()



tree_dict = tree.get_simple_tree_dict()

json_out_name = 'my_json.json'
with open('./json_data/' + json_out_name, 'w') as outfile:
    json.dump(tree_dict, outfile, indent = 2)

pdb.set_trace()

print_tree(family_tree)
draw_tree_python(family_tree)


pdb.set_trace()

