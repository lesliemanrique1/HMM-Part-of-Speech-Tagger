import viterbi

#uses viterbi algortihm

training = "WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_02-21.pos"
#tf = open(training,'r') 
#returns a list of sentence arrays containing tuples ('WORD','Part Of Speech')
corpus_list = viterbi.corpus_list(training)
#print("THE NUMBER OF SENTENCES",len(corpus_list)) 
corpus_dictionary = viterbi.corpus_dictionary(training) 
keys = viterbi.key_list(corpus_dictionary) 
#print(corpus)
 
#print(corpus_dictionary)

#pos_list = viterbi.corpus_pos_list(corpus_dictionary) 
#print(pos_list) 

transition_table = viterbi.transition_table(corpus_dictionary,corpus_list) 
#print(transition_table) 

#likelihood table 
#print(keys)
word_dic = viterbi.word_dic(corpus_list,keys) 
word_freq = viterbi.word_freq(corpus_dictionary,word_dic) 
#print(word_dic)
print("done")



 
