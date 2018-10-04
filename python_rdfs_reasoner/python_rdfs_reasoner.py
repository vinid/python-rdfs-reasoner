# -*- coding: utf-8 -*-

"""Main module."""
import json
import io
from entailment_rules import *
import os
from util import *
from multiprocessing import Pool
import argparse
import time
import logging

logging.basicConfig(level=logging.INFO)
logging.debug('This will get logged')

class Entailment:
    def __init__(self, kg_file_name):
        self.kg_file_name = kg_file_name

        if not os.path.exists("chains/"):
            os.makedirs("chains/")

        self.debug_graph_file = open("chains/" + self.kg_file_name.split("/")[-1] + "_load_chainer", "w")

        with open(self.kg_file_name) as f:
            self.json_data = json.load(f)

        # axiomatic triples
        with io.open("rdfs_axioms") as added:
            self.lines = added.readlines()
            self.lines = [k.strip().split() for k in self.lines]

        self.inferenced_triples = []

        self.triples = self.json_data["OriginalAxioms"]
        self.triples = [k.split() for k in self.triples]

        self.jena_inferenced = self.json_data["InferredAxioms"]
        self.jena_inferenced = [k.split() for k in self.jena_inferenced]

        self.path  = "inferenced/" + self.kg_file_name.split("/")[-1] + "/"
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # Creating the graph of the triples inferred by Jena

        with open(self.path + "K_Jena_Inferrence", "w") as kg_inf_write:
            for k in self.jena_inferenced:
                kg_inf_write.write(k[0] + " " + k[1] + " " + k[2] + " ." + "\n")

        # Creating the first graph with the triples
        with open(self.path + "K_0.json", "w") as kg_inf_write:
            #for k in self.triples:
            #    kg_inf_write.write(k[0] + " " + k[1] + " " + k[2] + " ." + "\n")
            self.json_data["InferredAxioms"] = [" ".join(k) for k in self.triples]
            json.dump(self.json_data,kg_inf_write)

        # Creating the second graph with the axiomatic triples
        with open(self.path + "K_1.json", "w") as kg_inf_write:
            #for k in self.lines:
            #    kg_inf_write.write(k[0] + " " + k[1] + " " + k[2] + " ." + "\n")
            self.json_data["InferredAxioms"] = [" ".join(k) for k in self.triples]
            json.dump(self.json_data,kg_inf_write)

        logging.info('Adding RDFS AXIOMS')
        self.triples = self.triples + self.lines

    def generate_inferences(self):
        chain_inference_number = 2
        logging.info('Generating Chain of Inference number ' + str(chain_inference_number))
        entailed = self.run_entailment()
        logging.info('Ended Generation of Chain of Inference number'  + str(chain_inference_number))

        while entailed != []:
            self.json_data["InferredAxioms"] = []
            with open(self.path + "K_" + str(chain_inference_number) + ".json", "w") as kg_inf_write:
                chain_inference_number = chain_inference_number+1
                    #kg_inf_write.write(k[0] + " " + k[1] + " " + k[2] + " ." + "\n")
                self.json_data["InferredAxioms"] += [" ".join(k) for k in entailed]
                json.dump(self.json_data,kg_inf_write)

            self.triples += entailed
            self.inferenced_triples += entailed

            logging.info('Generating Chain of Inference number ' + str(chain_inference_number))
            entailed = self.run_entailment()
            logging.info('Ended Generation of Chain of Inference number' + str(chain_inference_number))

        with open(self.path + "K_AggregatedInference",  "w") as kg_inf_write:
            for k in self.inferenced_triples:
                kg_inf_write.write(k[0] + " " + k[1] + " " + k[2] + " ." + "\n")

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

        a = rdfs1.get()
        b = rdfs2.get()
        c = rdfs3.get()
        d = rdfs4a.get()
        e = rdfs4b.get()
        f = rdfs5.get()
        g = rdfs6.get()
        h = rdfs7.get()
        i = rdfs8.get()
        l = rdfs9.get()
        m = rdfs10.get()
        n = rdfs11.get()
        o = rdfs12.get()
        p = rdfs13.get()

        infrenced_axioms += a[0] #match_rdfs1(self.triples,)
        infrenced_axioms += b[0] #match_rdfs2(self.triples,)# rdfs1.get()
        infrenced_axioms += c[0] #match_rdfs3(self.triples,)
        infrenced_axioms += d[0] #match_rdfs4b(self.triples,)
        infrenced_axioms += e[0] #match_rdfs4a(self.triples,)
        infrenced_axioms += f[0] #match_rdfs5(self.triples,)
        infrenced_axioms += g[0] #match_rdfs6(self.triples,)
        infrenced_axioms += h[0] #match_rdfs7(self.triples,)
        infrenced_axioms += i[0] #match_rdfs8(self.triples,)
        infrenced_axioms += l[0] #match_rdfs9(self.triples,)
        infrenced_axioms += m[0] #match_rdfs10(self.triples,)
        infrenced_axioms += n[0] #match_rdfs11(self.triples,)
        infrenced_axioms += o[0] #match_rdfs12(self.triples,)
        infrenced_axioms += p[0] #match_rdfs13(self.triples,)

        graph_inferences = [a[1],b[1],c[1],d[1],e[1],f[1],g[1],h[1],i[1],l[1],m[1],n[1],o[1],p[1]]

        for k in graph_inferences:
            for i in k:
                self.debug_graph_file.write(i)

        # remove duplicate axioms
        new_k = []
        for elem in infrenced_axioms:
            if elem not in new_k:
                new_k.append(elem)

        # remove duplicate axioms
        new_k = []
        for elem in infrenced_axioms:
            if elem in self.jena_inferenced:
                new_k.append(elem)

        return new_k


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_name',
                        help="Jena KG output")

    args = parser.parse_args()

    start_time = time.time()
    ent = Entailment(args.file_name)
    ent.generate_inferences()

    elapsed_time = time.time() - start_time
    logging.info('Elapsed Time = ' + str(elapsed_time))
    logging.info("Set of Jena Inferences - Set of Reasoner Inferences " +
                 str(len(diff(ent.jena_inferenced, ent.inferenced_triples))))
    logging.info("Set of Reasoner Inferences - Set of Jena Inferences " +
                 str(len(diff(ent.inferenced_triples, ent.jena_inferenced))))

    logging.info("Missing Triples from Reasoner")
    logging.info((([" ".join(k) for k in (diff(ent.jena_inferenced, ent.inferenced_triples + ent.lines))] )))




if __name__ == '__main__':
    main()
