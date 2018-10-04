import argparse
import networkx as nx
import pandas as pd

def get_chain_of_inference(node, G):
    neig = G.edges(node)
    if len(neig) == 2:
        print(neig[0][1] + " & " + neig[1][1])
        print ("\t=>" + node)
        print("--")
        get_chain_of_inference(neig[0][1], G)
        print("--")
        get_chain_of_inference(neig[1][1], G)
    elif len(neig) == 1:
        print(neig[0][1])
        print ("\t=>" + node)
        print("--")
        get_chain_of_inference(neig[0][1], G)
        print("--")


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_name', default="debug/debug_saved_graph_inferences",
                        help="Debug saved inferences graph file")
    parser.add_argument('-i', '--inference',
                        help="Inferenced axiom to be explored")

    args = parser.parse_args()
    load_triples = pd.read_csv(args.file_name, sep=",", names=["head", "rel", "tail"])

    G = nx.DiGraph()

    for index, row in load_triples.iterrows():
        G.add_edges_from([(row["tail"], row["head"])], label=row["rel"])

    get_chain_of_inference(args.inference, G)

if __name__ == '__main__':
    main()
