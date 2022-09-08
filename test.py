#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Modified by TAs at SNU Software Platform Lab for
# SWPP fall 2022 lecture.

import sys
import re
import os

from functools import wraps

"""Baby Names exercise

Implement the babyname parser class that parses the popular names and their ranks from an html file.

1) First, you need to implement a decorator that checks whether the html file exists or not.
2) Also, the parser should extract tuples of (rank, male-name, female-name) from the html file by using regex.
   When writing regex, it's convenient to include a copy of the target text for reference.
3) Finally, you need to implement `parse` method in `BabynameParser` class that parses the extracted tuples
   with the given lambda and returns a list of processed results.
"""


class BabynameFileNotFoundException(Exception):
    """
    A custom exception for the case that the babyname file does not exist.
    """
    pass


def check_filename_existence(func):
    """
    (1 point)
    A decorator that catches the non-exiting filename argument and raises a custom `BabynameFileNotFoundException`.

    Args:
        func: The function to decorate.
    Raises:
        BabynameFileNotFoundException: if there is no such file matching the first two arguments of the function to decorate.
    """
    # TODO: Implement this decorator
    def inner(*args):
        try:
            return func(*args)
        except FileNotFoundError:
            filename = f"{args[1]}/{args[2]}.html"
            raise BabynameFileNotFoundException(f"No such file: {filename}")
    return inner


class BabynameParser:

    @check_filename_existence
    def __init__(self, dirname, year):
        """
        (3 points)
        Given directory path and year, extracts the name of a file to open the corresponding file
        and a list of the (rank, male-name, female-name) tuples from the file read by using regex.
        [('1', 'Michael', 'Jessica'), ('2', 'Christopher', 'Ashley'), ....]

        Args:
            dirname (str): The name of the directory where baby name html files are stored.
            year (int): The target year to parse.
        """
        # TODO: Open and read html file of the corresponding year, and assign the content to `text`.
        # Also, make the BabynameParser to have the year attribute.
        with open(f"{dirname}/{year}.html", 'r') as f:
            text = f.read()
        self.year = year

        # TODO: Implement the tuple extracting code.
        # `self.rank_to_names_tuples` should be a list of tuples of ("rank", "male name", "female name").
        # You can process the file line-by-line, but regex on the whole text at once is even easier.
        # (If you resolve the previous TODO, the html content is saved in `text`.)
        # You may find the following method useful: `re.findall`.
        # See https://docs.python.org/3/library/re.html#re.findall.
        pattern = r"<td>\d*</td> <td>[a-zA-Z]*</td> <td>[a-zA-Z]*</td>"
        raw_datas = re.findall(pattern, text)
        parsed_datas = [data.split(" ") for data in raw_datas]
        self.rank_to_names_tuples = [(rank.strip(r"</?td>"), male.strip(r"</?td>"), female.strip(r"</?td>")) for rank, male, female in parsed_datas]
        

    def parse(self, parsing_lambda):
        """
        (2 points)
        Collects a list of babynames parsed from the (rank, male-name, female-name) tuples.
        The list must contains all results processed with the given lambda.

        Args:
            parsing_lambda: The parsing lambda.
                            It must process a single (string, string, string) tuple and return something.
        Returns:
            A list of lambda function's output
        """
        # TODO: Implement this method
        return list(map(parsing_lambda, self.rank_to_names_tuples))
class BabyRecord:
    def __init__(self, year, rank, name, gender, rank_change=None):
        """
        Args:
            year (int): The corresponding year of the data.
            rank (int): The rank of the data.
            name (str): The name of the data.
            gender (str): The gender of the data, either 'M' or 'F'.
            rank_change (int | None): The change of the rank compared to the previous year. `None` if no comparison possible.
        """
        self.year = year
        self.rank = rank
        self.name = name
        self.gender = gender
        self.rank_change = rank_change

    def to_csv_record(self):
        """
        (1 point)
        Convert the record into a comma-seperated string line, as format of "year,rank,name,gender(M/F),rank_change".
        The return value is a line of body of CSV file output.
        If rank_change is None, save it as blank ("").

        e.g. 2018,1,Joan,F,-2
        """
        # TODO: Implment this function


    def __repr__(self):
        """
        NOTE: This method is provided for debugging. You don't need to modify this.
        """
        return "<BabyRecord year={} rank={} name={} gender={} rank_change={}>".format(
            self.year,
            self.rank,
            self.name,
            self.gender,
            self.rank_change,
        )

def save(filename, records):
    """
    NOTE: DO NOT change this function.
    This function saves the parsed records in csv format.

    Args:
        filename: The name of the output file.
        records: The list of records.
    """
    with open(filename, "w") as f:
        f.write("year,rank,name,gender,rank_change\n")
        for record in records:
            f.write(record.to_csv_record())
            f.write("\n")
prev_male_ranking = {}
prev_female_ranking = {}
for year in range(2001, 2005):
    records = []
    parser = BabynameParser("babydata", year)
    male_records = parser.parse(lambda x: BabyRecord(year=year, rank=int(x[0]), name=x[1], gender='M')) # Parse the male ranks and store them as a list of `BabyRecord` objects.
    female_records = parser.parse(lambda x: BabyRecord(year=year, rank=int(x[0]), name=x[2], gender='F')) # Parse the female ranks and store it as a list of `BabyRecord` objects.
    for idx in range(1000):
        babyrecord = male_records[idx]
        male_name = babyrecord.name
        male_rank = babyrecord.rank
        prev_year = prev_male_ranking.get(year-1)
        if prev_year:
            prev_rank = prev_year.get(male_name)
            babyrecord.rank_change = male_rank - prev_rank if prev_rank else None
        if prev_male_ranking.get(year):
            prev_male_ranking[year][male_name] = male_rank
        else: 
            prev_male_ranking[year] = {
                male_name: male_rank
            }
            
        babyrecord = female_records[idx]
        female_name = babyrecord.name
        female_rank = babyrecord.rank
        prev_year = prev_female_ranking.get(year-1)
        if prev_year:
            prev_rank = prev_year.get(female_name)
            babyrecord.rank_change = female_rank - prev_rank if prev_rank else None
        if prev_female_ranking.get(year):
            prev_female_ranking[year][female_name] = female_rank
        else: 
            prev_female_ranking[year] = {
                female_name: female_rank
            }
    records.extend([*male_records, *female_records])
    print(records)