import argparse
import textwrap
import os.path
from pyads import ADS
import glob
import os
import csv

def get_args():
    parser = argparse.ArgumentParser(
        description="Outputs stats reports from ADS files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
        py find-fileStreams.py -f C:\data\ADS\
        py find-fileStreams.py -f C:\data\ADS\ -o fz
        py find-fileStreams.py -f C:\data\ADS\ -o e
        py find-fileStreams.py -f C:\data\ADS\ -o ze
        ''')
    )

    parser.add_argument("-d", "--dir", required=True,
                    help="input file directory", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-r', '--recursive', action='store_true', required=False)
    parser.add_argument('-o', '--options', action='store', type=str, default='a', help='f = ADS file report\ne = ADS extension report\nz = zone.identifer report, a = all reports')

    args = parser.parse_args()

    args_dict = vars(args)

    return args_dict

def is_valid_file(parser, arg):
    """Determines if the supplied directory path exists

    parameters:
    -----------
    parser : ArgumentParser
        throws error if directory path does not exist
    
    returns:
    --------
    arg : str
        directory path
    """

    if not os.path.isdir(arg):
        parser.error("The directory %s does not exist!" % arg)
    else:
        return arg

def main():
    args = get_args()
    directory = args['dir']
    doRecursive  = args['recursive']
    options = args['options']

    file_stats, extension_stats, = find_files(directory, doRecursive)
    
    if 'f' in options or 'a' in options:
        # ADS file report
        """this report is used to identify all files with ADS
        """
        out_csv_report(file_stats, ['fileName', 'streams', 'extension', 'totalStreams', 'type'], f'ADS_file_report.csv')
    
    if 'e' in options or 'a' in options:
        # ADS extension report
        """this report is used to idenitfy the top file extension with ADS
        """
        out_csv_report(extension_stats, ['extension', 'total', 'totalFiles'], f'ADS_extension_report.csv')
    
    if 'z' in options or 'a' in options:
        # zone.identifer report
        """this report is used to identify the content of the Zone.Identifer ADS
        """
        zoneId_stats = zoneId_report_stats(file_stats)
        out_csv_report(zoneId_stats, ['fileName', 'stream', 'extension', 'type','ZoneId','HostIpAddress','HostUrl','LastWriterPackageFamilyName','ReferrerUrl'], f'ADS_zone_identifer_report.csv')

def zoneId_report_stats(file_stats):
    """collects the Zone.Identifer information from each file

    this report is used to identify the content of the Zone.Identifer ADS

    Parameters:
    -----------
    file_stats : list
        list of file paths

    Returns:
    --------
    new_file_stats : list
        list of possible Zone.Identifer content
    """
    
    new_file_stats = []

    for item in file_stats:
        handler = ADS(item['fileName'])
        for stream_name in item['streams']:
            if stream_name.lower() == 'Zone.Identifier'.lower():
                stream_data = handler.get_stream_content(stream_name)
                str_stream_data = stream_data.decode('utf-8')
                zoneId_stats = parse_zone_identifier(str_stream_data)

                fields = {
                'fileName':item['fileName'], 
                'stream':stream_name, 
                'extension':item['extension'], 
                'type':item['type'], 
                'ZoneId':zoneId_stats['ZoneId'], 
                'HostIpAddress':zoneId_stats['HostIpAddress'],
                'HostUrl':zoneId_stats['HostUrl'],
                'LastWriterPackageFamilyName':zoneId_stats['LastWriterPackageFamilyName'],
                'ReferrerUrl':zoneId_stats['ReferrerUrl']
                }

                new_file_stats.append(fields)

            else:
                str_stream_data = 'n/a'
            
    return new_file_stats

def parse_zone_identifier(data):
    """get the zone content from a zone.Identifer ADS

    Parameters:
    -----------
    data : str
        zone.Identifer content

    Returns:
    --------
    zone_data : dict
        all possible zoneId fields
    """
    
    parts = data.split('\n')
    zone_data = {}
    zone_data['ZoneId'] = None
    zone_data['HostIpAddress'] = None
    zone_data['HostUrl'] = None
    zone_data['LastWriterPackageFamilyName'] = None
    zone_data['ReferrerUrl'] = None
    for part in parts: 
        text = part.strip()
        if text.lower() == '[ZoneTransfer]'.lower():
            continue
        else:
            if len(text.split('=')) > 1:
                text_parts = text.split('=')
                
                if text_parts[0].lower() == 'ZoneId'.lower():
                    zone_data['ZoneId'] = text_parts[1]
                
                
                elif text_parts[0].lower() == 'HostIpAddress'.lower():
                    zone_data['HostIpAddress'] = text_parts[1]
                
                
                elif text_parts[0].lower() == 'HostUrl'.lower():
                    zone_data['HostUrl'] = text_parts[1]
                
                
                elif text_parts[0].lower() == 'LastWriterPackageFamilyName'.lower():
                    zone_data['LastWriterPackageFamilyName'] = text_parts[1]
                
                
                elif text_parts[0].lower() == 'ReferrerUrl'.lower():
                    zone_data['ReferrerUrl'] = text_parts[1]
                
    return zone_data

def find_files(directory, doRecursive):
    """get all file paths with ADS from the given directory path

    Parameters:
    -----------
    directory : str
        file path
    doRecursive : bool
        recursive file path with glob

    Returns:
    --------
    file_data_stats : list
        list of files and metadata
    extension_stats : list
        list of file extensions and metadata
    """
    
    if doRecursive:
        filenames = glob.iglob(f"{directory}/**/*", recursive=True)
    else:
        filenames = glob.iglob(f"{directory}/*")
    
    file_data_stats = []
    file_extensions_stats = {}
    list_file_extensions = []
    extension_stats = []

    # count total number of files
    noOfFiles = 0
    for base, dirs, files in os.walk(directory):
        for Files in files:
            noOfFiles += 1
    #file_extensions_stats['totalFiles'] = noOfFiles

    # get stream data
    for filename in filenames:
        handler = ADS(filename)
        has_streams = handler.has_streams()

        if has_streams:
            #print(f"file: {filename} - Streams: {len(handler.streams)}")
            print(filename)
            f_extension = filename.split('.')[-1]
            
            # parse out file extension stats
            if f_extension in list_file_extensions:
                file_extensions_stats[f_extension] = file_extensions_stats[f_extension] + 1
            else:
                list_file_extensions.append(f_extension)
                file_extensions_stats[f_extension] = 0
                file_extensions_stats[f_extension] = file_extensions_stats[f_extension] + 1
            
            # build file data stats
            file_data = {}
            file_data['fileName'] = filename
            file_data['streams'] = handler.streams
            file_data['extension'] = f_extension
            file_data['totalStreams'] = len(handler.streams)
            if os.path.isdir(filename):
                file_data['type'] = 'dir'
            else:
                file_data['type'] = 'file'

            file_data_stats.append(file_data) # add file data in dict

    # build extenstion data stas
    for ext in list(file_extensions_stats.keys()):
        ext_data = {}
        ext_data['extension'] = ext
        ext_data['total'] = file_extensions_stats[ext]
        ext_data['totalFiles'] = noOfFiles
        extension_stats.append(ext_data)

    # returning file and extension stats for csv report
    return file_data_stats, extension_stats

def out_csv_report(stats, fieldnames, report_name):   
    """create csv report from ADS stats

    Parameters:
    -----------
    stats : list
        ADS stats
    fieldnames : list
        list of column names
    report_name : str
        file name
    """

    with open(report_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in stats:
            writer.writerow(item)
    print(f"file saved: {report_name}")

if __name__ == "__main__":
    main()