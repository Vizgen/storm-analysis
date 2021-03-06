#!/usr/bin/env python
"""
Analyze test data using Multiplane

Hazen 01/18
"""
import glob
import numpy
import os
import time

import storm_analysis.multi_plane.kmeans_classifier as kMeansClassifier
import storm_analysis.multi_plane.kmeans_measure_codebook as kMeansMeasureCodebook
import storm_analysis.multi_plane.multi_plane as mp


def analyzeData():
    
    dirs = sorted(glob.glob("test*"))

    for a_dir in dirs:
        print()
        print("Analyzing:", a_dir)
        print()
    
        mlist = a_dir + "/test.hdf5"

        # Remove stale results, if any.
        if os.path.exists(mlist):
            os.remove(mlist)

        # Run analysis.
        start_time = time.time()
        mp.analyze(a_dir + "/test", mlist, "multicolor.xml")

        # Categorize results using k-means clustering.
        #
    
        # Measure codebook.
        print("Measuring k-means codebook.")
        codebook = kMeansMeasureCodebook.KMeansMeasureVectors(os.path.join(a_dir, "test.hdf5"), 4)
        numpy.save(os.path.join(a_dir, "codebook.npy"), codebook)
        
        # K-means cluster.
        print("k-means clustering.")
        codebook = numpy.load(os.path.join(a_dir, "codebook.npy"))
        kMeansClassifier.KMeansClassifier(codebook,
                                          os.path.join(a_dir, "test.hdf5"),
                                          max_distance = 80.0)
        
        stop_time = time.time()

        # Save timing results.
        print("Analysis completed in {0:.2f} seconds".format(stop_time - start_time))

        with open(a_dir + "/timing.txt", "w") as fp:
            fp.write(str(stop_time - start_time) + "\n")

if (__name__ == "__main__"):
    analyzeData()
    
