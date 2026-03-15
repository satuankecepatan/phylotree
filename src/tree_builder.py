from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.Align import MultipleSeqAlignment

def get_distance_matrix(alignment: MultipleSeqAlignment, model: str = 'identity'):
    """Calculate the distance matrix for a multiple sequence alignment."""
    calculator = DistanceCalculator(model)
    distance_matrix = calculator.get_distance(alignment)
    return distance_matrix

def build_upgma_tree(distance_matrix):
    """Build an UPGMA tree from a distance matrix."""
    constructor = DistanceTreeConstructor()
    upgma_tree = constructor.upgma(distance_matrix)
    return upgma_tree

def build_nj_tree(distance_matrix):
    """Build an NJ tree from a distance matrix."""
    constructor = DistanceTreeConstructor()
    nj_tree = constructor.nj(distance_matrix)
    return nj_tree

def compare_trees(alignment: MultipleSeqAlignment, model: str = 'identity'):
    """A convenience function to compare UPGMA and NJ trees."""
    matrix = get_distance_matrix(alignment, model)
    return {
        "distance_matrix": matrix,
        "upgma": build_upgma_tree(matrix),
        "neighbor_joining": build_nj_tree(matrix)
    }