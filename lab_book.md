#month/day/year

#04/27/2018
#Getting the sequencing files
The innovation center that sequenced the genomes (POLO D’INNOVAZIONE DI GENOMICA, GENETICA E BIOLOGIA) sent the data in a HD. However, the 
HD was held at the Customs and the taxes we would have to pay to retrieve it were too high. So we suggested Laura Chiti (innovation 
center's representative) to share the files via Google Cloud. 

The fisrt attempt was to create a virtual machine to function as a FTP server. Then, Laura could upload the sequencing files after 
connecting to the FTP link and registering the user credentials. However, we could not establish the server since external access was
repeatdly blocked by the virtual machine's firewall.

Another way of sharing files through GCloud is by using the Google Cloud Storage service. The idea is to create a bucket and share it with
other users, so that they can upload/download files to it. The bucket was created (named "biobureau-upload") and shared doing the following
steps (assuming you have Goodle Cloud SDK installed in your machine):  

	1) Create a bucket where the files will be stored
		- gsutil mb gs://biobureau-upload
	2) Give permissions for another user to read/write from/to the bucket
		- gsutil acl ch -u googleaccount@gmail.com:W gs://biobureau-upload
		Important: the user to whom the bucket is being shared need to be a Google Account

After these two steps, the user invited to collaborate in the bucket should be able to access through the link:
https://console.cloud.google.com/storage/browser/name-of-the-bucket

Which should be, for the bucket created:
https://console.cloud.google.com/storage/browser/biobureau-upload

A login page should be prompted and after logging in the user is forwarded to the bucket's page at Google Cloud Console. Now uploading 
files is a simple matter of clicking on the upload button. 

----------------------------------------------------------------------------------------------------------------------------------------

#05/15/2018
#Merging files from different lanes
For each sample, it was done a paired-end sequencing, so that by the end of the process there was an R1 an R2 file for each condition. As 
each condition was sequenced in two different lanes of the sequencing machine, the whole process generated four files for the female and 
four files for the male genome:

-rw-r--r--  1 root   staff    19G May  8 04:21 LF6-A_GTGAAA_L001_R1_001.fastq.gz
-rw-r--r--  1 root   staff    20G May  8 12:12 LF6-A_GTGAAA_L001_R2_001.fastq.gz
-rw-r--r--  1 root   staff    19G May  9 03:40 LF6-A_GTGAAA_L002_R1_001.fastq.gz
-rw-r--r--  1 root   staff    20G May  9 17:25 LF6-A_GTGAAA_L002_R2_001.fastq.gz

Where the suffix L00X indicates the lane where the sequencing was done, and the suffix RX indicates if the data represents the forward (R1)
or reverse (R2) reads. 

Before proceeding to the following steps, the files that represented the same sample and set of reads (but that came from different lanes) 
should be merged. One could do this using the "cat" command on a Unix system:

$ cat LF6-A_GTGAAA_L001_R1_001.fastq.gz LF6-A_GTGAAA_L002_R1_001.fastq.gz > LF6-A_GTGAAA_R1_001.fastq.gz

As in the above example, the cat command generated a unique file that represented the set of forward reads of the male genome, previously 
divided into two different files. On a MacOSX system with a 2.66 GHz Intel Core 2 Duo processor and 8GB RAM, this process took 9h43min. 
Interestingly, When the cat command was ran for the files representing the reverse reads (R2), the process took only 4h13min:

$ cat LF6-A_GTGAAA_L001_R2_001.fastq.gz LF6-A_GTGAAA_L002_R2_001.fastq.gz > LF6-A_GTGAAA_R2_001.fastq.gz

Since the R2 files were actually 1 GB bigger than the R1 and the machine used for running the command was the same, it remains a mistery 
why the second round of merging ran so much faster. 

----------------------------------------------------------------------------------------------------------------------------------------

#05/16/2018
#Running FASTQC
The software FASTQC was used to assess the quality of the sequencing raw data. A total of 4 FASTQC runs were done, each of them taking
2-3 hours (MacOSX system with a 2.66 GHz Intel Core 2 Duo processor and 8GB RAM). The output of each run was an html file that contained
a graphical representation of all parameters analyzed. Those files can be found under the folder "FASTQC/sequencing_raw_data". 

----------------------------------------------------------------------------------------------------------------------------------------

#05/17/2018
#Output analysis 
The output of FASTQC guides the next step of the workflow, where quality control and adaptor trimming are done (if necessary). It follows
the analysis of the output for each sample: 

1) LF2-A_ACAGTG_R1_001: it passed the test for all the 11 parameters. However, it raised a warning for "Per sequence GC content" and 
"Adapter Content". As for the former, its curve had a shape slightly deviated from a (expected) normal distribution. It was also possible
to detect a second peak, even if very short. This second peak could represent adaptors remaining in the sample, as also indicated by the 
warning raised by the "Adapter Content" analysis. It is expected that adapter removal in the subsequent cleaning step should correct these
warnings.   

