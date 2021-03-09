import argparse
from extractor import extract_text_as_dict
from writer import write


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",
                        type=str,
                        help="Path to input PDF File")
    parser.add_argument("-o", "--output",
                        type=str,
                        help="Output format; JSON or XML",)
    args = parser.parse_args()

    my_dict = extract_text_as_dict(args.input)
    response = write(my_dict, args.output)
    print(response)