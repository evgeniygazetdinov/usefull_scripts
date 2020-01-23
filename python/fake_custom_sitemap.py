class PressDateSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def return_year_and_month_object(self,date):
        values = date.timetuple()
        year = values.tm_year
        month = values.tm_mon
        if int(month)<10:
            month = "0"+str(month)
        return year,month

    def return_unique_dates(self):
        posible_dates = []
        unique_dates = []
        for obj in Press.objects.all():
            year,mon = self.return_year_and_month_object(obj.date)
            posible_dates.append([year,mon])
        for unique in posible_dates:
            if unique not in unique_dates:
                unique_dates.append(unique)
        return unique_dates

    def create_urls_from_dates(self):
        dates = list(self.return_unique_dates())
        urls = []
        for date in dates:
            urls.append('{}/{}/'.format(date[0],date[1]))
        return urls

    def items(self):
        return self.create_urls_from_dates()

    def location(self, item):
        return '/press/'+item
