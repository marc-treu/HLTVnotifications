import json

from EmailNotifier import send_email
from IO import read, write
from WebScrapper import get_next_matches


"""
Main script


When is call
"""


def is_different(new_list, old_list):
    new_list_s = sorted(new_list, key=lambda k: k['time'])
    old_list_s = sorted(old_list, key=lambda k: k['time'])
    return new_list_s != old_list_s


def main():

    with open('config.json') as json_file:
        config = json.load(json_file)

    new_info_matchs = get_next_matches(config['team'], config['number'])  # get a dictionary that containt infos of next matchs

    if not new_info_matchs:  # If there is no following match
        exit()

    previous_info_matchs = read()  # Read previous info we got

    if is_different(previous_info_matchs, new_info_matchs):  # if there is any change in the shedule
        send_email(config['mail'], new_info_matchs)  # Send well formated email
        write(new_info_matchs)  # write down new info


if __name__ == '__main__':
    main()
