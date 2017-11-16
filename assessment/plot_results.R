# Title     : TODO
# Objective : TODO
# Created by: agladsteinNew
# Created on: 11/2/17

args<-commandArgs(TRUE)
if (length(args)<3) {
  stop("Three arguments must be supplied (sim input file), (real input file), (header)", call.=FALSE)
} else{
  print(args)
}

file_sim<-args[1] #simulation output, should have the form input_ABCtoolbox_M1_HPC.txt
file_real<-args[2] #real data, should have the form real_output_M23.summary
header<-args[3] #header of simulation containing desired columns

input_ABCtoolbox<-read.table(file_sim, header = T);
real_output<-read.table(file_real, header = T);
keep<-scan(header, character(), quote="")

out_params<-paste(strsplit(file_sim, ".txt")[[1]],"_params.pdf", sep="")
out_stats<-paste(strsplit(file_sim, ".txt")[[1]],"_stats.pdf", sep="")
out_pca<-paste(strsplit(file_sim, ".txt")[[1]],"_pca.pdf", sep="")

# extract columns containing stats. could use for loop to look for the first stat. or use real output to find the stats.