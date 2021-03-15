from bs4 import BeautifulSoup

import requests


def get_html(url):
    """Get the html code a the page given by the url in a BeautifulSoup Object

    :param url: str which is a valid url
    :return: The html code of the page url
    """
    html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 '
                                                    'Firefox/10.0 '})  # Need a header to avoid response 503
    return BeautifulSoup(html.text, features="html.parser")


def get_info_matches(matches_url):
    """

    :param matches_url: A list
    :return: A list of dictionary with essential info
    (ex : [{'team1': ['Vitality'], 'team2': ['FaZe'], 'time': datetime.datetime(2021, ...), 'url': 'https...'}, {...}])
    """
    info_matches = []
    for match_url in matches_url:
        match_html = get_html(match_url)
        teams = match_html.findAll('div', {'class': 'teamName'})  # Find teams name
        time = int(match_html.find('div', {'class': 'time'})['data-unix'][:-3])  # Find time

        info_matches.append({'team1': teams[0].contents[0], 'team2': teams[1].contents[0], 'time': time, 'url': match_url})

    return info_matches


def get_next_matches(team_name, team_number):
    """

    :param team_name:
    :param team_number:
    :return:
    """
    team_url = f'https://www.hltv.org/team/{team_number}/{team_name}#tab-matchesBox'  # Url of the team we want matches info

    html_page = get_html(team_url)

    next_matches_url = ["https://www.hltv.org" + match['href'] for match in html_page.findAll('a', {'class': 'matchpage-button'})]

    return get_info_matches(next_matches_url)


if __name__ == '__main__':
    url1 = 'https://www.hltv.org/team/9565/vitality#tab-matchesBox'
    url2 = 'https://www.hltv.org/team/10503/og#tab-matchesBox'
    soup = get_html(url1)
    next_matches_url = [match['href'] for match in soup.findAll('a', {'class': 'matchpage-button'})]
    print(next_matches_url)
