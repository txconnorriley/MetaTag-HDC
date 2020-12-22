import csv
import datetime
import itertools
import os
import sys
import time


def csv_read(csv_name):
    # kb_article[0], kb_meta[3]
    # Open .csv file
    with open(csv_name, 'rt', encoding='ISO-8859-1') as current:
        reader = csv.reader(current, delimiter=',')

        # Instantiate the Knowledge Base dictionary
        kb_dict = {}

        # Read CSV file row by row
        for row in reader:
            # Article number is found in the first column
            # Meta-tags for the article are found in the fourth column
            kb_article = row[0]
            kb_meta = row[3]

            # Assign the key, article number,
            # to the value, meta-tag string,
            # in the Knowledge Base dictionary
            kb_dict[kb_article] = kb_meta

        # Return the Knowledge Base dictionary with
        # meta-tag list in string form
        return kb_dict


def tag_csv_write(tag_list):
    # Make and open .csv with all KB articles and top 3 matches
    with open("MetaTagList.csv", mode="w") as output:
        match_writer = csv.writer(
            output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write the top row with titles for each column
        match_writer.writerow(
            ["Meta Tag", "Frequency", "KB Matches"])

        # For each KB article, write itself and the top 3 matches
        for i in tag_list:
            # Assign tag and frequency to temporary list
            temp_list = [i[0], i[1][0]]

            # For each KB Matched Article, append to the temp list
            for j in i[1][1]:
                temp_list.append(j)

            # Write full list to the row
            match_writer.writerow(temp_list)

        output.close()


def removed_csv_write(article_list):
    # Make and open .csv with all KB articles that have no tags
    with open("ManualReviewList.csv", mode="w") as output:
        match_writer = csv.writer(
            output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write the top row
        match_writer.writerow(["KB Article"])

        # Transform flat list to a matrix
        rows = zip(article_list)

        # Print each row of the matrix to the CSV
        for kb_article in rows:
            match_writer.writerow(kb_article)

        output.close()


def init_kb_dict(csv_file):
    # Instantiate Knowledge Base dictionary
    kb_dict = csv_read(csv_file)

    # Return the Knowledge Base dictionary with
    # meta-tag list in string form for all CSV files
    return kb_dict


def proc_kb_dict():
    # Get inital dictionary of article/tag pairs
    temp_kb_dict = init_kb_dict('kb_knowledge.csv')

    # Initialize new dictionary
    kb_dict = {}

    # Iterate through dictionary
    for key in temp_kb_dict.keys():
        # Get meta-tag string
        value = temp_kb_dict[key]

        # Split the string into a list of strings
        meta_list = value.split(',')

        # Remove any leading whitespace
        new_meta_list = []

        for tag in meta_list:
            new_meta_list.append(tag.lstrip())

        # Assign the old key with the new list
        kb_dict[key] = new_meta_list

    return remove_kcs_tags(kb_dict)


def remove_kcs_tags(kb_dict):
    # Initialize list of removed Knowledge Base keys
    removed_kbs = []

    # Iterate through Knowledge Base dictionary using keys
    for key in list(kb_dict):
        # Get the tag_list tied to each key
        tag_list = kb_dict[key]

        # If 'KCS' is not found, move on
        if 'KCS' not in tag_list:
            pass
        # Otherwise remove 'KCS' from the list
        else:
            tag_list.remove('KCS')

        # If after removal the list is empty
        # Remove key from dictionary
        if len(tag_list) == 0:
            removed_kbs.append(key)
            del kb_dict[key]

    removed_csv_write(removed_kbs)

    return kb_dict


def check_keys_matches(kb_dict):
    for key in kb_dict.keys():
        tag_list = kb_dict[key]
        print('\n' + key + ': ')

        for tag in tag_list:
            for comparison_key in kb_dict.keys():
                if key != comparison_key:
                    comparison_tag_list = kb_dict[comparison_key]

                    for comparison_tag in comparison_tag_list:
                        if tag == comparison_tag and tag != '':
                            print('Match in ' + comparison_key + '! ' + tag)


def check_tags_matches(kb_dict):
    # Instantiate a dictionary and list of all tags
    full_tag_dict = {}
    full_tag_list = []

    # Iterate through dictionary by key
    for key in kb_dict.keys():
        tag_list = kb_dict[key]

        # Iterate through each tag for each key
        for tag in tag_list:
            # If tag is not in list and is not null, add to list and add to
            # dictionary with value 1 with key in list
            if tag != '' and tag not in full_tag_list:
                full_tag_list.append(tag)
                full_tag_dict[tag] = [1, [key]]

            # If tag is already in full list, increment and
            # add key to list
            elif tag in full_tag_list:
                full_tag_dict[tag][0] = full_tag_dict[tag][0] + 1
                full_tag_dict[tag][1].append(key)

    return full_tag_dict


def sort_tags_by_val(tag_dict):
    # Parse to tuple and sort by value
    sorted_tag_matches = sorted(
        tag_matches_dict.items(), key=lambda kv: kv[1])

    # Parse to list with highest value first
    tag_list = list(sorted_tag_matches[::-1])

    # Create list for all new tags
    new_tag_list = []

    # If tag has more than 1 match, add it to new list
    for tag in tag_list:
        if tag[1][0] > 1:
            new_tag_list.append(tag)

    return new_tag_list


kb_dict = proc_kb_dict()
tag_matches_dict = check_tags_matches(kb_dict)
matched_list = sort_tags_by_val(tag_matches_dict)
tag_csv_write(matched_list)
