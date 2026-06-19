from argparse import ArgumentParser
from sellers import sellers,sellers_cutoff,filter_to_local_minima
from fasta import read_mfasta
import time
import matplotlib.pyplot as plt


if __name__=="__main__":
    parser = ArgumentParser(description="Find all entries of a fasta file with an edit distance below a threshold")
    parser.add_argument("query",help="Query multiple fasta file. (Contains multiple sequences to search in the text)")
    parser.add_argument("reference",help="Reference multiple fasta file.")
    parser.add_argument("--max-distance",type=int,default=3, help="Cost threshold.")
    parser.add_argument("--use-ukkonen",action="store_true")
    parser.add_argument("--both", action="store_true")
    args = parser.parse_args()
    #Read both fasta files and find positions matching
    # the queries with edit distance at most --max-distance
    # using the sellers algorithm
    #Use the cutoff-variant if --use-ukkonen is set

    query = read_mfasta(args.query)
    reference = read_mfasta(args.reference)[0].sequence
    max_distance = args.max_distance
    cutoff = args.use_ukkonen

    runtime_sellers = []
    runtime_ukkonen = []

    for seq in query:
        start = time.time()
        if cutoff:
            print(f"Query: {seq.id}",filter_to_local_minima(sellers_cutoff(reference,seq.sequence,max_distance)))
            end = time.time()
            runtime_ukkonen.append(end-start)
            print("Laufzeit: ", end - start)
        if args.both:
            print(f"Query: {seq.id}", filter_to_local_minima(sellers_cutoff(reference, seq.sequence, max_distance)))
            end = time.time()
            runtime_ukkonen.append(end - start)
            print("Laufzeit: ", end - start)

            start = time.time()
            print(f"Query: {seq.id}", filter_to_local_minima(sellers(reference, seq.sequence, max_distance)))
            end = time.time()
            runtime_sellers.append(end - start)
            print("Laufzeit: ", end - start)
        else:
            print(f"Query: {seq.id}",filter_to_local_minima(sellers(reference,seq.sequence,max_distance)))
            end = time.time()
            runtime_sellers.append(end-start)
            print("Laufzeit: ", end - start)

    plt.boxplot([runtime_sellers, runtime_ukkonen],
                tick_labels=["sellers","cutoff"])
    plt.ylabel("Laufzeit (s)")
    plt.title("Laufzeitvergleich")
    plt.show()