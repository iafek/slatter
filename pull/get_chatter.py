# demonstration of using the BeatBox library to call the sforce API

import sys

from beatbox._beatbox import (Client, _tPartnerNS)

sf = _tPartnerNS
svc = Client()
gzipRequest = False


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
		postsqr = svc.query("select CreatedById, Body from CollaborationGroupFeed where ParentId=\'0F91I000000MdhESAS\'")
                posts = []
                for rec in postsqr[sf.records:]:
                    posterqr = svc.query("select name from user where id = '" + str(rec[2]) + "'")
                    posts.append("Posted by : " + str(posterqr[sf.records:][0]) + " " + str(rec[3]))       
                    print ("Posted by : " + str(posterqr[sf.records:][0]) + " " + str(rec[3]))
		return posts

"""
	def dumpQueryResult(self, qr):
		print "query size = " + str(qr[sf.size])

		for rec in qr[sf.records:]:
			print str(rec[0]) + " : " + str(rec[1]) + " : " + str(rec[2])

		if (str(qr[sf.done]) == 'false'):
			print "\nqueryMore"
			qr = svc.queryMore(str(qr[sf.queryLocator]))
			for rec in qr[sf.records:]:
				print str(rec[0]) + " : " + str(rec[1]) + " : " + str(rec[2])
"""


if __name__ == "__main__":

	if len(sys.argv) != 1:
		print 'usage is %s .py' % sys.argv[0]
	else:
		fetcher = ChatterFetcher()
		fetcher.login()
		qr = fetcher.queryChatter()
		fetcher.dumpQueryResult(qr)
