import pypatt
saved_inferences = open("saved_inferences", "w")
saved_inferences_list = set()

@pypatt.transform
def match_one(triples, first = None, second = None, third = None):
    results = []
    for value in triples:
        if first == None and second != None and third != None: #FVV
            with match(value):
                with [quote(d1), second, third]:
                    results.append((d1, second, third))
        if first == None and second == None and third != None: #FFV
            with match(value):
                with [quote(d1), quote(d2), third]:
                    results.append((d1, d2, third))
        if first == None and second == None and third == None: #FFF
            with match(value):
                with [quote(d1), quote(d2), quote(d3)]:
                    results.append((d1, d2, d3))
        if first != None and second == None and third != None: #VFV
            with match(value):
                with [first, quote(d2), third]:
                    results.append((first, d2, third))
        if first != None and second == None and third == None: #VFF
            with match(value):
                with [first, quote(d2), quote(d3)]:
                    results.append((first, d2, d3))
        if first == None and second != None and third == None: #FVF
            with match(value):
                with [quote(d1), second, quote(d3)]:
                    results.append((d1, second, d3))
        if first != None and second != None and third != None: #VVV
            with match(value):
                with [first, second, third]:
                    results.append((first, second, third))
        if first != None and second != None and third == None: #VVF
            with match(value):
                with [first, second, quote(d3)]:
                    results.append((first, second, d3))
    return results

def match_rdfs1(triples):
    first_match = match_one(triples)
    all_values = []
    for a,b,c in first_match:

        new_inf_one = [a, "rdf:type", "rdfs:Datatype"]
        new_inf_two = [b, "rdf:type", "rdfs:Datatype"]
        new_inf_three = [c, "rdf:type", "rdfs:Datatype"]

        if not new_inf_one in triples:
            all_values.append(new_inf_one)
        if not new_inf_two in triples:
            all_values.append(new_inf_two)
        if not new_inf_three in triples:
            all_values.append(new_inf_three)
    return all_values

def match_rdfs2(triples):
    inferenced = []
    first_match = match_one(triples, second='rdfs:domain')
    for first_match_triple in first_match:
        second_match = match_one(triples, second=first_match_triple[0])
        for second_match_triple in second_match:

            new_inference = [second_match_triple[0], "rdf:type", first_match_triple[2]]
            if not new_inference in triples and not tuple(new_inference) in saved_inferences_list:
                inferenced.append(new_inference)
                saved_inferences_list.add(tuple(new_inference))
                saved_inferences.write(" ".join(first_match_triple) + " " + " ".join(second_match_triple) + " " + " ".join(new_inference) + "\n")

    return inferenced

def match_rdfs3(triples):
    inferenced = []
    first_match = match_one(triples, second='rdfs:range')
    for first_match_triple in first_match:
        second_match = match_one(triples, second=first_match_triple[0])
        for second_match_triple in second_match:
            new_inference = [second_match_triple[2], "rdf:type", first_match_triple[2]]

            if not new_inference in triples and not tuple(new_inference) in saved_inferences_list:
                inferenced.append(new_inference)
                saved_inferences_list.add(tuple(new_inference))
                saved_inferences.write(
                    " ".join(first_match_triple) + " " + " ".join(second_match_triple) + " " + " ".join(new_inference) + "\n")

    return inferenced

def match_rdfs4a(triples):
    inferenced = []
    first_match = match_one(triples)
    for first_match_triple in first_match:
        new_inference = [first_match_triple[0], "rdf:type", "rdfs:Resource"]

        if not new_inference in triples and not tuple(new_inference) in saved_inferences_list:
            inferenced.append(new_inference)
            saved_inferences_list.add(tuple(new_inference))
            saved_inferences.write(" ".join(first_match_triple) + " " + " ".join(new_inference) + "\n")

    return inferenced

def match_rdfs4b(triples):
    inferenced = []
    first_match = match_one(triples)
    for first_match_triple in first_match:
        new_inference = [first_match_triple[2], "rdf:type", "rdfs:Resource"]

        if not new_inference in triples:
            inferenced.append(new_inference)
            saved_inferences_list.add(tuple(new_inference))
            saved_inferences.write(" ".join(first_match_triple) + " "  + " ".join(new_inference) + "\n")

    return inferenced

def match_rdfs5(triples):
    inferenced = []
    first_match = match_one(triples, second='rdfs:subPropertyOf')
    for first_match_triple in first_match:
        second_match = match_one(triples, first=first_match_triple[2], second="rdfs:subPropertyOf")
        for second_match_triple in second_match:
            new_inference = [first_match_triple[0], "rdfs:subPropertyOf", second_match_triple[2]]

            if not new_inference in triples and not tuple(new_inference) in saved_inferences_list:
                inferenced.append(new_inference)
                saved_inferences_list.add(tuple(new_inference))
                saved_inferences.write(
                    " ".join(first_match_triple) + " " + " ".join(second_match_triple) + " " + " ".join(new_inference) + "\n")

    return inferenced

