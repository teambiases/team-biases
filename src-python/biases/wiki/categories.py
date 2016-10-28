
class SubCategorySearchNode(str):
    """
    Simply wrapper classes for subcategories that also keeps track of the depth
    of the subcategory below the root.
    """
    
    def __new__(cls, category, depth):
        node = str.__new__(cls, category)
        node.depth = depth
        return node

def get_subcategories(categories, root_category, depth = -1):
    """
    Given a dictionary of category-subcategory relationships as created by
    extract_categories.py and a root category, does a graph search to find all
    subcategories of that root. If depth is >= 0, stops at the given depth.
    Depth 0 returns only the root category. Returns subcategories as a set of
    category names.
    """
    
    subcategory_frontier = {SubCategorySearchNode(root_category, 0)}
    subcategories = set()
    while len(subcategory_frontier) > 0:
        subcategory = next(iter(subcategory_frontier))
        if depth < 0 or subcategory.depth <= depth:
            subcategory_frontier.remove(subcategory)
            subcategories.add(subcategory)
            
            immediate_subcategories = {SubCategorySearchNode(category,
                                       subcategory.depth + 1)
                                       for category in categories[subcategory]}
            subcategory_frontier |= (immediate_subcategories - subcategories)
        
    return subcategories
