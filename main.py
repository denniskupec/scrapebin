
import requests, json, time, sys, os

result_limit = 100
sleep_time = 90 #interval in seconds to sleep after each recent pastes batch
minimum_length = 50 #ignore pastes shorter than this
save_path = os.getcwd() + '/pastes/' #where keyword matching pastes get saved

keywords = [line.rstrip('\n') for line in open(os.getcwd() + '/keywords.txt', 'r').readlines()]


def http_get(url, params={}, tries=0):
	if tries > 10:
		sys.exit('Exceeded 10 fetch retries. Are you banned?')

	res = requests.get(url, params, timeout=3.3)

	if res.status_code == requests.codes.ok:
		return res

	time.sleep(1)
	return http_get(url, params, tries+1)


def save_paste(path, data, separator=None):
	if(separator is None):
		separator = '\n\n---------- PASTE START ----------\n\n'

	with open(path, 'w', encoding='utf-8') as file:
		file.write(json.dumps(paste, sort_keys=True, indent=3, separators=(',', ': ')) + separator)
		file.write(data)

	return file.closed


if __name__ == "__main__":
	while True:
		hits = 0
		recent_items = http_get('http://pastebin.com/api_scraping.php', params={'limit':result_limit}).json()

		for i, paste in enumerate(recent_items):

			print('\rScraping: {0} / {1}'.format(i+1, result_limit), end='')

			filename = save_path + paste['key']

			if os.path.isfile(filename) or int(paste['size']) < minimum_length:
				continue

			save_paste(filename, http_get(paste['scrape_url']).text)

			hits += 1
			time.sleep(1)

		print("\nHits: {0}".format(hits))
		print("Waiting...\n\n")

		time.sleep(sleep_time)
