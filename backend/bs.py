import csv

# This is the code used to decrease the rows in a csv file to 300. Used for convenience.

with open("dataset/goa.csv", "r") as infile, open("output_300.csv", "w", newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    header = next(reader)  # write header
    writer.writerow(header)

    for i, row in enumerate(reader):
        if i >= 300:
            break
        writer.writerow(row)
