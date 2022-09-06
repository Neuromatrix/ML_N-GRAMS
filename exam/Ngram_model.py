import queue
import re
import os
import random
import pickle
#-----------------------

class N_gram:
    #attributes
    n = 2
    vocab = []
    text = []
    corpus = ""
    n_grams = []
    n_plus_grams =[]
    count_Ngrams = {}
    count_Nplusgrams = {}


    def __init__(self, len_n_gram = 2) -> None:
        self.n = len_n_gram


    def _tokenize(self,ccorpus: str) -> None:
        self.corpus = ccorpus.lower()
        self.corpus = self.corpus.replace('\n','')
        filter(None,self.corpus)
        self.corpus = re.sub(r'[^a-zA-Z0-9\s]', ' ', self.corpus)
        self.text = [token for token in self.corpus.split(" ") if token != ""]

        if len(self.vocab)>0:
            self.vocab = self.vocab[0]
        for word in list(set(self.text)):
            self.vocab.append(word)

        self.vocab = list(set(self.vocab))
        ngrams = zip(*[self.text[i:] for i in range(self.n)])
        ngramsplus = zip(*[self.text[i:] for i in range(self.n+1)])
        self.n_grams +=  [" ".join(ngram) for ngram in ngrams]
        self.n_plus_grams +=  [" ".join(ngram) for ngram in ngramsplus]

    def probability(self,prefix: str,next_word: str) -> int:
        if (prefix + ' ' + next_word) in self.count_Nplusgrams:
            a = self.count_Nplusgrams[prefix + ' ' + next_word]
        else:
            a = 0
        b = self.count_Ngrams[prefix]
        return a/b

    def upfit(self,text: str,model: str) -> None: #function unlike fit upd model
        self.load(model)
        self._tokenize(text)
        for ngram in self.n_grams:
            if ngram in self.count_Ngrams:
                self.count_Ngrams[ngram] += 1
            else:
                self.count_Ngrams[ngram] = 1
        for ngram in self.n_plus_grams:
            if ngram in self.count_Nplusgrams :
                self.count_Nplusgrams [ngram] += 1
            else:
                self.count_Nplusgrams [ngram] = 1
        self.upload(model)

    def fit(self,text: str,model: str) -> None: #learn without update, we get old model and add new data and at once generate sequence
        self.load(model)
        self._tokenize(text)

        for ngram in self.n_grams:
            if ngram in self.count_Ngrams:
                self.count_Ngrams[ngram] += 1
            else:
                self.count_Ngrams[ngram] = 1
        for ngram in self.n_plus_grams:
            if ngram in self.count_Nplusgrams :
                self.count_Nplusgrams [ngram] += 1
            else:
                self.count_Nplusgrams [ngram] = 1
    def choose_next_word(self,prefix) -> str:
        possible_words = []
        wweights = []
        for word in self.vocab:

            possible_words.append(word)
            wweights.append(self.probability(prefix,word))
        return random.choices(possible_words,weights=wweights,k = 1)

    def generate_sequence(self,model = 0,prefix = 0,length = 30)  -> str:
        self.load(model)
        if len(self.vocab) > 0:
            self.vocab = self.vocab[0]
        if prefix == 0:
            prefix = random.choice(self.n_grams)
        prefix_queue = list(prefix.split(" "))
        result_seq = []
        for i in prefix_queue:
            tmp = []
            tmp.append(i)
            result_seq.append(tmp)
        prefix_queue = prefix_queue[-self.n:]
        for _ in range(length):
            tmp_q = ""
            for i in prefix_queue:
                tmp_q += i
                tmp_q += ' '
            tmp_q =tmp_q[:-1]
            next_w = self.choose_next_word(tmp_q)
            result_seq.append(next_w)
            prefix_queue += next_w
            prefix_queue = prefix_queue[1:]

        res = ""
        for i in result_seq:
            res += i[0]
            res += ' '
        return res

    def load(self,model) -> None:
        with open(model, 'rb') as f:
            if (os.stat(model).st_size!=0):
                self.vocab = pickle.load(f),
                self.n_grams = pickle.load(f)
                self.n_plus_grams = pickle.load(f)
                self.count_Ngrams = pickle.load(f)
                self.count_Nplusgrams = pickle.load(f)

    def upload(self,model) -> None:
        with open(model, 'wb') as f:
            pickle.dump(self.vocab, f)
            pickle.dump(self.n_grams, f)
            pickle.dump(self.n_plus_grams, f)
            pickle.dump(self.count_Ngrams , f)
            pickle.dump(self.count_Nplusgrams, f)

if __name__ == "__main__":
    #! please dont touch dump_model.pkl, there are 6grams from 1984, brave new world and animal farm(
    os.chdir(r"C:\Users\grivi\vscodes\ML\exam")
    with open("text.txt", 'r') as f:
        text = f.read()
    a = N_gram(6)
    a.upfit(text,r"C:\Users\grivi\vscodes\ML\exam\model.pkl")
    b = N_gram(6)
    print(b.generate_sequence(r"C:\Users\grivi\vscodes\ML\exam\model.pkl"))
