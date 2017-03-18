#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import json
import os

from httplib2 import Http

from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
	def get(self):
		scopes = ['https://www.googleapis.com/auth/gmail.readonly']

		credentials = ServiceAccountCredentials.from_json_keyfile_name(
		    'client_secret.json', scopes)
		# delegated_credentials = credentials.create_delegated('vy@fju.us')
		http = credentials.authorize(Http())
		service = build('gmail', 'v1', http=http)
		results = service.users().labels().list(userId='me').execute()
		labels = results.get('labels', [])

		if not labels:
			print('No labels found.')
		else:
			print('Labels:')
			for label in labels:
				print(label['name'])

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
