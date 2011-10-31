from django.conf import settings
from django.utils.http import urlquote


class ChangeContentType(object):

    STATIC_CONTENT = [settings.MEDIA_URL,
                      settings.STATIC_URL,
                      settings.ADMIN_MEDIA_PREFIX,
                      ]
    FILE_ASSOCIATION = {'htc': 'text/x-component'}

    def is_supported(self, path):
        for p in self.STATIC_CONTENT:
            if path.startswith(p):
                return True

    def process_response(self, request, response):
        path = urlquote(request.get_full_path())
        try:
            extension = path.split('.')[-1]
        except IndexError:
            extension = None
        if self.is_supported(path) and extension in self.FILE_ASSOCIATION:
            response['Content-Type'] = self.FILE_ASSOCIATION[extension]
        return response


class StagingMarquee(object):
    def process_response(self, request, response):
        content = response.content
        index = content.upper().find('</BODY>')
        if index == -1:
            return response
        marquee = "<div style='color:red;position:absolute;top:0;font-weight:bold;font-size:20px;'>STAGING</div>"
        response.content = content[:index] + marquee + content[index:]
        return response
