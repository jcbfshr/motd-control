import urllib.request, json, sys, api_handler
from datetime import datetime
from dateutil import parser

# fetch api content
def fetch(search_terms=[]):
    api_info = api_handler.get_api_info("guardian")
    base_url = f"{api_info['base_url']}{str(api_info['api_key'])}"
    if len(search_terms) > 1:
        base_url = f"{base_url}&section={search_terms[0]}{'%20AND%20'.join(search_terms[1:])}"
    elif len(search_terms) == 1:
        base_url = f"{base_url}&q={search_terms[0]}"
    return api_handler.fetch(base_url)

# format headlines into list with timestamps and category
if __name__ == "__main__":
    try:
        articles = fetch()["response"]["results"]
    except KeyError as e:
        print(f"Invalid json: {str(e)} probably not found")
        sys.exit(1)
    except TypeError:
        print(f"Invalid json: probably blank field")
        sys.exit(1)

    for article in articles:
        print(f"[{parser.isoparse(article['webPublicationDate']).strftime('%H:%M:%S %a %d %b %Y')}] {article['sectionName']}: {article['webTitle']}")