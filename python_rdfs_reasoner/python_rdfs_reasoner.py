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
        with open(self.path + "K_0", "w") as kg_inf_write:
            for k in self.triples:
                kg_inf_write.write(k[0] + " " + k[1] + " " + k[2] + " ." + "\n")

        # Creating the second graph with the axiomatic triples
        with open(self.path + "K_1", "w") as kg_inf_write:
            for k in self.lines:
                kg_inf_write.write(k[0] + " " + k[1] + " " + k[2] + " ." + "\n")

        logging.info('Adding RDFS AXIOMS')
        self.triples = self.triples + self.lines

    def generate_inferences(self):
        chain_inference_number = 2
        logging.info('Generating Chain of Inference number ' + str(chain_inference_number))
        entailed = self.run_entailment()
        logging.info('Ended Generation of Chain of Inference number'  + str(chain_inference_number))

        while entailed != []:

            with open(self.path + "K_" + str(chain_inference_number), "w") as kg_inf_write:
                chain_inference_number = chain_inference_number+1
                for k in entailed:
                    kg_inf_write.write(k[0] + " " + k[1] + " " + k[2] + " ." + "\n")

            self.triples += entailed
            self.inferenced_triples += entailed

            logging.info('Generating Chain of Inference number ' + str(chain_inference_number))
            entailed = self.run_entailment()
            logging.info('Ended Generation of Chain of Inference number' + str(chain_inference_number))

        with open(self.path + "K_AggregatedInference",  "w") as kg_inf_write:
            for k in self.inferenced_triples:
                kg_inf_write.write(k[0] + " " + k[1] + " " + k[2] + " ." + "\n")

    def run_entailment(self):

        #pool = Pool(processes=10)

        #rdfs1 = pool.apply_async(match_rdfs1, args = (self.triples,))
        #rdfs2 = pool.apply_async(match_rdfs2, args = (self.triples,))
        #rdfs3 = pool.apply_async(match_rdfs3, args = (self.triples,))
        #rdfs4a = pool.apply_async(match_rdfs4a, args = (self.triples,))
        #rdfs4b = pool.apply_async(match_rdfs4b, args = (self.triples,))
        #rdfs5 = pool.apply_async(match_rdfs5, args = (self.triples,))
        #rdfs6 = pool.apply_async(match_rdfs6, args = (self.triples,))
        #rdfs7 = pool.apply_async(match_rdfs7, args = (self.triples,))
        #rdfs8 = pool.apply_async(match_rdfs8, args = (self.triples,))
        #rdfs9 = pool.apply_async(match_rdfs9, args = (self.triples,))
        #rdfs10 = pool.apply_async(match_rdfs10, args = (self.triples,))
        #rdfs11 = pool.apply_async(match_rdfs11, args = (self.triples,))
        #rdfs12 = pool.apply_async(match_rdfs12, args = (self.triples,))
        #rdfs13 = pool.apply_async(match_rdfs13, args = (self.triples,))

        infrenced_axioms = []

        infrenced_axioms += match_rdfs1(self.triples,)
        infrenced_axioms +=  match_rdfs2(self.triples,)# rdfs1.get()
        infrenced_axioms += match_rdfs3(self.triples,)
        infrenced_axioms += match_rdfs4b(self.triples,)
        infrenced_axioms += match_rdfs4a(self.triples,)
        infrenced_axioms += match_rdfs5(self.triples,)
        infrenced_axioms += match_rdfs6(self.triples,)
        infrenced_axioms += match_rdfs7(self.triples,)
        infrenced_axioms += match_rdfs8(self.triples,)
        infrenced_axioms += match_rdfs9(self.triples,)
        infrenced_axioms += match_rdfs10(self.triples,)
        infrenced_axioms += match_rdfs11(self.triples,)
        infrenced_axioms += match_rdfs12(self.triples,)
        infrenced_axioms += match_rdfs13(self.triples,)

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
