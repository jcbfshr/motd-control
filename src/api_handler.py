import json, sys, urllib.request

# load api settings for provider from path
def get_api_info(provider,path="./src/api_keys.json"):
    try:
        with open(str(path),"r") as file:
            return json.loads(file.read())["api_keys"][str(provider)]
    except FileNotFoundError:
        print(f"Can't find {str(path)}")
        sys.exit(1)
    except KeyError as e:
        print(f"Invalid {str(path)}: {str(e)} probably not found")
        sys.exit(1)

# scrape url for json
def fetch(url):
    try:
        with urllib.request.urlopen(url) as fetched:
            return json.loads(fetched.read().decode())
    except urllib.error.HTTPError as e:
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/83.0.4103.61 Chrome/83.0.4103.61 Safari/537.36")
            with urllib.request.urlopen(url) as fetched:
                return json.loads(fetched.read().decode())
        except:
            print(f"Received HTTP error: {str(e)}")
            if str(e) == "HTTP Error 403: Forbidden":
                print("Invalid url: probably bad API key")
            sys.exit(1)