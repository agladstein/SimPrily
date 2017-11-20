FROM python:2.7
MAINTAINER bjoyce3<bjoyce3@email.arizona.edu>
LABEL Description "This dockerfile will accept a user defined output folder from SimPrily HT execution on the CyVerse Discovery Environment and concatenate all of the results files from individual files into a single file with one header. Each line in the concatenated file will be the output from a single simulation. This concatenated file will then be assessed by SimPrily to compare to real data in a downstream step."

ADD SimPrily_concatenate_workflow.py /usr/local/bin/
RUN chmod +x /usr/local/bin/SimPrily_concatenate_workflow.py
ENTRYPOINT ["SimPrily_concatenate_workflow.py"]