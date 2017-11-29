# demonstration of using the BeatBox library to call the sforce API

import sys

from pull import beatbox

sf = beatbox._tPartnerNS
svc = beatbox.Client()
beatbox.gzipRequest=False


class ChatterFetcher:
	def __init__(self):
		self.servel_url = 'https://na73.salesforce.com/services/Soap/u/40.0'
		self.username = 'slatter@ofekhackathon.org'
		self.password = 'test1234'

	def login(self):
		login_result = svc.login(self.username, self.password, serverUrl=self.server_url)
		print "sid = " + str(login_result[sf.sessionId])
		print "welcome " + str(login_result[sf.userInfo][sf.userFullName])
	
	def getServerTimestamp(self):
		print "\ngetServerTimestamp " + svc.getServerTimestamp()
			
	def dumpQueryResult(self, qr):
		print "query size = " + str(qr[sf.size])
	
		for rec in qr[sf.records:]:
			print str(rec[0]) + " : " + str(rec[2]) + " : " + str(rec[3])
	
		if (str(qr[sf.done]) == 'false'):
			print "\nqueryMore"
			qr = svc.queryMore(str(qr[sf.queryLocator]))
			for rec in qr[sf.records:]:
				print str(rec[0]) + " : " + str(rec[2]) + " : " + str(rec[3])


if __name__ == "__main__":

	if len(sys.argv) != 1:
		print 'usage is %s .py' % sys.argv[0]
	else:
		fetcher = ChatterFetcher()
		fetcher.login()
