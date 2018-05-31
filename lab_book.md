#### month/day/year

#### 04/27/2018
#### Getting the sequencing files
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

#### 05/15/2018
#### Merging files from different lanes
For each sample, it was done a paired-end sequencing, so that by the end of the process there was an R1 an R2 file for each condition. As each condition was sequenced in two different lanes of the sequencing machine, the whole process generated four files for the female and four files for the male genome:

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

#### 05/16/2018
#### Running FASTQC
The software FASTQC was used to assess the quality of the sequencing raw data. A total of 4 FASTQC runs were done, each of them taking
2-3 hours (MacOSX system with a 2.66 GHz Intel Core 2 Duo processor and 8GB RAM). The output of each run was an html file that contained
a graphical representation of all parameters analyzed. Those files can be found under the folder "FASTQC/sequencing_raw_data". 

----------------------------------------------------------------------------------------------------------------------------------------

#### 05/17/2018
#### Output analysis 
The output of FASTQC guides the next step of the workflow, where quality control and adaptor trimming are done (if necessary). It follows the analysis of the output for each sample: 

1) LF2-A_ACAGTG_R1_001

   It passed the test for all the 11 parameters. However, it raised a warning for "Per sequence GC content" and 
"Adapter Content". As for the former, its curve had a shape slightly deviated from a (expected) normal distribution. It was also possible to detect a second peak, even if very short. This second peak could represent adaptors remaining in the sample, as also indicated by the warning raised by the "Adapter Content" analysis. It is expected that adapter removal in the subsequent cleaning step should correct these warnings.  

----------------------------------------------------------------------------------------------------------------------------------------

#### 05/22/2018
#### Output analysis (continuation)

2) LF2-A_ACAGTG_R2_001

   Differently from LF2-A_ACAGTG_R1_001, LF2-A_ACAGTG_R2_001 showed a high proportion of bad quality nucleotides at the end of the sequence (from nucleotide 225 on), failing the "Per base sequence quality" parameter. This issue was likely caused by a problem at the tile 1115, that according to the "Per tile sequence quality" analysis, had a poor performance at the final nucleotides. This problem can be fixed by trimming of the bad quality region, in this case the last 25 nucleotides. As well as A_ACAGTG_R1_001, A_ACAGTG_R2_001 showed a GC peak slightly abnormal and a very subtle second peak. Again, this should be fixed by removal of adapters.     
   
3) LF6-A_GTGAAA_R1_001

   It showed the exact same pattern as LF2-A_ACAGTG_R1_001, passing all the tests and just raising warnings for "Per sequence GC content" and "Adapter Content". Adapter removal should be able to eliminate all those warnings. 
   
4) LF6-A_GTGAAA_R2_001

   The same pattern as LF2-A_ACAGTG_R2_001, failing at the "Per base sequence quality" test. However, the degeneration of quality occurred later on the sequenced: from the nucleotide 230 on. Then a trimming from this region on should fix the issue. As in all other samples, the GC curve raised a warning, probably due to the presence of adapters. Then trimming and adapter removal should be done for this sample.   
   
----------------------------------------------------------------------------------------------------------------------------------------

#### 05/26/2018
#### Trimming and quality control (Trimmomatic)

The software Trimmomatic was used to clip adapters out and to remove bad quality reads. The program was ran in the paired end mode, giving as input the pair of R1/R2 sequencing files. Then, a total of 2 runs were done: one for the male (LF-6) and one for te female (LF-2) genomes. Each run generated 4 output files (fastq): 

i) a file representing forward reads (R1) that still had a pair after quality control; 

ii) a file representing reverse reads (R2) that still had a pair after quality control; 

iii) a file representing forward reads that had no pair after quality control (their R2 pair was removed) and 

iv) a file representing reverse reads that had no pair after quality control.

#### Trimmomatic on the female genome

The command used to run the quality control of the female genome was:

$ java -jar /Users/bioma/Downloads/Trimmomatic-0.38/trimmomatic-0.38.jar PE -phred33 LF2-A_ACAGTG_R1_001.fastq.gz LF2-A_ACAGTG_R2_001.fastq.gz output_paired_LF2-A_ACAGTG_R1_001.fastq.gz output_unpaired_LF2-A_ACAGTG_R1_001.fastq.gz output_paired_LF2-A_ACAGTG_R2_001.fastq.gz output_unpaired_LF2-A_ACAGTG_R2_001.fastq.gz ILLUMINACLIP:/Users/bioma/Downloads/Trimmomatic-0.38/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 CROP:225

