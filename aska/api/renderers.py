from rest_framework.renderers import BrowsableAPIRenderer


class CustomBrowsableAPIRender(BrowsableAPIRenderer):
    template = "api/api.html"
