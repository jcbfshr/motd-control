import sys, api_handler

# fetch api content
def fetch():
    return api_handler.fetch(api_handler.get_api_info("useless_facts")["base_url"])

# print fact
if __name__ == "__main__":
    try:
        fact = fetch()
    except KeyError as e:
        print(f"Invalid json: {str(e)} probably not found")
        sys.exit(1)
    except TypeError:
        print(f"Invalid json: probably blank field")
        sys.exit(1)

    print(f"{fact['text']}")