In this run, the TruSeq3-PE.fa adapters library was used to recognize and remove adapters sequences from the sequencing raw data. It also cut the last 25 nucleotides of all reads (CROP:225), as the previous FASTQC analysis had shown they had very low quality. The job took approximately 16 hours to run in a MacOSX system with a 2.66 GHz Intel Core 2 Duo processor and 8GB RAM. Trimmomatic's output shows the percentage of reads remaining after processing:

Input Read Pairs: 223981456 
Both Surviving: 193554993 (86.42%) 
Forward Only Surviving: 30125366 (13.45%) 
Reverse Only Surviving: 273794 (0.12%) 
Dropped: 27303 (0.01%)

#### FASTQC analysis of quality controled female genome

Again, the software FASTQC was used to assess the quality of our sequencing files, now the ones that went through adapters removal and quality control pipeline. As expected, the Trimmomatic run removed all the adapters and low quality regions from the reads. The only parameters that remained with a warning after Trimmomatic were: 

1) Per tile sequence quality:

   The warning was only raised for the R2 files, indicating a problem at the tile 1115. However, this problem didn't seem to compromise the overall quality of the sequencing. 
   
2) Per sequence GC content: 

   The warning was present in all files indicating that a kind of bias may have happened at the library preparation. The second peak, that could indicate contamination of sample, was eliminated in all paired files, but remained in the unpaired ones. 
   
3) Sequence length distribution:

   This warning was raised due to the CROP command, so it is only an artefact and it shouldn't concern us. 

All the html files containing the FASTQC analysis of the quality controled data can be found at the folder "FASTQC/after_trimmomatic"

----------------------------------------------------------------------------------------------------------------------------------------

#### 05/30/2018
#### Trimmomatic on the male genome

The command used to run the quality control of the male genome was:

$ java -jar /Users/bioma/Downloads/Trimmomatic-0.38/trimmomatic-0.38.jar PE -phred33 LF6-A_GTGAAA_R1_001.fastq.gz LF6-A_GTGAAA_R2_001.fastq.gz output_paired_LF6-A_GTGAAA_R1_001.fastq.gz output_unpaired_LF6-A_GTGAAA_R1_001.fastq.gz output_paired_LF6-A_GTGAAA_R2_001.fastq.gz output_unpaired_LF6-A_GTGAAA_R2_001.fastq.gz ILLUMINACLIP:/Users/bioma/Downloads/Trimmomatic-0.38/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 CROP:230

The same parameters were used in as in the female genome processing, only difference being the CROP flag, that cut off the last 20 nucleotides in the male genome (CROP:230) and 25 in the female genome (CROP:225). The job took approximately 14h to finish in a MacOSX system with a 2.66 GHz Intel Core 2 Duo processor and 8GB RAM. Find the summary of the processing step below:

Input Read Pairs: 191753950 
Both Surviving: 167036203 (87.11%) 
Forward Only Surviving: 24441370 (12.75%) 
Reverse Only Surviving: 247096 (0.13%) 
Dropped: 29281 (0.02%)

----------------------------------------------------------------------------------------------------------------------------------------

#### 05/31/2018
#### FASTQC analysis of quality controled male genome 

The FASTQC analysis of LF6 data after processing showed that Trimmomatic was effective in selecting good quality data (see all 4 files at folder "FASTQC/after_trimmomatic". The two files that had paired data (output_paired_LF6-A_GTGAAA_R1_001 e output_paired_LF6-A_GTGAAA_R2_001) have passed the quality test for all the parameters analysed, only raising a warning for the "Per sequence GC content" and "Sequence length distribution". As already explained at "FASTQC analysis of quality controled female genome", those warnings should not be a concern. The unpaired R1 file (output_unpaired_LF6-A_GTGAAA_R1_001) also showed really good quality, passing in all tests, except for the "Sequence length distribution". The warning was raised due to the presence of reads of different lengths. However, as explained in the FASTQC Manual, this type of warning can be ignored, since it is entirely normal for some sequencing platforms to have reads of different lengths. The unpaired R2 file (output_unpaired_LF6-A_GTGAAA_R1_001) was the only one that failed the FASTQC test for a parameter: it failed the "Per sequence GC content". This failure can be explained by a second peak of 60% GC content that pretty much merged with the main 34% peak expected for a *Limnoperna fortunei* genome. A further step of removal of sequences of 60% GC content could solve this issue.      
