#!/usr/bin/env python -u

"""Solve the Wine Tasting problem at http://bloomreach.com/puzzles/"""

from os import remove
import time
import zipfile
from collections import defaultdict
from optparse import OptionParser
from tempfile import NamedTemporaryFile

__author__ = "David Blume"
__copyright__ = "Copyright 2014, David Blume"
__license__ = "http://www.wtfpl.net/"

# Nobody may buy more than this many bottles of wine
max_wines_per_person = 3


def verify_result_file(filename):
    """
    Ensures the results contain non-repeating wines and
    no more than (max_wines_per_person) instances of the same person.

    :param filename: The name of the results file to verify
    """
    wines = set()
    people = defaultdict(int)
    with open(filename, 'r') as f:
        for line in f:
            person, wine = line.strip().split('\t')
            assert(wine not in wines)
            wines.add(wine)
            people[person] += 1
            assert(people[person] <= max_wines_per_person)


class WineAllocator(object):

    def __init__(self):
        self.people = defaultdict(list)      # each person and all the wines they want
        self.wines = defaultdict(list)       # each wine and all the people who want it
        self.people_have = defaultdict(int)  # each person's count of wines they got
        self.wines_sold = 0
        self.outfile = NamedTemporaryFile(mode='w', delete=False)

    def __del__(self):
        remove(self.outfile.name)

    def remove_wine(self, wine):
        """
        Removes the wine from each person's list of desired wines.

        :param wine: The wine to remove
        :return: true if any winelists became empty
        """
        have_empty_lists = False
        for person in self.wines[wine]:
            self.people[person].remove(wine)
            if len(self.people[person]) == 0:
                have_empty_lists = True
        return have_empty_lists

    def remove_person(self, person):
        """
        Removes the person from each wine's list of potential buyers

        Potential change: If, after removing this person, only one other
        person wanted a particular wine, that other person gets to have it.

        :param person: The person to remove
        :return: true if any lists became empty
        """
        have_empty_lists = False
        wines = self.people[person]
        self.people[person] = []
        for wine in wines:
            self.wines[wine].remove(person)
            num_buyers = len(self.wines[wine])
            if num_buyers == 0:
                have_empty_lists = True
#            elif num_buyers == 1:
#                # Only one other person wanted this wine. Let them have it.
#                # Note: This can be recursive.
#                # Try doing the selling outside this for loop.
#                buyer = self.wines[wine][0]
#                if self.people_have[buyer] < max_wines_per_person:
#                    self.sell_wine(wine, buyer)
        return have_empty_lists

    def clear_empty_records(self):
        for person in self.people.keys():
            if len(self.people[person]) == 0:
                del self.people[person]
        for wine in self.wines.keys():
            if len(self.wines[wine]) == 0:
                del self.wines[wine]

    def sell_wine(self, wine, buyer):
        """
        Allocates the wine to the buyer.

        :param wine: The wine to be sold
        :param buyer: The buyer that'll take the wine.
        :return: True if this person cannot buy any more wine.
        """
        self.people_have[buyer] += 1
        self.outfile.write("%s\t%s\n" % (buyer, wine))
        self.remove_wine(wine)
        self.wines[wine] = []
        self.wines_sold += 1
        if self.people_have[buyer] >= max_wines_per_person:
            self.remove_person(buyer)
            return True
        return False

    def sell_wines_with_one_buyer(self):
        """
        If only one person wants this wine, let her have it.
        :return: number of wines sold
        """
        wines_sold = 0
        for wine in self.wines.keys():
            buyers = self.wines[wine]
            if len(buyers) == 1:
                self.sell_wine(wine, buyers[0])
                wines_sold += 1
        return wines_sold

    def sell_wines(self, num_wines):
        """
        If the person only wants this many wines (or fewer), she may have them.

        :param num_wines: The size of the person's wine list to check.
        :return: number of wines sold
        """
        wines_sold = 0
        for buyer in self.people.keys():
            wines = self.people[buyer]
            if len(wines) <= num_wines or num_wines == max_wines_per_person:
                for wine in wines[:max_wines_per_person]:
                    # print "attempting to sell", wine, "to", buyer
                    wines_sold += 1
                    if self.sell_wine(wine, buyer):
                        break
        return wines_sold

    def process(self, lines):
        # Read in the raw data and populate the two dicts.
        for line in lines:
            person, wine = line.strip().split('\t')
            self.people[person].append(wine)
            self.wines[wine].append(person)

        # Determine when we can probably stop working the data
        num_wines_requested = len(self.wines)
        max_wines_people_can_have = max_wines_per_person * len(self.people)
        max_lines = min(num_wines_requested, max_wines_people_can_have)

        # If a person only listed (wines_to_sell_at_once) wines, then we
        # can simply give them those wines.  We start at one, so for each
        # person that only wanted one wine, we let them have it.
        #
        # If nobody listed only one wine, then we increment the variable,
        # and allow everybody who only listed two bottles to have both.
        # (If we let them have just one bottle, then they're left with just
        # the one other bottle in the list. Just give it too, then.)
        wines_to_sell_at_once = 1

        # The algorithm:
        # 1. Always assign the wines that have only one person interested in them.
        # 2. Then see if there is anybody who only wants (wines_to_sell_at_once) wines,
        #    and if there is, give them all their wines.
        while self.wines_sold < max_lines and wines_to_sell_at_once <= max_wines_per_person:
            wines_sold = self.sell_wines_with_one_buyer()
            if wines_sold > 0:
                self.clear_empty_records()
            wines_sold = self.sell_wines(wines_to_sell_at_once)
            if wines_sold > 0:
                self.clear_empty_records()
                wines_to_sell_at_once = 1   # Remove me if using recursive code in Remove_person
            else:
                wines_to_sell_at_once += 1  # Do me always if using recursive code in Remove_person

        self.outfile.close()
        print self.wines_sold
        with open(self.outfile.name, 'r') as f:
            for line in f:
                print line.strip()


def main(fname, debug):
    start_time = time.time()
    wine_allocator = WineAllocator()
    if zipfile.is_zipfile(fname):
        with zipfile.ZipFile(fname, 'r') as zf:
            for zname in zf.namelist():
                with zf.open(zname, 'r') as f:
                    wine_allocator.process(f)
    else:
        with open(fname, 'r') as f:
            wine_allocator.process(f)
    if debug:
        verify_result_file(wine_allocator.outfile.name)
        print "Done.  That took %1.2fs." % (time.time() - start_time)

if __name__ == '__main__':
    usage = "usage: %prog [options] input_file(.txt|.zip)"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--debug", action="store_true", dest="debug")
    parser.set_defaults(debug=False)
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    main(args[0], options.debug)
