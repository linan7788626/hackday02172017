# This script export Nan's simulations to a nice HDF5 format
from astropy.table import Table, vstack
import pyfits as fits
import numpy as np
import glob
import os

# Path to the extracted archive
dataset_path='/data2/LSST_SL/data_of_lsst/'

# Path to the export data
export_path='/data2/projects/DeepLens/data/'

categories = ['single', 'stack']

for cat in categories:

    sub_dir = os.path.join(dataset_path, 'lsst_mocks_'+cat, 'lensed_outputs/1')

    # Extract the fields related to the images
    l = glob.glob(sub_dir+'/*')
    ids = [int(g.split('_')[::-1][6]) for g in l]
    col1 = [float(g.split('_')[::-1][5]) for g in l]
    col2 = [float(g.split('_')[::-1][4]) for g in l]
    col3 = [float(g.split('_')[::-1][3]) for g in l]
    col4 = [float(g.split('_')[::-1][2]) for g in l]
    col5 = [float(g.split('_')[::-1][1]) for g in l]

    # Create array to store images
    x = np.zeros((len(ids), 1, 45, 45))

    print "Loading images from " + sub_dir
    for i, fname in enumerate(l):
        x[i,0] = fits.getdata(fname)

    # Create the Table
    cat_lensed = Table([ids, col1, col2, col3, col4, col5, x],
                names=['ID', 'col1', 'col2', 'col3', 'col4', 'col5', 'image'])

    cat_lensed['is_lens'] = 1

    # Same thing for the unlensed outputs

    sub_dir = os.path.join(dataset_path, 'lsst_mocks_'+cat, 'unlensed_outputs/1')

    # Extract the fields related to the images
    l = glob.glob(sub_dir+'/*')
    ids = [int(g.split('_')[::-1][6]) for g in l]
    col1 = [float(g.split('_')[::-1][5]) for g in l]
    col2 = [float(g.split('_')[::-1][4]) for g in l]
    col3 = [float(g.split('_')[::-1][3]) for g in l]
    col4 = [float(g.split('_')[::-1][2]) for g in l]
    col5 = [float(g.split('_')[::-1][1]) for g in l]

    # Create array to store images
    x = np.zeros((len(ids), 1, 45, 45))

    print "Loading images from " + sub_dir
    for i, fname in enumerate(l):
        x[i,0] = fits.getdata(fname)

    # Create the Table
    cat_unlensed = Table([ids, col1, col2, col3, col4, col5, x],
                names=['ID', 'col1', 'col2', 'col3', 'col4', 'col5', 'image'])

    cat_unlensed['is_lens'] = 0

    catalog = vstack([cat_lensed, cat_unlensed])

    # Save the catalog
    catalog.write(export_path+'data_lsst.hdf5', path='/'+cat, append=True)
