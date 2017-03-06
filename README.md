[![Code Climate](https://codeclimate.com/github/dblume/wine-tasting/badges/gpa.svg)](https://codeclimate.com/github/dblume/wine-tasting)
[![Issue Count](https://codeclimate.com/github/dblume/wine-tasting/badges/issue_count.svg)](https://codeclimate.com/github/dblume/wine-tasting)
[![License](https://img.shields.io/badge/license-MIT_license-blue.svg)](https://github.com/dblume/wine-tasting/blob/master/LICENSE.txt)
![python2.x](https://img.shields.io/badge/python-2.x-yellow.svg)
# wine-tasting

An attempt to solve [the Wine Tasting problem at Bloomreach](http://bloomreach.com/puzzles/) in Python.

#### Results from my cygwin sandbox

    $ time ./wine_allocator.py person_wine_3.txt > pw3_out.txt; head -n 1 pw3_out.txt

    real    0m5.866s
    user    0m3.291s
    sys     0m2.558s
    300000

    $ time ./wine_allocator.py person_wine_4.txt.zip > pw4_out.txt; head -n 1 pw4_out.txt

    real    0m53.804s
    user    0m43.586s
    sys     0m10.124s
    2918548

#### To Do

There is room for experimentation and optimizations. I'd like to see if I can make the recursive remove\_person calls work. May have to make those calls after the "for wine in wines" loop.

