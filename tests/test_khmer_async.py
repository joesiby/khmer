#
# This file is part of khmer, http://github.com/ged-lab/khmer/, and is
# Copyright (C) Michigan State University, 2009-2013. It is licensed under
# the three-clause BSD license; see doc/LICENSE.txt.
# Contact: khmer-project@idyll.org
#
# pylint: disable=missing-docstring,protected-access
import khmer
import time

from screed.fasta import fasta_iter
import screed

import khmer_tst_utils as utils
from nose.plugins.attrib import attr

def teardown():
    utils.cleanup()

def test_async_submodule():
    try:
        from khmer import async
    except ImportError as e:
        print e
        assert False

def test_n_processed():
    filename = utils.get_test_data('test-reads.fa')
    ht = khmer.new_counting_hash(20, 1e7, 4)
    
    asd = khmer.async.AsyncDiginorm(ht)
    asd.start(filename, 1000, False, 1)
    time.sleep(.4)
    asd.stop()

    print asd.n_processed()
    assert asd.n_processed() == 25000L

def test_n_kept():
    filename = utils.get_test_data('test-reads.fa')
    ht = khmer.new_counting_hash(20, 1e7, 4)
    
    asd = khmer.async.AsyncDiginorm(ht)
    asd.start(filename, 1000, False, 1)
    time.sleep(.4)
    asd.stop()

    print asd.n_kept()
    assert asd.n_kept() == 25000L

def test_n_parsed():
    filename = utils.get_test_data('test-reads.fa')
    ht = khmer.new_counting_hash(20, 1e7, 4)
    
    asd = khmer.async.AsyncDiginorm(ht)
    asd.start(filename, 1000, False, 1)
    time.sleep(.4)
    asd.stop()

    print asd.n_parsed()
    assert asd.n_parsed() == 25000L

def test_async_diginorm_pair_fail():
    filename = utils.get_test_data('paired-mixed.fa')
    ht = khmer.new_counting_hash(20, 1e7, 4)
    
    asd = khmer.async.AsyncDiginorm(ht)
    asd.start(filename, 1000, True, 1)
    time.sleep(.4)

    try:
        asd.check_exception()
    except IOError as e:
        print "Caught an exception"
        print e
        #asd.stop()
    else:
        print "Failed to catch exception"
        #asd.stop()
        assert False

def test_async_diginorm_paired():
    filename = utils.get_test_data('paired.fa')
    ht = khmer.new_counting_hash(20, 1e7, 4)
    
    asd = khmer.async.AsyncDiginorm(ht)
    asd.start(filename, 1000, True, 1)
    time.sleep(.4)

    try:
        asd.check_exception()
    except IOError as e:
        print e
        assert False
    else:
        rcount = 0
        for r1, r2 in asd.processed():
            assert r1.name
            assert r2.name
            assert r1.sequence
            assert r2.sequence
            assert "895:1:37:17593:9954/1" in r1.name
            assert "895:1:37:17593:9954/2" in r2.name
            rcount += 2
        assert rcount == 6 



def test_async_diginorm():
    filename = utils.get_test_data('test-reads.fa')
    ht = khmer.new_counting_hash(20, 1e7, 4)
    
    asd = khmer.async.AsyncDiginorm(ht)
    asd.start(filename, 5, False, 1)
    time.sleep(1)
    asd.stop()

    assert asd.n_kept() < 24995L