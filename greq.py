import grequests

class Check_url:
    def __init__(self,urls):
        self.urls = urls

    def exception(self, request, exception):
        print("Problem: {}: {}".format(request.url, exception))

    def async(self):
        results = grequests.get(self.urls)
        #exception_handler=self.exception, size=5)
        dir(results)
        #return [results.status,results.url]
