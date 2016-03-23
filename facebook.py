import json
import requests
import csv

class GraphAPI(object):
	prefix_url = 'https://graph.facebook.com/v2.5/'
	
	def __init__(self, access_token):
		self.access_token = access_token

	def get_request(self, path, params={}):
		params['access_token'] = self.access_token
		url = self.prefix_url + path
		r = requests.get(url, params=params)
		return r.json()
	def get_all_likes(self, board):
		r = self.get_request(board)
		likes = [info['name'] for info in r['music']['data']]
		#print likes
		if r['music']['paging']['next']:
			r = requests.get(r['music']['paging']['next'])
			r = r.json()
			currentlikes =  [song['name'] for song in r['data']]
			likes += currentlikes
			while r['paging']['next']:
				r = requests.get(r['paging']['next'])
				r = r.json()
				currentlikes =  [song['name'] for song in r['data']]
				likes += currentlikes
				if 'next' in r['paging']:
					nextpage = r['paging']['next']
				else:
					break

		return likes

def main():
	obj = GraphAPI('CAACEdEose0cBANUDtsL6JOFQ58xDcrWz2LTkCpQ2TLbNh069XBwuzD1ZBujmYbnmtLMfJN7byvzl9NZBkGoI37G8B0aZAQ3qnL6GsXya08iuj44kmVuao4WYOJnU0pYf0BPVgxZBMiERd7c7uKI3P6Qzecg5rbYPlt3VGfxUiZAiEZBYvaZAYZCiQR55YaLF6oVPRzHqDATSJ5mRr4P5YrZAq')
	#r = obj.get_request('me?fields=id,name,music')
	
	likes = obj.get_all_likes('me?fields=id,name,music')
	#print likes
	print len(likes)
	with open('elbertlikes.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["artists"])
		for i in range(len(likes)):
			like = likes[i].encode("utf-8")
			writer.writerow([like])


if __name__ == '__main__':
    main()