echo "STARTING FAST SETUP" && cd setup && cd astropy && sudo python3 setup.py build && sudo python3 setup.py install && cd .. && cd sewpy && sudo python3 setup.py install && cd .. && ls -l && sudo alien -i sextractor-2.19.5-1.x86_64.rpm && cd fitsio && sudo python3 setup.py build && sudo python3 setup.py install && echo "DONE"
