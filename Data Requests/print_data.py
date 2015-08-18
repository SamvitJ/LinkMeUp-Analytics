import sys

from get_class_data import returnClassData

def main(argv):

   class_data = returnClassData(argv[1])

   for entry in class_data:

      print entry

# execute main
if __name__ == "__main__":
    main(sys.argv)
