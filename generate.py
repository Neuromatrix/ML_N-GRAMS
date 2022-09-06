
import sys
import Ngram_model


if __name__ == "__main__":
    student = Ngram_model.N_gram(6)
    arguments = sys.argv[1:]
    model = arguments[arguments.index('--model')+1]
    length = int(arguments[arguments.index('--length')+1])
    if '--prefix' in arguments:
        lprefix = arguments[arguments.index('--prefix')+1:arguments.index('--prefix')+7]
        prefix = ""
        for it in lprefix:
            prefix+=str(it)+" "
        prefix = prefix[:-1]
    else :
        prefix = 0
    print(student.generate_sequence(model,prefix,length))
