import viterbi

training = "WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_02-21.pos"


#returns a list of sentence list containing tuples (word,part of speech) 

corpus_list = viterbi.corpus_list(training) 


#creates a dictionary of corpus part of speech tag : occurences 
corpus_dictionary = viterbi.corpus_dictionary(training) 

#pos_keys 
keys = viterbi.key_list(corpus_dictionary) 

#creates the prior_probabilities transitions table for the entire corpus 


prior_probabilities_table = viterbi.transition_table(corpus_dictionary,corpus_list)


#creates a word dictionary 
#word: list of part of speeches and increment occurences of word as part of speech 
word_dic = viterbi.word_dic(corpus_list,keys) 


#word_keys
words = viterbi.key_list(word_dic)


#likelihood_table 
likelihood_table  = viterbi.word_freq(corpus_dictionary,word_dic)


#Emissions and Transitions 
test_file = "WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_24.words"
sentences = viterbi.corpus_list_2(test_file) 

error_list = [] 
error_list_i = [] 
new_sentences = [] 
count = 0 
for sentence in sentences:
	trans = viterbi.sentence_tag(sentence,keys,words,likelihood_table)
	s_pos = viterbi.sentence_pos(trans)
	transition_table = viterbi.transition_probabilities(trans,s_pos,prior_probabilities_table,keys)

	observed_like = viterbi.observed_likelihoods(sentence,s_pos,trans,likelihood_table,words,keys)
	vit_sent = viterbi.viterbi(observed_like,sentence,s_pos,transition_table) 
	errors = 0 
	for p in vit_sent:
		if p[1] == 'S':
			errors=errors+1 
	
	new_sentences.append(vit_sent) 
	if(errors>0):
		error_list.append(vit_sent) 
		error_list_i.append(count)
	count=count+1

print(error_list)
print(error_list_i)
