

## find_matches_shm: (spawn + SharedMemory)

Chunks Read: 14 Elapsed time: 11.7454 seconds.
Chunks Read: 28 Elapsed time: 27.4473 seconds.
Chunks Read: 42 Elapsed time: 41.9583 seconds.
Chunks Read: 56 Elapsed time: 56.2905 seconds.

Could be some copies still be made.

## FindMatches

Chunks Read: 14 Elapsed time: 15.3 seconds.
Chunks Read: 28 Elapsed time: 30.0 seconds.
Chunks Read: 42 Elapsed time: 45.2 seconds.
Chunks Read: 56 Elapsed time: 60.4 seconds.
Chunks Read: 70 Elapsed time: 75.7 seconds.
Chunks Read: 84 Elapsed time: 91.0 seconds.
Chunks Read: 98 Elapsed time: 106.3 seconds.
Chunks Read: 112 Elapsed time: 121.7 seconds.

Pretty similar to the previous result. We are probably constraint by read a lot.


Interesting if we keep processes alive. And just communicate the data.

Right now the data is located on APPLE HDD ST1000LM024, where
* Maximum interface speed 300 MB/s
* Maximum buffered read speed 223 MB/s
* Maximum read speed 100 MB/s 
So, we will almost always be bound by the hard drive IO.