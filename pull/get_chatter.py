# demonstration of using the BeatBox library to call the sforce API

import sys
import re
from beatbox._beatbox import (Client, _tPartnerNS)
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime, timedelta
env = Environment(
    loader=PackageLoader('pull', 'templates'),
    autoescape=select_autoescape(['html', 'xml', 'json'])
)
sf = _tPartnerNS
svc = Client()
gzipRequest = False

reload(sys)
sys.setdefaultencoding('utf8')
class ChatterFetcher:
    def __init__(self):
        self.server_url = 'https://na73.salesforce.com/services/Soap/u/40.0'
        self.username = 'slatter@ofekhackathon.org'
        self.password = 'test1234'

    def login(self):
        svc.serverUrl = self.server_url
        login_result = svc.login(self.username, self.password)
        print "sid = " + str(login_result[sf.sessionId])
        print "welcome " + str(login_result[sf.userInfo][sf.userFullName])

    def getServerTimestamp(self):
        print "\ngetServerTimestamp " + svc.getServerTimestamp()

    def queryChatter(self):
        print "\nqueryChatter"
        template = env.get_template("attachment.json")
        commentTemplate = env.get_template("comment.json")

        postsqr = svc.query("select CreatedById, Body, CreatedDate, Id "
                            "from CollaborationGroupFeed where ParentId=\'0F91I000000Men9SAC\'"
                            "AND Type = 'TextPost' order by LastModifiedDate")
        posts = []
        for rec in postsqr[sf.records:]:
            posterqr = svc.query("select name from user where id = '" + str(rec[2]) + "'")
            msg = re.sub('<[^<]+>', "", "".join(str(rec[3]).split("\n")))
            ts = (datetime.strptime(str(rec[4])[:-5], '%Y-%m-%dT%H:%M:%S') - timedelta(hours=10)).strftime('%s')

            if msg:
                posts.append(template.render(name=str(posterqr[sf.records:][0]), body=msg, ts=ts))
                commentqr = svc.query("select CreatedById, commentBody from FeedComment where FeedItemid = '" + str(rec[5]) + "'")
                for commrec in commentqr[sf.records:]:
                    commenterqr = svc.query("select name from user where id = '" + str(commrec[2]) + "'")
                    comment = re.sub('<[^<]+>', "", "".join(str(commrec[3]).split("\n")))
                    if  comment:
                        posts.append(commentTemplate.render(name=str(commenterqr[sf.records:][0]), body=comment, ts=ts))

        return posts

    def parse_query_result(self, qr):
        posts = []
        for rec in qr[sf.records:]:
            posts.append(re.sub('<[^<]+>', "", str(rec[2])))

        if str(qr[sf.done]) == 'false':
            qr = svc.queryMore(str(qr[sf.queryLocator]))
            for rec in qr[sf.records:]:
                posts.append(str(rec[2]))

        return posts


if __name__ == "__main__":

    if len(sys.argv) != 1:
        print 'usage is %s .py' % sys.argv[0]
    else:
        fetcher = ChatterFetcher()
        fetcher.login()
        qr = fetcher.queryChatter()
        fetcher.dumpQueryResult(qr)
