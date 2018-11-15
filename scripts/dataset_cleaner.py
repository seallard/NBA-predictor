import csv

with open('raw_dataset.csv','r') as infile:
    
    outfile = open('clean_dataset.csv','w')
    
    filewriter = csv.writer(outfile)

    for row in infile:
        row = row.split(',')

        # Replace xx-yy score with xx.
        clean_row = [row[0].split('-')[0], row[1].split('-')[0], row[2].split('-')[0]] + row[3:12] 

        # Add value to date column.
        clean_row.append(row[15].strip('\n'))

        # Write clean data to outfile.
        filewriter.writerow(clean_row)