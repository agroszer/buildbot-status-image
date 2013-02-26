# this is a snippet ready to be pasted into master.cfg
# then you can get the image by:
# http://localhost:8010/buildstatusimage?builder=runtests&number=-1

import os
from buildbot.status import html
try:
    # buildbot 0.8.7p1
    from buildbot.status.results import SUCCESS, WARNINGS, FAILURE, SKIPPED, EXCEPTION
    from buildbot.status.results import Results
except ImportError:
    # buildbot 0.8.0
    from buildbot.status.builder import SUCCESS, WARNINGS, FAILURE, EXCEPTION, RETRY
    from buildbot.status.builder import Results
from buildbot.status.web.base import HtmlResource

class BuildStatusImageResource(HtmlResource):
    contentType = "image/png"

    def __init__(self, categories=None):
        HtmlResource.__init__(self)

    def content(self, request, ctx):
        """Display a build status image like Travis does."""

        status = self.getStatus(request)
        request.setHeader('Cache-Control', 'no-cache')

        # Get the parameters.
        name = request.args.get("builder", [None])[0]
        number = request.args.get("number", [None])[0]
        if not name or not number:
            return "builder and number parameter missing"
        number = int(number)

        # Check if the builder in parameter exists.
        try:
            builder = status.getBuilder(name)
        except:
            return "unknown builder"

        # Check if the build in parameter exists.
        build = builder.getBuild(int(number))
        if not build:
            return "unknown build %s" % number

        #SUCCESS, WARNINGS, FAILURE, SKIPPED or EXCEPTION
        res = build.getResults()
        resname = Results[res]

        img = 'status_image_%s.png' % resname
        here = os.path.dirname(__file__)
        imgfile = os.path.join(here, img)

        imgcontent = open(imgfile, 'rb').read()

        return imgcontent

class WebStatus(html.WebStatus):
    def setupUsualPages(self, numbuilds, num_events, num_events_max):
        html.WebStatus.setupUsualPages(self, numbuilds, num_events, num_events_max)
        self.putChild("buildstatusimage", BuildStatusImageResource())


# and use the WebStatus defined above instead of buildbot's
#c['status'].append(WebStatus(http_port=8010))