def match_rdfs6(triples):
    inferenced = []
    first_match = match_one(triples, second="rdf:type", third="rdf:Property")
    for first_match_triple in first_match:
        new_inference = [first_match_triple[0], "rdfs:subPropertyOf", first_match_triple[0]]

        if not new_inference in triples:
            inferenced.append(new_inference)
            saved_inferences_list.add(tuple(new_inference))
            saved_inferences.write(" ".join(first_match_triple) + " " + " ".join(new_inference) + "\n")

    return inferenced

def match_rdfs7(triples):
    inferenced = []
    first_match = match_one(triples, second='rdfs:subPropertyOf')
    for first_match_triple in first_match:
        second_match = match_one(triples, second=first_match_triple[0])
        for second_match_triple in second_match:
            new_inference = [second_match_triple[0], first_match_triple[2], second_match_triple[2]]

            if not new_inference in triples and not tuple(new_inference) in saved_inferences_list:
                inferenced.append(new_inference)
                saved_inferences_list.add(tuple((new_inference)))
                saved_inferences.write(
                    " ".join(first_match_triple) + " " + " ".join(second_match_triple) + " " + " ".join(new_inference) + "\n")

    return inferenced

def match_rdfs8(triples):
    inferenced = []
    first_match = match_one(triples, second="rdf:type", third="rdfs:Class")
    for first_match_triple in first_match:
        new_inference = [first_match_triple[0], "rdfs:subClassOf", "rdfs:Resource"]
        if not new_inference in triples and not tuple(new_inference) in saved_inferences_list:
            inferenced.append(new_inference)
            saved_inferences_list.add(tuple((new_inference)))
            saved_inferences.write(" ".join(first_match_triple) + " " + " ".join(new_inference) + "\n")

    return inferenced

def match_rdfs9(triples):
    inferenced = []
    first_match = match_one(triples, second='rdfs:subClassOf')
    for first_match_triple in first_match:
        second_match = match_one(triples, second="rdf:type", third=first_match_triple[0])
        for second_match_triple in second_match:
            new_inference = [second_match_triple[0], "rdf:type", first_match_triple[2]]
            if not new_inference in triples and not tuple(new_inference) in saved_inferences_list:
                inferenced.append(new_inference)
                saved_inferences_list.add(tuple((new_inference)))
                saved_inferences.write(
                    " ".join(first_match_triple) + " " + " ".join(second_match_triple) + " " + " ".join(new_inference) + "\n")

    return inferenced

def match_rdfs10(triples):
    inferenced = []
    first_match = match_one(triples, second="rdf:type", third="rdfs:Class")
    for first_match_triple in first_match:
        new_inference = [first_match_triple[0], "rdfs:subClassOf", first_match_triple[0]]
        if not new_inference in triples and not tuple(new_inference) in saved_inferences_list:
            inferenced.append(new_inference)
            saved_inferences_list.add(tuple((new_inference)))
            saved_inferences.write(" ".join(first_match_triple) + " " + " ".join(new_inference) + "\n")

    return inferenced

def match_rdfs11(triples):
    inferenced = []
    first_match = match_one(triples, second='rdfs:subClassOf')
    for first_match_triple in first_match:
        second_match = match_one(triples, first=first_match_triple[2], second="rdfs:subClassOf")
        for second_match_triple in second_match:
            new_inference = [first_match_triple[0], "rdfs:subClassOf", second_match_triple[2]]
            if not new_inference in triples and not tuple(new_inference) in saved_inferences_list:
                inferenced.append(new_inference)
                saved_inferences_list.add(tuple((new_inference)))
                saved_inferences.write(
                    " ".join(first_match_triple) + " " + " ".join(second_match_triple) + " " + " ".join(new_inference) + "\n")

    return inferenced

def match_rdfs12(triples):
    inferenced = []
    first_match = match_one(triples, second="rdf:type", third="rdfs:ContainerMembershipProperty")
    for first_match_triple in first_match:
        new_inference = [first_match_triple[0], "rdfs:subPropertyOf", "rdfs:member"]
        if not new_inference in triples and not tuple(new_inference) in saved_inferences_list:
            inferenced.append(new_inference)
            saved_inferences_list.add(tuple((new_inference)))
            saved_inferences.write(" ".join(first_match_triple) + " "  + " ".join(new_inference) + "\n")

    return inferenced

def match_container(triples):
    matches = match_one(triples, third="rdfs:ContainerMembershipProperty")
    return [k[0] for k in matches]

def match_rdfs13(triples):
    inferenced = []
    first_match = match_one(triples, second="rdf:type", third="rdfs:Datatype")
    for first_match_triple in first_match:
        new_inference = [first_match_triple[0], "rdfs:subClassOf", "rdfs:Literal"]
        if not new_inference in triples and not tuple(new_inference) in saved_inferences_list:
            inferenced.append(new_inference)
            saved_inferences_list.add(tuple((new_inference)))
            saved_inferences.write(" ".join(first_match_triple)  + " "  + " ".join(new_inference) + "\n")

    return inferenced
