from argparse import ArgumentParser
from fasta import read_mfasta
from nussinov import nussinov_matrix

if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument("sequences")
    #TODO: Read the rna sequences and apply the nussinov algorithm to determine the score of each sequence

    parser.add_argument("fasta",help="Fasta file")
    args = parser.parse_args()
    fasta = read_mfasta(args.fasta)

    for seq in fasta:
        print(seq.sequence)
        nussinov_matrix(seq.sequence
                        )

