import csv
import sys
import jellyfish
import itertools
import operator

def main():
    print("Process started")
    if len(sys.argv) != 5:
        print ("Error: Please type in 4 different file names as arguments.")
        sys.exit()

    f1 = open(sys.argv[1],'r') # the ESMS names list that is used to comparing with OFA names
    f2 = open(sys.argv[2],'r') # the OFA name list is used as a standard
    f3 = open(sys.argv[3],'w', newline='') # the names with higher rates
    f4 = open(sys.argv[4],'w', newline='') # the names with lower rates

    c1 = csv.reader(f1)
    c2 = csv.reader(f2)
    c3 = csv.writer(f3)
    c4 = csv.writer(f4)
    
    masterlist = list(c2) # OFA list
    comparelist = list(c1) # ESMS

    for i in range(0, len(masterlist)):
            masterlist[i][0] = str(masterlist[i][0]).lstrip().rstrip().title()
            masterlist[i][1] = str(masterlist[i][1]).lstrip().rstrip().title()
  
    for i in range(1, len(comparelist)):
            comparelist[i][1] = str(comparelist[i][1]).lstrip().rstrip().title()
            comparelist[i][2] = str(comparelist[i][2]).lstrip().rstrip().title()

    result_list = []
    for hosts_row in comparelist:
        masterindex = 0
        compareindex = 0
        for master_row in masterlist: 
            masterindex += 1
            compareindex += 1
            string1 = ""
            string2 = ""
            string1+=hosts_row[0]
            string1+=" "
            string1+=hosts_row[1]
            string2+=master_row[0]
            string2+=" "
            string2+=master_row[1]
            result = jellyfish.jaro_distance(string1, string2)
            if result >= 0.85 and result != 1.0:
                result_list.append(result)
                result_list = result_list + hosts_row
                result_list = result_list + master_row 

                num1 = map(int, str(compareindex).split(','))
                result_list = result_list + list(num1)

                num2 = map(int, str(masterindex).split(','))
                result_list = result_list + list(num2) 

                c3.writerow(result_list)
                del result_list[:]
            elif result < 0.85 and result >0.74:
                result_list.append(result)
                result_list = result_list + hosts_row
                result_list = result_list + master_row

                num1 = map(int, str(compareindex).split(','))
                result_list = result_list + list(num1)

                num2 = map(int, str(masterindex).split(','))
                result_list = result_list + list(num2) 

                c4.writerow(result_list)
                del result_list[:]
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    print ("Comparison process finished, sorting process started.")
    # Read from comparing result and sort them from largest to smallest
    f1 = open(sys.argv[3],'r') # the ESMS names list that is used to comparing with OFA names
    f2 = open(sys.argv[4],'r') # the OFA name list is used as a standard

    c1 = csv.reader(f1)
    c2 = csv.reader(f2)
    sorted_higher = sorted(c1, key=operator.itemgetter(0), reverse = True)
    sorted_lower = sorted(c2, key=operator.itemgetter(0), reverse = True)
    
    f1.close()
    f2.close()


    f3 = open(sys.argv[3],'w', newline='') # the names with higher rates
    f4 = open(sys.argv[4],'w', newline='') # the names with lower rates

    c3 = csv.writer(f3)
    c4 = csv.writer(f4)
    
    c3.writerow(["Comparison result", "Last Name1", "First name1", "Last Name2", "First Name2",str(sys.argv[1]),str(sys.argv[2])])
    c4.writerow(["Comparison result", "Last Name1", "First name1", "Last Name2", "First Name2",str(sys.argv[1]),str(sys.argv[2])])
   

    for eachline in sorted_higher:
        c3.writerow(eachline)
    for eachline in sorted_lower:
        c4.writerow(eachline) 

    f3.close()
    f4.close()
    print("Process finished")

if __name__ == "__main__":
    main()