import sys

if __name__ == "__main__":
    loadModel = sys.argv[1] == 'true'
    if loadModel:
        print("Loading Model")
    else:
        input_text = sys.argv[2]
        print(input_text + " has been processed")

        repositoryPath = sys.argv[3]
        print("The opened window is: " + repositoryPath)
