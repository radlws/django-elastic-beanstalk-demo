from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home/landing.html'

home = HomeView.as_view()


#################### ERROR VIEWS ####################

# class PermissionDeniedView(TemplateView):
#     template_name = '403.html'
# 
# permission_denied_view = PermissionDeniedView.as_view()
# 
# 
# class ServerErrorView(TemplateView):
#     template_name = '500.html'
# 
# server_error_view = ServerErrorView.as_view()
