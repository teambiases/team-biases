import itertools

def average_agreement(items):
    """
    Compute average inter-annotater agreement for several annotated items.
    Each element of items is a list of given annotations for each item; for
    examples, it could be ['Y', 'Y', 'Y', 'N'] if three people annotated Yes
    and one person annotated No.
    """
    
    total_pairs = 0
    agreed_pairs = 0
    for annotations in items:
        for annotation1, annotation2 in itertools.combinations(annotations, 2):
            total_pairs += 1
            if annotation1 == annotation2:
                agreed_pairs += 1
    
    return agreed_pairs / total_pairs
