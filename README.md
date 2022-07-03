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

### Usage

**Parameter -f, --file**
- type : str
- the file path to a file

**Example 1**

`py get-streams.py --file my_secret.txt`
 - returns all data stream names
 
 **Example 2**
 
 `py get-streams.py -f C:\data\ADS\my_secret.txt`
 - uses the alias of parameter `--file` to specify the file path
 - returns all data stream names

## read-stream.py
Displays the content of a data stream.

**Parameter -f, --file**
- type : str
- the file path to a file

**Parameter -n, --name**
- type : str
- data stream name

**Example 1**

`py read-stream.py --file my_secret.txt --name test`
- displays the content of data stream test from file my_secret.txt

**Example 2**

`py read-stream.py -f C:\data\ADS\my_secret.txt -n 'test,test2'`
- uses the alias of parameter `--file` to specify the file path
- uses the alias of parameter `--name` to spcifiy two data stream names
- displays the content of data streams test and test2 from file my_secret.txt
