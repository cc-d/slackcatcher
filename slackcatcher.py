#!/usr/bin/env python
import subprocess
import sys
import json
import requests
import logging
import os
logger = logging.getLogger('slackcatcher')

def main():
	command = ' '.join(sys.argv[1:])
	config_path = os.path.dirname(os.path.realpath(__file__)) + '/config.json'
	with open(config_path, 'r') as c:
		config = json.loads(c.read())
	try:
		response = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
		logger.debug('No errors occured.')

	except subprocess.CalledProcessError as e:
		logger.debug('An error has occured.')
		payload = {key:config[key] for key in config if key != 'webhook_url'}
	
		payload['attachments'] = [{
						"title":"Error",
						"fallback":e.output, 
						"fields": [{
							"title":command,
							"value":e.output,
						}],
						"color":"danger",
					}]

		payload = json.dumps(payload)
		r = requests.post(config['webhook_url'], data={'payload':payload})
	
if __name__ == '__main__':
	main()
