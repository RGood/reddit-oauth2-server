# oauth PRAW template by /u/The1RGood #
#==================================================Config stuff====================================================
import time, praw
import webbrowser
import logging
from flask import Flask, request, redirect
from threading import Thread
from configparser import ConfigParser

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
#==================================================End Config======================================================
#==================================================OAUTH APPROVAL==================================================
app = Flask(__name__)

config = ConfigParser()
config.read('example.ini')

#Callback function to receive auth code
@app.route("/{0}".format("/".join(config["App Info"]["callback"].split("/")[3:])))
def authorized():
	global access_information
	state = request.args.get('state', '')
	code = request.args.get('code', '')
	r.auth.authorize(code)
	user = r.user.me()

	do_task(user)

	return redirect(config["App Info"]["return_to_url"], code=302)

def do_task(user):
	approval_sub = host.subreddit(config["App Info"]["subreddit"])
	approval_sub.contributor.add(user.name)
	print("Approved User: {0}".format(user.name))

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
app.run(debug=False, host="0.0.0.0", port=1701)
#==================================================END OAUTH APPROVAL-=============================================
