import numpy 
import csv

#NOTE:
#
#		Find a new way to form corpus list 
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
	if (len(l) == 0):
		array.append(sentence) 
		sentence = [] 
	else:
		tags = (l[0],l[1]) 
		sentence.append(tags)
  
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
	#list_1 is columns
	#list_2 is rows
	period_r = list_2.index('.')
	period_c = list_1.index('.')
	#row = 0 
	#print sentence
	#print(sentence) 
	#print("SENTENCE IS ABOVEEEEE!!!")
	this_sentence = [('','S')] + sentence 
	#print this_sentence
	#for i in sentence:
	for i in range(len(this_sentence)-1):
		current = this_sentence[i][1]
		row = list_2.index(current) 
		following = this_sentence[i+1][1]
		column = list_1.index(following) 
		matrix[row][column]+=1 

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
#@param corpus_list	list of sentences with words as tuples 
#@return table		returns prior probabilities transition table 
def transition_table(dic,corpus_list):
	ls = key_list(dic) 

	list_1 =  ls #columns 
	list_2 = ['S'] + ls #rows
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


#-----------------Viterbi Algorithm------------
#Creates an Array of sentences 
def corpus_list_2(filename): 
	tf = open(filename,'r') 
	#sent_cond = True 
	sentence = [] 
	array = []
	for line in tf:
		l = line.split()
		if(len(l) == 0):
			array.append(sentence) 
			sentence = []
		else:
			tags = (l[0]) 
			sentence.append(tags) 

		
		
	tf.close()

	return array

#return OOV list of possabilities 
def OOV_tag(word,index,pos_keys):
	OOV_pos = [] 

	#if there's a hyphen , return JJ
	if '-' in word:
		if 'JJ' not in OOV_pos: 
			OOV_pos.append('JJ')

	#if word ends with able, return JJ 
	if 'able' in word:
		if 'JJ' not in OOV_pos: 
			OOV_pos.append('JJ') 
		

	#if word is numnerical, return CD 
	if unicode(word).isnumeric():
		if 'CD' not in OOV_pos: 
			OOV_pos.append('CD') 
	#if it starts with an uppercase letter and is not found at the beginning of the sentence AND end with an S return NNPS 
	if word[0].isupper() and index > 0 and word[-1] == 's':
		if 'NNPS' not in OOV_pos: 
			OOV_pos.append("NNPS") 

	#if it starts with an uppercase letter and is not found at the beginning of the sentence
	#return NNP
	if word[0].isupper() and index > 0:
		if 'JJ' not in OOV_pos: 
			OOV_pos.append("NNP") 

	#if it ends with an s then return NNS 
	if word[-1] == 's':
		if 'NNS' not in OOV_pos: 
			OOV_pos.append("NNS")  

	#if it ends with ing, return VBG
	if word[-3:] == 'ing':
		if 'VBG' not in OOV_pos: 
			OOV_pos.append("VBG") 

	#if it ends with ed, return VBD 
	if word[-2:] == 'ed':
		if 'VBD' not in OOV_pos: 
			OOV_pos.append('VBD') 
	
	#if it ends with ly return RB 
	if word[-2:] == 'ly':
		if 'RB' not in OOV_pos: 
			OOV_pos.append('RB')
	#if it ends with er return JJR
	if word[-2:] == 'er':
		if 'JJR' not in OOV_pos: 
			OOV_pos.append('JJR')  
	#if it ends with est return JJS 
	if word[-3:] == 'est':
		if 'JJS' not in OOV_pos: 
			OOV_pos.append('JJS')  
	if len(OOV_pos) == 0: 
		if 'N' not in OOV_pos: 
			OOV_pos.append('NN')
	return OOV_pos 

#finds parts of speeches for all words in sentence using corpus and OOV_tag function 
def sentence_tag(sentence,pos_keys, word_keys, likelihood_table):  
	#first find the parts of speeches 
	dic = {} 
	i = 0 
	print(sentence)
	for word in sentence:
	 
		#find row index in likelihood table
		pos_list =[] 
		try:
			word_index = word_keys.index(word.lower()) 
		except ValueError:
			word_index = -1

		if word_index > -1: 
			for j in range(len(likelihood_table[word_index])):
				if likelihood_table[word_index][j] > 0:
					pos_list.append(pos_keys[j]) 
		else:
			pos_list = OOV_tag(word,i,pos_keys) 
		dic[i] = pos_list 

		i+=1 

	return dic

#gets all the unique part of speech tags from the sentece x part of speech dictionary 

def sentence_pos(dic):
	pos_list = [] 
	for key in dic: 
		for val in dic[key]:
			if val not in pos_list:
				pos_list.append(val)
	return pos_list
#def sentence_tag_transition(sentence,pos_keys,pp_table)


