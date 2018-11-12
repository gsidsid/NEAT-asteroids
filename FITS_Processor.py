from astropy.io import fits
from astropy import units as u
from astropy.wcs import WCS
from astropy.nddata import CCDData
import ccdproc
from sewpy import sewpy
import numpy as np
import matplotlib.pyplot as plt
import glob, os

flats_folder_format='flats'
darks_folder_format='darks'
lights_folder_format='obsdata'

geodss_data_volume='geodss/data'
tricam_data_volume='tricam/data'
tricam2_data_volume='tricam2/data'

sextractor_params='sexconf'
sextractor_output='sexout'
processed_volume='preprocessed'

def formFITSPaths(sample):
	paths = dict()
	paths['darks'] = geodss_data_volume+'/'+sample+'/'+darks_folder_format
	paths['flats'] = geodss_data_volume+'/'+sample+'/'+flats_folder_format
	paths['lights'] = geodss_data_volume+'/'+sample+'/'+lights_folder_format
	return paths

def findFITSFiles(sample):
	paths = formFITSPaths(sample)
	files = dict()
	files['darks']=glob.glob(paths['darks']+'/*.fit')
	files['flats']=glob.glob(paths['flats']+'/*.fit')
	files['lights']=glob.glob(paths['lights']+'/*.fit')
	return files

def primaryHDU(file):
	hdulist = fits.open(file)
	hdu = hdulist[0]
	return hdu

def HDU2CCD(hdu):
	CCD = CCDData(hdu.data[:,:], unit='adu')
	return CCD

def preprocessSampleData(idx, FITSFiles):
	sample_processed = []
	dark=HDU2CCD(primaryHDU(FITSFiles['darks'][0]))
	flat=HDU2CCD(primaryHDU(FITSFiles['flats'][0]))
	lights=FITSFiles['lights']
	lighted = HDU2CCD(primaryHDU(lights[idx]))
	dark_subtracted = ccdproc.subtract_dark(lighted, dark, dark_exposure=20*u.second, data_exposure=20*u.second, scale=True)
	flat_corrected = ccdproc.flat_correct(dark_subtracted,flat)
	path_plan = processed_volume+"/"+sample+"/"
	try:
		os.makedirs(path_plan)
		flat_corrected.write(path_plan+str(idx)+'.fits')
	except Exception as e:
		print(e)
	return flat_corrected

def process(sample,idx):
	preprocessSampleData(idx,findFITSFiles(sample)).to_hdu()[0]

sample='g19960418'
light_id = 1

print("Processing sample " + sample + " #" + str(light_id) + "...")
process(sample, light_id)
print("Done.")