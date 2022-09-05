
import sys
import Ngram_model


if __name__ == "__main__":
    student = Ngram_model.N_gram(6)
    arguments = sys.argv[1:]
    model = arguments.index('--model')+1
    if '--input-dir' in arguments:
        test_path = arguments.index('--input-dir')+1
    else :
        test_path = "stdin"
    if test_path == "stdin":
        text = ""
        for line in sys.stdin:
            text += input()
    else :
        with open(test_path, 'r') as f:
            text = f.read()
    student.upfit(text,model)
