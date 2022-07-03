# Alternate-Data-Streams

## Synopsis
A suite of python tools to work with Alterndate Data Streams (ADS) in the NTFS file system.

## Description

The tools use [pyADS](https://github.com/RobinDavid/pyADS) from [RobinDavid](https://github.com/RobinDavid) to access the alternate data streams. I modified pyADS to work better with my tools, therefore I have uploaded it to this repositiory. 

I created 5 tools to interact with alternate data streams:
1. get-streams.py
2. read-stream.py
3. write-stream.py
4. delete-stream.py
5. find-fileStreams.py

## get-streams.py
Displays all data streams within a file.

### usage

**Parameter -f, --file**
- type : str
- the file path to a file

**Example 1**
`py get-streams.py --file my_secret.txt`
 - returns all data stream names
 
 **Example 2**
 `py get-streams.py -f C:\data\ADS\my_secret.txt`
 - uses the alias of parameter `--file` to specify the file path
