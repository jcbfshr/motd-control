import urllib.request, json, sys
from datetime import datetime
from dateutil import parser

def get_api_info(path="./api_keys.json"):
    try:
        with open(str(path)) as file:
            return json.loads(file.read())["api_keys"]["guardian"],path
    except FileNotFoundError:
        print(f"Can't find {str(path)}")
        sys.exit(1)
    except KeyError as e:
        print(f"Invalid {str(path)}: {str(e)} probably not found")
        sys.exit(1)

def validate(prompt,acceptable=["y","n"],ending=":"):
    response = ""
    while response not in acceptable:
        response = str(input(f"{prompt}{ending} [y/N] "))[0].lower()
    return response

def fetch(api_key,search_terms=[]):
    base_url = "https://content.guardianapis.com/search?api-key="
    if api_key != "":
        base_url = f"{base_url}{str(api_key)}"
        
        if len(search_terms) > 1:
            base_url = f"{base_url}&section={search_terms[0]}{'%20AND%20'.join(search_terms[1:])}"
        elif len(search_terms) == 1:
            base_url = f"{base_url}&q={search_terms[0]}"
        try:
            with urllib.request.urlopen(base_url) as url:
                data = json.loads(url.read().decode())
                return data
        except urllib.error.HTTPError as e:
            print(f"Received HTTP error: {str(e)}")
            if str(e) == "HTTP Error 403: Forbidden":
                print("Probably bad API key")
            sys.exit(1)
    else:
        return "Please add your api key to main.py"

if __name__ == "__main__":
    api_info,path = get_api_info()
    try:
        articles = fetch(api_info["api_key"])["response"]["results"]
    except KeyError as e:
        print(f"Invalid {str(path)}: {str(e)} probably not found")
        sys.exit(1)
    except TypeError:
        print(f"Invalid {str(path)}: probably blank field")
        sys.exit(1)

    for article in articles:
        print(f"[{parser.isoparse(article['webPublicationDate']).strftime('%H:%M:%S %a %d %b %Y')}] {article['sectionName']}: {article['webTitle']}")