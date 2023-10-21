#!/bin/bash

# Install necessary R packages and IRkernel
R -e "install.packages(c('repr', 'IRdisplay', 'evaluate', 'crayon', 'pbdZMQ', 'devtools', 'uuid', 'digest'), repos='https://cloud.r-project.org/')"
R -e "devtools::install_github('IRkernel/IRkernel')"
