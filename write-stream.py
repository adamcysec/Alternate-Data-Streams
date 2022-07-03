import argparse
import textwrap
import os.path
from xmlrpc.client import boolean
from pyads import ADS

def get_args():
    parser = argparse.ArgumentParser(
        description="Writes data to a file stream.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
        py write-stream.py -f my_secret.txt -n marvel -d "peter parker is spiderman"
        py write-stream.py -f C:\data\ADS\my_secret.txt -n token -d "blah.txt"
        ''')
    )

    parser.add_argument("-f", "--file", dest="filename", required=True,
                    help="input file path", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-n','--name', action='store', type=str, required=True, help="data stream name to read")
    parser.add_argument('-d','--data', action='store', type=str, required=True, help="data to write to stream")
    parser.add_argument('-a', '--append', action='store_true', required=False)

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
    file = args['filename']
    stream_name = args['name']
    stream_data = args['data']
    isAppend = args['append']

    isfile = is_filepath(stream_data)
    if isfile:
        write_file_to_stream(file, stream_name, stream_data, isAppend)
    else:
        write_str_to_stream(file, stream_name, stream_data, isAppend)

def is_filepath(stream_data):
    """Determines if the supplied stream data is a file path

    parameters:
    -----------
    stream_data : str
        user supplied data to write

    returns:
    --------
    isfile : bool
        True if user supplies a file path
    """
    
    isfile = False
    if os.path.isfile(stream_data):
        isfile = True
    
    return isfile

def write_str_to_stream(file, stream_name, stream_data, isAppend):
    """Writes a string to a data stream
    
    parameters:
    -----------
    file : str
        file path to read stream from
    stream_name : str
        data stream to write data to
    stream_data : str
        the data to write
    isAppend : bool
        write data in append mode 
    """

    handler = ADS(file)
    stream_data = str.encode(stream_data) # convert str to byte str
    succesful_write = handler.add_stream_from_string(stream_name, stream_data, isAppend)
    if succesful_write:
        print(f"Succesful write to stream {stream_name}")

def write_file_to_stream(file, stream_name, stream_data, isAppend):
    """Writes a file contents to a data stream

    parameters:
    -----------
    file : str
        file path to read stream from
    stream_name : str
        data stream to write data to
    stream_data : str
        the data to write
    isAppend : bool
        write data in append mode 
    """

    handler = ADS(file)
    succesful_write = handler.add_stream_from_file(stream_name, stream_data, isAppend)
    if succesful_write:
        print(f"Succesful write to stream {stream_name}")




if __name__ == "__main__":
    main()