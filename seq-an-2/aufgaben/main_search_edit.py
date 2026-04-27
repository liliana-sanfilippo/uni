from argparse import ArgumentParser
from fasta import read_mfasta
from d_edit import d_edit
from d_maximal_matches import d_maximal_matches
from d_q_gram import d_q_gram
import sys


def filter_q_gram(a: str, b : str, max_edit_distance: int, q: int = 7) -> bool:
    #TODO: Implement a filter based on d_q_gram
    raise NotImplementedError

def filter_maximal_matches(a : str,b : str, max_edit_distance : int) -> bool:
    #TODO: Implement a filter based on d_maximal_matches
    raise NotImplementedError

if __name__=="__main__":
    parser = ArgumentParser(description="Find all entries of a fasta file with an edit distance below a threshold")
    parser.add_argument("query",help="Query fasta file. (Contains a single sequence)")
    parser.add_argument("reference",help="Reference multiple fasta file.")
    parser.add_argument("--filter",choices=["none","q-gram","maxmatch","both"],default="none")
    parser.add_argument("--max-distance",type=int,default=3, help="Edit distance threshold.")
    args = parser.parse_args()
    # TODO: 
    # - Read both fasta files
    #
    # - Based on the user argument "--filter" use filter_q_gram and/or 
    #   filter_maximal_matches to decide early whether you need to compute
    #   the full edit distance
    #
    # - Calculate edit distances between query and each reference sequence
    #
    # - If the distance is below the "--max-distance" threshold, 
    #   output the if from the fasta header and the score to stdout
    #
    # - Tip: Start with the case without any filters
    # - *Optional*: Output the time needed to complete the query
