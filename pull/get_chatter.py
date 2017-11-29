# demonstration of using the BeatBox library to call the sforce API

import sys
import re
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
		qr = svc.query("select Body from CollaborationGroupFeed where ParentId=\'0F91I000000MdhESAS\'")
		return qr

	def dumpQueryResult(self, qr):
		print "query size = " + str(qr[sf.size])

		for rec in qr[sf.records:]:
			print str(rec[0]) + " : " + str(rec[1]) + " : " + str(rec[2])

		if (str(qr[sf.done]) == 'false'):
			print "\nqueryMore"
			qr = svc.queryMore(str(qr[sf.queryLocator]))
			for rec in qr[sf.records:]:
				print str(rec[0]) + " : " + str(rec[1]) + " : " + str(rec[2])

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
