"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
from xblockutils.studio_editable import StudioEditableXBlockMixin


loader = ResourceLoader(__name__)

_ = lambda text: text

class HeraHtmlContentXBlock(StudioEditableXBlockMixin, XBlock):

    display_name = String(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        scope=Scope.settings,
        default=_("Text")
    )

    image_url = String(
        display_name="URL to image",
        help="Enter absolute path to the image",
        scope=Scope.settings,
        default=''
        )

    iframe_url = String(
        display_name="URL to image",
        help="Enter absolute path to the image",
        scope=Scope.settings,
        default=''
    )

    data = String(
        help=_("Html contents to display for this module"),
        default=u"Test text",
        scope=Scope.content
    )


    def resource_string(self, path):
        """
        Handy helper for getting resources from our kit.
        """
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")


    def student_view(self, context=None):
        """
        The primary view of the EasyXBlock, shown to students
        when viewing courses.
        """
        context = {
            'display_name': self.display_name,
            'image_url': self.image_url,
            'iframe_url': self.iframe_url,
            'data': self.data
        }
        html = loader.render_django_template(
            'templates/htmlXBlock_student.html',
            context=context
        )
        frag = Fragment(html)
        frag.add_css_url(self.runtime.local_resource_url(self, 'public/bootstrap-4.3.1/css/bootstrap.min.css'))
        return frag

    def studio_view(self, context=None):
        """  Returns studio view fragment """
        context = {
            'display_name': self.display_name,
            'image_url': self.image_url,
            'iframe_url': self.iframe_url,
            'data': self.data
        }

        html = loader.render_django_template("templates/htmlXBlock_studio.html", context=context)
        frag = Fragment(html.format(self=self))
        js_str = self.resource_string("static/js/src/hera_html_content.js")
        frag.add_javascript(js_str)
        frag.initialize_js('HeraHtmlContentXBlock')

        return frag


    @XBlock.json_handler
    def save_hera_html_content(self, data, suffix=''):
        self.display_name = data["display-name"]
        self.image_url = data["image-url"]
        self.iframe_url = data["iframe-url"]
        self.data = data["html-content"]
        return {"result": "success"}
