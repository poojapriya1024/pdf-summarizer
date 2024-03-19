#this file contains only the NLP part = text summarization

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = "Citizen science, the involvement of the public in scientific research, has experienced a remarkable surge in popularity in recent years. This collaborative approach harnesses the collective power of everyday people to contribute to real-world scientific projects. Once relegated to the fringes of research, citizen science initiatives are now tackling some of the most pressing challenges facing our planet, from monitoring biodiversity loss to tracking climate change patterns."

stopwords = list(STOP_WORDS) #find the filler words to focus on the more important words

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)

#get the stream of tokens
tokens = [token.text for token in doc]
# print(tokens)

#all the punctuations
punctuation_symbols = punctuation + '\\n'

#used to store the frequency of each word
word_frequencies = {}
for word in doc:
    if word.text.lower() not in stopwords:
        if word.text.lower() not in punctuation_symbols:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1


max_frequency = max(word_frequencies.values())
for word in word_frequencies.keys():
    word_frequencies[word] = word_frequencies[word] / max_frequency

#obtain the list of sentences in the doc
sentence_tokens = [sentence for sentence in doc.sents]
#get the score(importance) of each sentence in the doc based on the frequently repeated words
sentence_scores = {} 

for sent in sentence_tokens:
    for word in sent:
        if word.text.lower() in word_frequencies.keys():
            if sent not in sentence_scores.keys():
                sentence_scores[sent] = word_frequencies[word.text.lower()]
            else:
                sentence_scores[sent] += word_frequencies[word.text.lower()]
                

#indicates how short we wish the summary to be
select_length = int(len(sentence_tokens)*0.7) 
#obtain the top most sentences that has high frequency score based on the select_length value
summary = nlargest(select_length,sentence_scores,key = sentence_scores.get)

final_summary = [word.text for word in summary]
#join the contents of final_summary(list) to make a proper paragraph
summary = "".join(final_summary)

print(summary)