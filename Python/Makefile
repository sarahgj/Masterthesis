##############################################################
## Makefile that does all the plotting for my master thesis ##
## Made by: Sarah Gjermo, 22.03.2017			    ##
##							    ##
## REMEMBER!!						    ##
## >> module use --append /projects/NS1000K/modulefiles	    ##
## >> module load python/anaconda			    ##
##############################################################


# Automated variables
# $< is first dependency
# $^ is all dependencies
# $@ is the target

.PHONY: colorlines
colorlines:
	python colorlines_Flex.py ASTRA M TTP h n


.PHONY: ASTRA_M
ASTRA_M:
	python fluxes_plots.py ASTRA M
	python entrainment_plot.py ASTRA M
	python released_entrained_correlation ASTRA M


.PHONY: all
 # By default, makefile operates on files so if there will be a file called all it will try to use it instead of a command. To avoid this use .PHONY before attributing.
all:
	python Scripts/Python/colorlines_Flex.py ASTRA h M 1000
	python Scripts/Python/colorlines_Flex.py ASTRA h M TTP


.PHONY: methyliodide_ASTRA
methyliodide_ASTRA:
	python Scripts/Python/colorlines_Flex.py ASTRA h M 1000
	python Scripts/Python/colorlines_Flex.py ASTRA h M TTP
	python Scripts/Python/entrainedTTP_Flex.py ASTRA
	python Scripts/Python/entrainment_plot.py ASTRA

.PHONY: help
help:
	@echo "	make all: Run the whole project."
	@echo "	make methyliodide_ASTRA: Runs all scripts for methyliodide ASTRA."

#There is @ before each echo because by default make prints every line to the console before it's executed. At sign is to suppress this and @ is discarded before line is passed to the shell.