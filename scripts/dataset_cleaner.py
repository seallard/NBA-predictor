import csv

with open('raw_dataset.csv','r') as infile:
    outfile = open('clean_dataset.csv','w',newline='')
    filewriter = csv.writer(outfile, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['fg','3pt','ft','oreb','dreb','reb','ast','stl','blk','to','pf','pts','home'])

    next(infile)
    for row in infile:
        row = row.split(',')
        clean_row = [row[0].split('-')[0],row[1].split('-')[0],row[2].split('-')[0]] + row[3:12] #Replace xx-yy score with xx.
        clean_row.append(row[14]) #Add home/away status column.
        filewriter.writerow(clean_row)