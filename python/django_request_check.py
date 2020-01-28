  def get(self, request):
        return_path = request.GET.get("state")
        from django.utils.html import escape
        return HttpResponse(escape(repr(request)))
        context = {}
        context['body'] = request.body
        context['cookies'] = request.COOKIES
        context['get'] = request.GET
        context['header'] = content_type
        return HttpResponse(escape(repr(context)))
