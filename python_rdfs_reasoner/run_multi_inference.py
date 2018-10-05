import logging
from python_rdfs_reasoner import *
from os import listdir
from os.path import isfile, join
from subprocess import call

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder',
                        help="Folder with knowledge graphs")

    args = parser.parse_args()

    files = [f for f in listdir(args.folder) if isfile(join(args.folder, f))]

    for file in files:
        start_time = time.time()
        logging.info("Reasoning over " + args.folder + file)
        import os
        cwd = os.getcwd()

        os.system("python " + cwd + "/python_rdfs_reasoner.py -f " + cwd + "/" + args.folder + file)

        ent = Entailment(args.folder + file)
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
