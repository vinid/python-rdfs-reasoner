# -*- coding: utf-8 -*-

"""Main module."""
import json
import io
from entailment_rules import *
import os
from multiprocessing.dummy import Pool

class Entailment:
    def __init__(self, kg_file_name):
        self.kg_file_name = kg_file_name


        with open(self.kg_file_name) as f:
            self.json_data = json.load(f)

        with io.open("triples_to_be_added") as added:
            lines = added.readlines()
            lines = [k.strip().split() for k in lines]


        self.triples = self.json_data["OriginalAxioms"]
        self.triples = [k.split() for k in self.triples]
        self.inferenced_triples = []
        self.jena_inferenced = self.json_data["InferredAxioms"]
        self.jena_inferenced = [k.split() for k in self.jena_inferenced]

        self.path  = "inferenced/" + self.kg_file_name.split("/")[-1] + "/"

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(self.path + "K_0", "w") as kg_inf_write:
            for k in self.triples:
                kg_inf_write.write(k[0] + " " + k[1] + " " + k[2] + "\n")

        with open(self.path + "K_1", "w") as kg_inf_write:
            for k in lines:
                kg_inf_write.write(k[0] + " " + k[1] + " " + k[2] + "\n")

        self.triples = self.triples + lines

    def generate_inferences(self):
        print("Generating Set 2")
        entailed = self.run_entailment()
        print("Ended Set 2")
        i = 2
        while entailed != []:
            print("Printing Set " + str(i))
            
            with open(self.path + "K_" + str(i), "w") as kg_inf_write:
                i = i+1
                for k in entailed:
                    kg_inf_write.write(k[0] + " " + k[1] + " " + k[2] + "\n")

            self.triples = self.triples + entailed
            self.inferenced_triples += entailed

            print("Generating Set " + str(i))
            entailed = self.run_entailment()
            print("Ended Set "  + str(i))


    def run_entailment(self):

        pool = Pool(processes=10)

        rdfs1 = pool.apply_async(match_rdfs1, args = (self.triples,))
        rdfs2 = pool.apply_async(match_rdfs2, args = (self.triples,))
        rdfs3 = pool.apply_async(match_rdfs3, args = (self.triples,))
        rdfs4a = pool.apply_async(match_rdfs4a, args = (self.triples,))
        rdfs4b = pool.apply_async(match_rdfs4b, args = (self.triples,))
        rdfs5 = pool.apply_async(match_rdfs5, args = (self.triples,))
        rdfs6 = pool.apply_async(match_rdfs6, args = (self.triples,))
        rdfs7 = pool.apply_async(match_rdfs7, args = (self.triples,))
        rdfs8 = pool.apply_async(match_rdfs8, args = (self.triples,))
        rdfs9 = pool.apply_async(match_rdfs9, args = (self.triples,))
        rdfs10 = pool.apply_async(match_rdfs10, args = (self.triples,))
        rdfs11 = pool.apply_async(match_rdfs11, args = (self.triples,))
        rdfs12 = pool.apply_async(match_rdfs12, args = (self.triples,))
        rdfs13 = pool.apply_async(match_rdfs13, args = (self.triples,))

        infrenced_axioms = []

        infrenced_axioms += rdfs1.get()
        infrenced_axioms += rdfs2.get()
        infrenced_axioms += rdfs3.get()
        infrenced_axioms += rdfs4a.get()
        infrenced_axioms += rdfs4b.get()
        infrenced_axioms += rdfs5.get()
        infrenced_axioms += rdfs6.get()
        infrenced_axioms += rdfs7.get()
        infrenced_axioms += rdfs8.get()
        infrenced_axioms += rdfs9.get()
        infrenced_axioms += rdfs10.get()
        infrenced_axioms += rdfs11.get()
        infrenced_axioms += rdfs12.get()
        infrenced_axioms += rdfs13.get()

        #for i in infrenced_axioms:
        #    if i in self.jena_inferenced:
        #        assioms.append(i)

        new_k = []
        for elem in infrenced_axioms:
            if elem not in new_k:
                new_k.append(elem)

        return new_k

ent = Entailment("knowledge_graphs/DAO_2.json")
ent.generate_inferences()

def diff(first, second):
    x = [tuple(y) for y in first]
    z = [tuple(y) for y in second]
    return set(x) - set(z)

print(len(ent.jena_inferenced))
print(len(ent.inferenced_triples))
print("Jena - Tool")
print(len(diff(ent.jena_inferenced, ent.inferenced_triples)))
#print(([" ".join(k) for k in (diff(ent.jena_inferenced, ent.inferenced_triples))]))

print("Tool - Jena")
print(len(diff(ent.inferenced_triples, ent.jena_inferenced)))
#print(([" ".join(k) for k in (diff(ent.inferenced_triples,ent.jena_inferenced))]))

print("Inferences")
#print(ent.inferenced_triples)
#print(([" ".join(k) for k in (ent.inferenced_triples)]))

#print("Jena Inferences")
#print(([" ".join(k) for k in (ent.jena_inferenced)]))
