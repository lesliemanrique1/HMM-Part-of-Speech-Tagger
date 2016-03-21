import numpy 
import csv


#reads from training file 
#returns a an array of sentence arrays made of tuples (Word,POS)
#@param filename 	name of file to read
#@return array 		list of sentence lists of tuples 
def corpus_list(filename):
    
    tf = open(filename , 'r')

    sent_cond = True 
    sentence = []
    array = []
    count = 0
    for line in tf:
        l = line.split()
        if(len(l) != 2):
            continue
        else:
            
            if sent_cond == False:
                array.append(sentence)
                sentence = []
                sent_cond = True
            
            tags = (l[0],l[1]) 
            if l[0] == '.': 
                sent_cond = False
        
        sentence.append(tags)
        count=count+1  

    tf.close()
    
    return array 


"""
def corpus_dictionary(filename):
    training = filename
    tf = open(training, 'r')
    dic = {}
    for line in tf:
        l = line.split()
        #print(line) 
        #POS is made up of letters; check to see if it's a letter
        if(len(l) == 2):
           
                #add line to list
                #POS.append(l[1])
                #Tokens.append(l[0])
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
    tf.close()
    
    return dic  
"""

#returns a dictionary of the part of speech tag with number of occurences
#@param filename	file to read from 
#@return dic		dictionary 
def corpus_dictionary(filename): 
	training = filename 
	tf = open(training,'r') 
	dic = {}
	for line in tf:
		l = line.split()
		if(len(l) == 2):
			#check if key is existing 
			if l[1] in dic:
				dic[l[1]]+=1 
			else:
				dic[l[1]] = 1
	return dic 




#returns a list of dictionary key
#@param	dictionary	dictionary
#@return pos_list	list of dictionary keys
def key_list(dic):
	list_  = list(dic.keys()) 
	return list_


#prints matrix and row and column headers to a csv file titles 'prior_probabilities.csv'
#@param matrix          the matrix or 2d list that includes the number of times each 
#                       transition occurs in corpus
#@param list_1		column headers
#@param list_2		row headers
def print_transition(filename,matrix,list_1,list_2):
	f = open(filename,'wb')
	with f as out:
		writer = csv.writer(out) 
		writer.writerow(['']+list_1)
		j = 0
		for i in matrix:
			writer.writerow([list_2[j]] + map(lambda num:num,i))
			j+=1
		
#according to the corpus, counts how many times a transition occurs in a matrix
#@param sentence	list of tuples ('word','part of speech') 
#@param matrix          the matrix or 2d list that includes the number of times each 
#                       transition occurs in corpus
#@param list_1		column header 
#@param list_2		row header 
def helper_transition(sentence,matrix,list_1,list_2):
	row = 0 
	for i in sentence:
		past = list_2[row] 
		current = i[1]
		column = list_1.index(current) 
		matrix[row][column] +=1 
		row = list_2.index(current) 

#calculates the prior probabilities 
#@param corpus_list	list of sentences in corpus with words as tuples 
#@param matrix		the matrix or 2d list that includes the number of times each 
#			transition occurs in corpus
#@param dic		dictionary of corpus pos : number of times pos occurs
#@param list_2 		the list that contains the pos tag which are the row headers 
#@return None		no return value; void 
def calculate_prior_probabilities(corpus_list,matrix,dic,list_2):
	for i in range(len(matrix)):
		if i > 0:
			for j in range(len(matrix[i])):
					key = list_2[i]
					matrix[i,j] = matrix[i,j]/dic[key] 
		else:
			dividend = len(corpus_list)
			for j in range(len(matrix[i])):
				matrix[i,j] = matrix[i,j]/dividend 	

#creates the transition table 
#@param dic		dictionary the includes pos:# of times appeared 
#@param corpus_list	list of sentences with words as tuples 
#@return table		returns prior probabilities transition table 
def transition_table(dic,corpus_list):
	ls = key_list(dic) 

	list_1 =  ls 
	list_2 = ['S'] + ls 
	#creates a matrix with indexes initialized to 0 using numpy 
	table = numpy.zeros(shape = (len(list_2),len(list_1)))
	#add values to table sentence by sentence
	for i in corpus_list:
		#call to helper function 
		helper_transition(i,table,list_1,list_2)

	#calculate prior probabilities 
	calculate_prior_probabilities(corpus_list,table,dic,list_2) 
	#prints prior probabilities table to csv file 
	print_transition('prior_probabilities.csv',table,list_1,list_2)  
	return table




#----------------------likelihood table----------------------------------#

#creates a dictionary of the different words in the corpus 
#@param corpus_list	list of words and part of speeches 
#@param keys		column header 
#@return dic		dictionary 
def word_dic(corpus_list, keys):
	dic = {} 
	#print(keys)
	for i in corpus_list:
		for j in i:
			word = j[0].lower() 
			pos = j[1]
			#create dictionary 
			if word in dic:
				index = keys.index(pos) 
				dic[word][index] += 1  
			else:
				#create dictionary element first
				dic[word] = [0]*len(keys) 
				index = keys.index(pos)
				dic[word][index] +=1 
				
	#print(dic)
	return dic 

 

#calculates word frequencies and outputs table into csv file named likelihood.csv 
#@param pos_dic		dictionary of part of speech and their occurences
#@param word_dic	dictionary of words and their occurences of each port of speech 
#@return table		the likelihood matrix
def word_freq(pos_dic,word_dic):
	#get list of keys in word_dic 
	word_keys = key_list(word_dic) 
	pos_keys = key_list(pos_dic) 
	table = numpy.zeros(shape = (len(word_keys),len(pos_keys)))  
	count = 0 
	for key in word_dic:
		for i in range(len(word_dic[key])):	
			#print(word_dic[key][i]) 
			pos_occurences = pos_dic[pos_keys[i]] 
			#print(pos_occurences) 
			#pos_occurences = pos_dic[i]
			#print(pos_occurences)
			#print(word_dic[key][i]) 
			table[count,i] = float(word_dic[key][i])/float(pos_occurences) 
			
			"""if key == 'misanthrope':
				print("key",key) 
				print("original",float(word_dic[key][i])) 
				print("pos_occurences",float(pos_occurences)) 
				print("division",float(table[count,i])) 
			"""
		count+=1 
	print_transition('likelihood.csv',table,pos_keys,word_keys)

	return table 
