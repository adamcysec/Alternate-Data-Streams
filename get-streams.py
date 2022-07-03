import argparse
import textwrap
import os.path
from pyads import ADS

def get_args():
    parser = argparse.ArgumentParser(
        description="prints all data stream names from a file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
        py get-streams.py -f my_secret.txt
        py get-streams.py -f C:\data\ADS\my_secret.txt
        ''')
    )

    parser.add_argument("-f", "--file", dest="filename", required=True,
                    help="input file path", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))

    args = parser.parse_args()

    args_dict = vars(args)

    return args_dict

def is_valid_file(parser, arg):
    """Determines if the supplied file path exists

    parameters:
    -----------
    parser : ArgumentParser
        throws error if file path does not exist
    
    returns:
    --------
    arg : str
        file path
    """

    if not os.path.isfile(arg):
        if not os.path.isdir(arg):
            parser.error("The file %s does not exist!" % arg)
    else:
        return arg 

def main():
    args = get_args()
    stream_names = read_ADS(args['filename'])
    for stream in stream_names:
        print(stream)

def read_ADS(file):
    """Open file path with ADS and read the streams

    parameters:
    -----------
    file : str
        full file path of a file
    
    returns:
    --------
    stream_names : list
        contains one or more alternate data stream names
    """

    handler = ADS(file)
    stream_names = []
    stream_names.append(':$DATA')
    for stream in handler:
        stream_names.append(stream)
    
    return stream_names

if __name__ == "__main__":
    main()