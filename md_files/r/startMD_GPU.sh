#!/usr/bin/bash

################################################################################
#  This bash script submits MD simulations as replica to desmond with slurm.   #
# Place this script in the folder with the cms-, msj- and cfg-file and change  #
# variables according to your system setup and project.                        #
################################################################################

# @author david schaller

# job settings
REPLICA=5
NAME=cyp19_18r
QUEUE=any-gpu
CMS=cyp19_18r.cms # name of cms file
MSJ=cyp19_18r.msj # name of msj file
CFG=cyp19_18r.cfg # name of cfg file

# directory of schrodinger installation
SCHRODINGER=/software/desmond/2022-1

# submit jobs
for counter in $(seq 0 $((REPLICA - 1)))
do
  if [ -d "$counter" ]; then
    rm -r $counter
  fi
  mkdir $counter
  echo "Copying files for ${counter} ..."
  cp ${MSJ} ${CMS} ${counter}
  /usr/bin/sed "s/seed = 2007/seed = $((2007+$counter))/" ${CFG} > $counter/${CFG}
  cd $counter
  echo "Submitting replica ${counter} ..."
  $SCHRODINGER/utilities/multisim \
    -JOBNAME ${NAME}_${counter} \
    -HOST ${QUEUE} \
    -maxjob 1 \
    ${CMS} \
    -m ${MSJ} \
    -c ${CFG} \
    -o ${NAME}_${counter}-out.cms \
    -mode umbrella \
    -set 'stage[1].set_family.md.jlaunch_opt=["-gpu"]'
  cd ..
done
