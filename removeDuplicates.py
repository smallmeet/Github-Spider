"""
Script to remove duplicate lines from a file. 
Produces a new txt document with duplicate lines removed
"""
infilename = raw_input("Enter input file with .txt: ")
outfilename = raw_input("Enter output file with .txt: ")

lines_seen = set() # holds lines already seen
outfile = open(outfilename, "w")
for line in open(infilename, "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
