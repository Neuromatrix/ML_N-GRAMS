
import sys
import Ngram_model
import os

if __name__ == "__main__":
    student = Ngram_model.N_gram(6)
    arguments = sys.argv[1:]
    model = arguments[arguments.index('--model')+1]
    if '--input-dir' in arguments:
        test_path = arguments[arguments.index('--input-dir')+1]
    else :
        test_path = "stdin"
    if test_path == "stdin":
        text = ""
        for line in sys.stdin:
            text+=line
        student.upfit(text,model)
    else :
        os.chdir(test_path)
        for filename in os.scandir(test_path):
            if filename.is_file():
                with open(filename, 'r') as f:
                    text = f.read()
                student.upfit(text,model)
