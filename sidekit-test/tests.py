#Idmap: are used to store two lists of strings and to map between them
import numpy
import sidekit

idmap= sidekit.IdMap()
idmap.leftids = numpy.array(["model_1", "model_2", "model_3"])
idmap.rightids = numpy.array(["segment_1", "segment_2", "segment_3"])
idmap.start = numpy.empty((3), dtype="|O")
idmap.stop = numpy.empty((3), dtype="|O")

print('Idmap %s '% idmap.validate())

#Ndx: Ndx objects store trials index information - Combination
# of model and segment IDs that should be evaluated by system 
# which will produce a score for those trials

#Trialmask: Matrix of boolean m-by-n, m is number of unique models
# and n is number of unique segments

import numpy
import sidekit

ndx = sidekit.Ndx()
ndx.modelset = numpy.array(["model_1", "model_2"])
ndx.segset = numpy.array(["segment_1", "segment_2", "segment_3"])
ndx.trialmask = numpy.ones((2,3), dtype='bool')
print('Ndx %s '% ndx.validate())

#Keys: Are used to store information about which trial is a target trial and
# which one is a non-target trial. tar(i, j) is true if the test between model i 
# and segment j is target

import numpy
import sidekit

key = sidekit.Key()
key.modelset = ndx.modelset
key.segset = ndx.segset
key.tar = numpy.zeros((2,3), dtype='bool')
key.tar[0, 0] = True
key.tar[1:, 1:] = True
key.non = numpy.zeros((2,3), dtype='bool')
key.non[0, 1:] = True
key.non[1, 0] = True
print('Key %s '% key.validate())