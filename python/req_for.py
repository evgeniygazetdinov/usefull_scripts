import requests



def main(link):
    response = requests.get()
    if response.status_code != 200:
        print("Something wrong, status code, "response.status_code)
        raise Exception("error!"*5)
    print("Status ",response.status_code)
    print("Content ",response['content type'])
    data = response.json()
    print('response in json',data)


if __name__ == "__main__":
    main()
