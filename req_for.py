import requests



def main(link):
    response = requests.get()
    print("Status ",response.status_code)
    print("Content ",response['content type'])
    data = response.json()
    print('response in json',data)


if __name__ == "__main__":
    main()
