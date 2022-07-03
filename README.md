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

### Usage

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

## write-stream.py
Writes data to a file stream.

### Usage

**Parameter -f, --file**
- type : str
- the file path to a file

**Parameter -n, --name**
- type : str
- data stream name

**Parameter -d, --data**
- type : str
- data to write
- you can supply a file path to write a file's contents

**Parameter -a, --append**
- type : bool
- write data in append mode

**Example 1**

`py write-stream.py --file my_secret.txt --name marvel --data "peter parker is spiderman"`
- writes data to data stream marvel in file my_secret.txt

**Example 2**

`py write-stream.py -f C:\data\ADS\my_secret.txt -n token -d "blah.txt"`
- uses the alias of parameter `--file` to specify the file path
- uses the alias of parameter `--name` to specify the data stream name
- uses the alias of parameter `--data` to specify the data to write
- writes the content of file blah.txt to the specified data stream 

## delete-stream.py
Removes a data stream from a file.

### Usage

**Parameter -f, --file**
- type : str
- the file path to a file

**Parameter -n, --name**
- type : str
- data stream name

**Example 1**

`py delete-stream.py --file my_secret.txt --name marvel`
- removes data stream marvel from file my_secret.txt

**Example 2**

`py delete-stream.py -f C:\data\ADS\my_secret.txt -n token`
- uses the alias of parameter `--file` to specify the file path
- uses the alias of parameter `--name` to specify the data stream name

## find-fileStreams.py
Outputs 3 different CSV reports for analyzing alternate data streams from a host.

### Report Types
**(f) file report**

This report is used to identify all files with ADS.

**(e) extension report**
This report is used to idenitfy the top file extension with ADS.

**(z) zone.identifer report**
This report is used to identify the content of the Zone.Identifer ADS

All reports are saved in the current working directory. 

### Usage

**Parameter -d, --dir**
- required
- type : str
- directory path to read files from


**Parameter -r, --recursive**
- type : bool
- recursive read files from the specified directory path


**Parameter -o, --options**
- type : str
- file report options
- allowed values:
    - a : run all reports
    - f : run file report
    - e : run run extension report
    - z : run zone.identifer report
- default : a

**Example 1**

`py find-fileStreams.py -f C:\data\ADS\`
- outputs all reports from files within directory C:\data\ADS\

**Example 2**

`py find-fileStreams.py -f C:\data\ADS\ -o fz`
- outputs file and zone.identifer reports

**Example 3**

`py find-fileStreams.py -f C:\data\ADS\ -o ze -r`
- recusive read all files within directory C:\data\ADS\
- outputs zone.identifier and extension report
