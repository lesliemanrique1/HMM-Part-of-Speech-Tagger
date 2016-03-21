#Leslie Manrique
#Homework_4_Bigram 
#Name:  Table
#       Probabilities for each POS tags(assuming bigrams) using
#       training corpus (WSJ_02-21.pos)
#OutputFile: Table.txt


#Part_1
#Table of Probabilities
#Output table in Table.txt



#Takes in dictionary and calculates the probability of each POS tag
#Probability = 
#@return dictionary table
#                   POS | PROBABILITY
#



#Find Likelihood
#Token/
#def EmmissionTable(dic):
    
    
    
def makePOSDict(f,POS,Tokens,dic):
    count = 0
    for line in f:
        # count@15 to 
        if count<50:
            count = count+1 

            #print(line)
            l = line.split()
            #print(line) 
            #POS is made up of letters; check to see if it's a letter
            if(len(l) == 2):
                if l[1].isalpha():
                    #add line to list
                    POS.append(l[1])
                    Tokens.append(l[0])
                    #check if key is exiting 
                    if l[1] in dic:
                        #append the new tag to existing array if it's not already in the array 
                        #dic[l[1]].append(l[0])
                        word = l[0].lower() 
                        if not word in dic[l[1]]:
                            dic[l[1]].append(word) 
                    else:
                        #create a new key and array
                        dic[l[1]] = [l[0].lower()]     
            
        else:
            break
   

    

def main():
    training = "WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_02-21.pos"
    tf = open(training,'r')
    POS_Dict = { } 
    #Part Of Speech Array _ FOR TESTING
    POS = []
    #Array of Tags _ FOR TESTING
    Tokens = []
    
    makePOSDict(tf,POS,Tokens,POS_Dict)
    tf.close()
    
    #print(POS)
    #print(Tags)
    print(POS_Dict) 
   

main() 
    



