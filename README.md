# Python  RDFS Reasoner

Given a KG generates step by step inferences and report the inferences of each chain in a different file. It is possible to explore a given inference and to retrieve the chain of axioms that generated that inference. Inference is done with the use of the [RDFS entailment axioms](https://www.w3.org/TR/rdf11-mt/#rdfs-entailment)

The tool filters out those inferences that are not made by Jena.

## Inference

To generate the inferences from the axiom you can use the following command.
```python
python2.7 python_rdfs_reasoner.py -f knowledge_graphs/DAO_2.json
```

## Chain Retrieval

To print the chain of relation inferences that generated a given axiom you can use the following command.

```python
python2.7 chain_inferences.py -f debug/debug_saved_graph_inferences -i ":Drug rdfs:subClassOf rdfs:Resource"```