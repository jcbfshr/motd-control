import sys
from jokeapi import Jokes

# fetch api content
def fetch():
    j = Jokes()
    return j.get_joke(blacklist=["nsfw", "religious", "political", "racist", "sexist"],type="single",category=["programming","miscellaneous"])

# print joke
if __name__ == "__main__":
    print(f"{fetch()['joke']}")