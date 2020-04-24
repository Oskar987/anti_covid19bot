import os
import requests
import codecs
import ciso8601

from jinja2 import Template
from cachetools import cached, TTLCache
from common.containers import DBContext


class StatisticsService:
    """This class provide information about statistics"""

    # cache time 3 hours
    cache = TTLCache(maxsize=100, ttl=10800)

    def __init__(self):
        try:
            self.covid_api_token = os.getenv('COVID_STAT_API_TOKEN')
            self.db_context = DBContext.mongo_db_context()
        except Exception as e:
            raise e

    # method for getting statistics from API
    def __get_statistics_by_country_from_api(self, country_name):
        url = "https://covid-193.p.rapidapi.com/statistics"
        query_string = {'country': country_name}
        headers = {
            'x-rapidapi-host': "covid-193.p.rapidapi.com",
            'x-rapidapi-key': self.covid_api_token
        }
        response = requests.request("GET", url, headers=headers, params=query_string)
        return response.json()

    # method for rendering statistics as html
    @cached(cache)
    def __get_statistics_by_country_as_html(self, country_name):
        try:
            statistics_json = self.__get_statistics_by_country_from_api(country_name)
            if len(statistics_json['response']) == 0:
                with codecs.open('templates/idunnocommand.html', 'r', encoding='UTF-8') as file:
                    template = Template(file.read())
                    return template.render(text_command=country_name)
            else:
                with codecs.open('templates/country_statistics.html', 'r', encoding='UTF-8') as file:
                    template = Template(file.read())
                    return template.render(date=ciso8601.parse_datetime(statistics_json['response'][0]['time']).date(),
                                           country=statistics_json['response'][0]['country'].upper(),
                                           new_cases=statistics_json['response'][0]['cases']['new'],
                                           active_cases=statistics_json['response'][0]['cases']['active'],
                                           critical_cases=statistics_json['response'][0]['cases']['critical'],
                                           recovered_cases=statistics_json['response'][0]['cases']['recovered'],
                                           total_cases=statistics_json['response'][0]['cases']['total'],
                                           new_deaths=statistics_json['response'][0]['deaths']['new'],
                                           total_deaths=statistics_json['response'][0]['deaths']['total'])
        except Exception as e:
            raise e

    # method for getting statistics by country_name
    def get_statistics_by_country_name(self, country_name, user_name):
        self.db_context.save_query(country_name, user_name)
        return self.__get_statistics_by_country_as_html(country_name)

    # method for getting statistics of users and queries
    def get_statistics_of_users_queries(self):
        query_statistics = self.db_context.get_users_queries()
        with codecs.open('templates/query_statistics.html', 'r', encoding='UTF-8') as file:
            template = Template(file.read())
            return template.render(queries=query_statistics['queries'], users=query_statistics['users'])
