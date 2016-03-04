"""Math-related utilities."""

def cosine_similarity(v, w):
    """Computes the cosine between the sparse vectors v and w, represented
    as dictionaries."""
    
    dp = 0 # dot product of v and w
    v2, w2 = 0, 0 # norm squared of v and w
    for key in set(v.keys()) | set(w.keys()):
        if key in v:
            v2 += v[key] ** 2
        if key in w:
            w2 += w[key] ** 2
        if key in v and key in w:
            dp += v[key] * w[key]
    
    try:        
        return dp / (v2 * w2) ** 0.5
    except ZeroDivisionError:
        # Return zero if one of the magnitudes is zero
        return 0
    
def set_cosine_similarity(v, w):
    """Computes the cosine between sparse vectors v and w, represented as
    sets."""
    
    try:
        return len(v & w) / (len(v) * len(w)) ** 0.5
    except ZeroDivisionError:
        # Return zero if one of the magnitudes is zero
        return 0
    
def spectrum_from_similarities(sim1, sim2, end1 = -1, end2 = 1):
    """Given positive similarity values relative to two ends of a spectrum,
    returns a placement along the spectrum."""
    
    return (sim1 / (sim1 + sim2)) * (end2 - end1) + end1
