import argparse
import textwrap
import os.path
from pyads import ADS

def get_args():
    parser = argparse.ArgumentParser(
        description="Prints the contents of a file stream.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
        py read-stream.py -f my_secret.txt -n test
        py read-stream.py -f C:\data\ADS\my_secret.txt -n 'test,test2'
        ''')
    )

    parser.add_argument("-f", "--file", dest="filename", required=True,
                    help="input file path", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-n','--name', action='store', type=str, required=False, help="data stream name to read")

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
    stream_names = parse_file_names(args['name'])
    
    for stream in stream_names:
        stream_data = read_stream(args['filename'], stream)
        if stream_data != None:
            print(stream_data)
        elif stream == '$DATA':
            f = open(args['filename'])
            lines = f.read()

            print(lines)

def read_stream(file, stream_name):
    """Open file path with ADS and read the stream content

    parameters:
    -----------
    file : str
        file path
    
    stream_name : str
        name of data stream to read

    returns:
    --------
    data : byte str
        byte string of the stream content
    """
    
    handler = ADS(file)
    data = handler.get_stream_content(stream_name)

    return data

def parse_file_names(stream_names):
    """parse the commandline ips supplied

    parameters:
    -----------
    stream_names : str
        one or more stream names in csv format

    returns:
    --------
    list_streams : list
        contains streams to read from
    """

    list_streams = []

    parts = stream_names.split(',')
    for part in parts:
        name = part.strip()
        list_streams.append(name)
    
    return list_streams

if __name__ == "__main__":
    main()