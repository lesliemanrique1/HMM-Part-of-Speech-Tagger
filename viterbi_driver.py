import viterbi
#uses viterbi algortihm

training = "WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_02-21.pos"
#tf = open(training,'r') 
#returns a list of sentence arrays containing tuples ('WORD','Part Of Speech')
corpus_list = viterbi.corpus_list(training)

#print("THE NUMBER OF SENTENCES",len(corpus_list)) 
corpus_dictionary = viterbi.corpus_dictionary(training) 

keys = viterbi.key_list(corpus_dictionary) #pos_keys 
print(keys) 

prior_probabilities_table = viterbi.transition_table(corpus_dictionary,corpus_list) 

#print(transition_table) 
#likelihood table 
#print(keys)
word_dic = viterbi.word_dic(corpus_list,keys) 
words = viterbi.key_list(word_dic) #word keys 

#print(words)
likelihood_table  = viterbi.word_freq(corpus_dictionary,word_dic) 
#print(prior_probabilities_table)
#print(likelihood_table)
#print(word_dic)

test_file = "WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_24.words"
sentences = viterbi.corpus_list_2(test_file) 
#print(sentences) 


print(sentences[0])
s1_trans = viterbi.sentence_tag(sentences[0],keys,words,likelihood_table)  
print(s1_trans)
s1_pos = viterbi.sentence_pos(s1_trans) 
print("\n\n") 
print("sentence pos : ", s1_pos)

#Transition Probabilities of Sentence 

transition_probabilities = viterbi.transition_probabilities(s1_trans,s1_pos,prior_probabilities_table,keys) 

#print(transition_probabilities) 


#Observed Likelihoods table 
observed_like = viterbi.observed_likelihoods(sentences[0],s1_pos,s1_trans,likelihood_table,words,keys)

#THE LAST PART IS TO IMPLEMENT VITERBI ALGORITHMS

#def vit(observed_likelihoods, l_rows,l_columns,transitions,t_rows,t_columns,lookup,decisions): 

table = viterbi.viterbi(observed_like,sentences[0],s1_pos,s1_trans,likelihood_table,words,keys,transition_probabilities)
