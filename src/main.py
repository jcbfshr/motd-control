import headlines,joke,fact,sys,time
from datetime import datetime
from dateutil import parser

# print content to specified path
def print_file(path,content):
    try:
        with open(str(path),"w") as file:
            file.write(content)
    except FileNotFoundError:
        print("Invalid save path in ./src/main.py")
        sys.exit(1)

# get headers and print underneath relevant api content
def run(headers=["main","fact","joke","headlines"]):
    output = "\n\n\n"

    for header in headers:
        try:
            with open(f"./headers/{str(header)}.txt","r") as file:
                output += file.read()
        except FileNotFoundError:
            print("Invalid headers in ./src/main.py")
            sys.exit(1)
        if header != "main":
            if header == "fact":
                output += "\n"
                output += fact.fetch()["text"]
            elif header == "joke":
                output += "\n"
                output += joke.fetch()["joke"]
            elif header == "headlines":
                articles = headlines.fetch()["response"]["results"]
                for article in articles:
                    output += f"\n[{parser.isoparse(article['webPublicationDate']).strftime('%H:%M:%S %a %d %b %Y')}] {article['sectionName']}: {article['webTitle']}"
        output += "\n\n"
    return output

# refresh api content every 5 minutes
if __name__ == "__main__":
    while True:
        print_file("./motd.txt",run())
        time.sleep(300)