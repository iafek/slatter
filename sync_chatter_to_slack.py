from pull.get_chatter import ChatterFetcher
from push.post_slack import SlackPoster
import sys

if __name__ == "__main__":
	if len(sys.argv) != 1:
		print 'usage is %s .py' % sys.argv[0]
		exit(-1)

	fetcher = ChatterFetcher()
	fetcher.login()
	posts = fetcher.queryChatter()
	# posts = fetcher.parse_query_result(qr)

	poster = SlackPoster()
	for message in posts:
		if message:
			poster.post(message)

