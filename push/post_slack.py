
import json
import requests


class SlackPoster(object):

	def __init__(self):
		self.webhook_url = 'https://hooks.slack.com/services/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'

	def post(self, message):

		slack_data = {'text': message}

		response = requests.post(
			self.webhook_url, data=json.dumps(slack_data),
			headers={'Content-Type': 'application/json'}
		)

		if response.status_code != 200:
			raise ValueError(
				'Request to slack returned an error %s, the response is:\n%s'
				% (response.status_code, response.text)
			)


if __name__ == "__main__":
	poster = SlackPoster()
	poster.post('testing from python')
