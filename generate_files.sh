#!/bin/tcsh

@ i = 1
while ($i <= 24) #up to number of files needed
  mkdir options/options-$i
  cp -r options_BASE/* options/options-$i/
  cp releases/RELEASES-$i options/options-$i/RELEASES
  cp commands/COMMAND-$i options/options-$i/COMMAND
  mkdir /work/users/sarahgj/M91/Bromoform_F92/outputs-$i
  @ i += 1
end

exit

#Run with: 
#chmod +x generate_files.sh
#./generate_files.sh
