[![Code Climate](https://codeclimate.com/github/dblume/wine-tasting/badges/gpa.svg)](https://codeclimate.com/github/dblume/wine-tasting)
[![Issue Count](https://codeclimate.com/github/dblume/wine-tasting/badges/issue_count.svg)](https://codeclimate.com/github/dblume/wine-tasting/issues)
[![License](https://img.shields.io/badge/license-MIT_license-blue.svg)](https://github.com/dblume/wine-tasting/blob/main/LICENSE.txt)
![python2.x](https://img.shields.io/badge/python-2.x-yellow.svg)
# wine-tasting

An attempt to solve [the Wine Tasting problem at Bloomreach](http://bloomreach.com/puzzles/) in Python.

## Description

A large group of friends from the town of Nocillis visit the vineyards of Apan to taste wines. The vineyards produce many fine wines and the friends decide to buy as many as 3 bottles of wine each if they are available to purchase. Unfortunately, the vineyards of Apan have a peculiar restriction that they can not sell more than one bottle of the same wine. So the vineyards come up with the following scheme: They ask each person to write down a list of up to 10 wines that they enjoyed and would be happy buying. With this information, please help the vineyards maximize the number of wines that they can sell to the group of friends.

#### Input 
A two-column TSV file with the first column containing the ID (just a string) of a person and the second column the ID of the wine that they like. Here are three input data sets of increasing sizes. Please send us solutions even if it runs only on the first file.

* [person_wine_3.txt](https://s3.amazonaws.com/br-user/puzzles/person_wine_3.txt)
* [person_wine_4.txt.zip](https://s3.amazonaws.com/br-user/puzzles/person_wine_4.txt.zip)
* [person_wine_5.txt.zip](https://s3.amazonaws.com/br-user/puzzles/person_wine_5.txt.zip)

#### Output 
First line contains the number of wine bottles sold in aggregate with your solution. Each subsequent line should be two columns, tab separated. The first column is an ID of a person and the second column should be the ID of the wine that they will buy.

Please check your work. Note that the IDs of the output second column should be unique since a single bottle of wine can not be sold to two people and an ID on the first column can appear at most three times since each person can only buy up to 3 bottles of wine.

## Results from my cygwin sandbox

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

## To Do

There is room for experimentation and optimizations. I'd like to see if I can make the recursive remove\_person calls work. May have to make those calls after the "for wine in wines" loop.
