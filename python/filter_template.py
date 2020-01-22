from django import template

register = template.Library()

@register.filter
def parse_url(urls):
    parsed_urls=[]
    rs = (grequests.get(url['location']) for url in urls)
    requests = grequests.map(rs)
    print(requests)
