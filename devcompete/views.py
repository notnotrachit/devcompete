from django.shortcuts import render


from django.views.generic import View

class MyView(View):
    template_name = "home.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
