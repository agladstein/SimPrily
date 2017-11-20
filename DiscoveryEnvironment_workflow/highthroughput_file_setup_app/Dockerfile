FROM ubuntu:16.04
MAINTAINER bjoyce3<bjoyce3@email.arizona.edu>
LABEL Description "This dockerfile is for setting up SimPrily HT execution as a workflow on the CyVerse Discovery Environment"

RUN apt-get update
ADD SimPrily_HTfile_setup_workflow.sh /usr/bin/
RUN chmod +x /usr/bin/SimPrily_HTfile_setup_workflow.sh
ENTRYPOINT ["SimPrily_HTfile_setup_workflow.sh"]