def transition_probabilities(dic,pos_list,transition_table,pos_keys):
	rows = ['S'] + pos_list 
	columns = pos_list 
	t_rows = ['S'] + pos_keys
	t_columns = pos_keys 
	#numpy initialize matrix to 0  

	table = numpy.zeros(shape = (len(rows),len(columns)))
	for i in range(len(rows)):
			row_index = t_rows.index(rows[i]) 
			for j in range(len(columns)):
				column_index = t_columns.index(columns[j]) 
				table[i,j] = transition_table[row_index,column_index] 
	
	
	print_transition('test_trans.csv',table,columns,rows)
	return table




#
#@param sentence 		the sentence list 
#@param pos_list		list of parts of speeches for this particular sentence	
#					obtained from sentence_pos 
#@param	sentence_dic		list of parts of speeches for each word in sentence
#@param	likelihood		likelihood table from training corpus
#@param l_rows		likelihood table rows
#@param	l_columns	likelihood table columns 
def observed_likelihoods(sentence,pos_list,sentence_dic,likelihood_table,l_rows,l_columns ):
	#Rows = POS_list
	#Columns = Words 
	rows = pos_list 
	columns = sentence
	table = numpy.zeros(shape = (len(rows),len(columns))) 
	for i in range(len(sentence)): 
		#find part of speech for word 
		word = sentence[i]
		#columns.append(word) #add word to columns list
		#find part of speech for word - list 
		word_pos = sentence_dic[i] 
		#print(word_pos) 

		try:
			l_row_i = l_rows.index(word.lower()) #find likelihood table row 
		except ValueError: 
			l_row_i = -1 #when OOV 
		#print("print likelihood row position\t\t", l_row_i) 
		for pos in word_pos: 
			

			#find column position 
			l_column_i = l_columns.index(pos) 

			#find likelihoods from likelihood table 
			if l_row_i != -1:		
				#find likelihood 
				likelihood = likelihood_table[l_row_i][l_column_i] 
			#NOTE
			#100K is used for temporary testing
			#Will Evaluate this to be different for all parts of speech 
			else:
				likelihood = 1/100000 

			#attach to observed likelihoods table

			row = pos_list.index(pos) 
			column = i

			table[row][column] = likelihood


	print_transition('observed_likelihoods.csv',table,columns,rows)
	return table


#def viterbi_helper(prior_row, prior_column,observed,sentence,pos_list,likelihood_table,l_rows,l_columns,transitions):
	#like = observed[
"""
def viterbi_helper(prev_r,prev_col):
	for j in range(prev_col,len(columns)):
		for i in range(prev_r,len(rows)): 
			likelihood = observed[i-1][j-1] 
			transition = transistions[][j-1] 
			viterbi[i][j] = max(viterbi[i][j],viterbi[prev_r,prev_col] * likelihood * trans)
			path[i][j] = """

def viterbi(observed,sentence,pos_list,sentence_dic,likelihood_table,l_rows,l_columns,transitions ):
	rows = ['S'] + pos_list
	columns  = ['S'] + sentence
	viterbi = numpy.zeros(shape = (len(rows),len(columns))) #lookup 
	path = numpy.zeros(shape = (len(rows),len(columns))) #path 
	#initialize viterbi and path matrix 
	#viterbi will include calculations
	#path will include tuples 
	for i in range(len(rows)):
		array = []
		for j in range(len(columns)):
			if i == 0 and j== 0:
				viterbi[i][j] = 1 
			#if i>0 and j>0: 
				
				#viterbi[i][j] = observed[i-1][j-1] 
			
			#to_this = (0,0) 
			#array.append(to_this)
		#path.append(array)

	#fill in with correct values 
	#go through array column by column
	prev_r = 0 
	prev_c = 0 
	
	prev_rows = []
	prev_rows.append(int(0)) 


	print("\n\n prev rows \n\n",prev_rows)
	for j in range(1,len(columns)):
		prev_list = [] 
		print("NGKFBGKFDBGKFDJG \t\t ", j)
		for i in range(1,len(rows)): 
			if j != 0: 
				like = observed[i-1][j-1]  
				print("like: \t\t", like) 
				if like > 0: 
					prev_list.append(i) 
			

					print("PREVIOUS ROWS ", prev_rows) 
					for k in prev_rows:
						print(k) 
						previous_vit = viterbi[k][j-1] 
						print("k : ", k, "j-1",j-1)
						print("previous vit" ,previous_vit)
						#transition = transitions[k-1][j-1] 
						#how do i find the transition? 
						print("HELLO")
						transition = transitions[k][i-1]
						print("transition \t\t", transition) 
						calc = previous_vit * like * transition 
						print("\n\n CALC \n\n" , calc) 
						number = viterbi[i][j] 
						print("NUMBER",number)
						if calc > number:
							print("\t\t\t should change value \n") 
							viterbi[i][j] = calc 
							path[i][j] = k 
		
		prev_rows = prev_list 
	print_transition('viterbi.csv',viterbi,columns,rows)
	print_transition('viterbi_path.csv',path,columns,rows)
	return viterbi

