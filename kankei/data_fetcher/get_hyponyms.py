#f014e479-08cc-4f52-bac1-b233b78a75b5

#curl -X GET --header 'Accept: application/json'
# 'https://api.apitore.com/api/42/wordnet-simple/hypernym?
# access_token=f014e479-08cc-4f52-bac1-b233b78a75b5
#
# word=%E3%82%AA%E3%82%AA%E3%82%AB%E3%83%9F
# pos=n%2Cv%2Ca%2Cr'
from data_fetcher import web_api_fetch


@web_api_fetch
def get_hyponym(request_get,fetch_helper):

    request_get()

