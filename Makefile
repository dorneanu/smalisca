# Makefile for smalisca
# 

PYTHON 			= `which python`
SETUPFILE		= setup.py
INSTALLFILES	= install.record
BUILDDIRS		= build dist smalisca.egg-info

help:
	@echo "----------------------------------------------------------------------"
	@echo "Please use 'make <target>' where <target> is one of"
	@echo " install         to install smalisca"
	@echo " uninstall       to remove smalisca"
	@echo " clean           to clean directory"
	@echo "----------------------------------------------------------------------"

clean:
	rm -rf ${BUILDDIRS}

install:
	${PYTHON} setup.py install --record ${INSTALLFILES}
	@echo -e "\n\n* SUCCESS: Install complete."


uninstall:
	cat ${INSTALLFILES} | xargs rm -rf
	@echo -e "\n\n* SUCCESS: Uninstall complete."
	rm ${INSTALLFILES}
