import cherrypy
import pyautogui
import time
import os

video_direcory = r"D:\Videos\TempVideo\172.16.3"


class Root(object):
	@cherrypy.expose
	def index(self):
		return """<html>
	  <head></head>
	  <body>
		<form method="get" action="generate">
		  <button type="submit">Make Video</button>
		</form>
	  <body>
	</html>"""
	@cherrypy.expose
	def generate(self):
		pyautogui.click(933, 332)
		return
	@cherrypy.expose
	def filename(self):
		return os.listdir(video_direcory)
	@cherrypy.expose
	def start(self):
		# if video directory is empty start video
		if os.listdir(video_direcory) == []: 
			pyautogui.click(933, 332)
		else: # else do nothing
			print("already running")
	@cherrypy.expose
	def stop(self):
		if os.listdir(video_direcory) != []: 
			pyautogui.click(933, 332)
		else:
			print("nothing is currently running")
		
if __name__ == '__main__':
	cherrypy.config.update({'server.shutdown_timeout':1, 'server.socket_host':'0.0.0.0', 'server.socket_port':7788})
	cherrypy.quickstart(Root(), '/')
		