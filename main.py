# oauth PRAW template by /u/The1RGood #
#==================================================Config stuff====================================================
import time, praw
import webbrowser
from flask import Flask, request
from threading import Thread
from configparser import ConfigParser

#==================================================End Config======================================================
#==================================================OAUTH APPROVAL==================================================
app = Flask(__name__)

config = ConfigParser()
config.read('example.ini')

#Kill function, to stop server once auth is granted
def kill():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	return "Shutting down..."

#Callback function to receive auth code
@app.route('/')
def authorized():
	global access_information
	state = request.args.get('state', '')
	code = request.args.get('code', '')
	r.auth.authorize(code)
	user = r.user.me()
	text = 'Bot successfully recognized /u/'+user.name
	
	do_task(user)

	return text

def do_task(user):
	approval_sub = host.subreddit(config["App Info"]["subreddit"])
	approval_sub.contributor.add(user.name)

host = praw.Reddit(
	client_id=config["Host Bot"]["id"],
	client_secret=config["Host Bot"]["secret"],
	user_agent="PRAW Testing",
	username=config["Host Bot"]["username"],
	password=config["Host Bot"]["password"]
)

r = praw.Reddit(
	client_id=config["App Info"]["id"],
	client_secret=config["App Info"]["secret"],
	redirect_uri=config["App Info"]["callback"],
	user_agent="Third-Party Reddit Auth"
)

print(r.auth.url(["identity"], "uniqueCode", "temporary"))
app.run(debug=False, port=1701)
#==================================================END OAUTH APPROVAL-=============================================
