#!/usr/bin/python

import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts, users, taxonomies
from apiclient.discovery import build
from optparse import OptionParser

WPPATH = "http://vicubic.com/xmlrpc.php"
WPUSER = "sergibondarenko"
WPPASS = "zef1rv1ter"
DEVELOPER_KEY = "AIzaSyCEmhLRLXatMGEtEVQ78Roo83VdaDpaYZ8"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def func_Create_WP_Post(atitle, acontent, category):
	wp = Client(WPPATH, WPUSER, WPPASS)
	my_category = category
	post = WordPressPost()
	post.title = atitle
	post.content = acontent
	post.post_format = "video"
	post.terms_names = {'category':[my_category]}

	
	print(category)
	print("---")
	
	my_posts = []
	#my_posts = set()
	my_increment = 20
	my_offset = 0
	while True:
		wp_obj_posts = wp.call(posts.GetPosts({'number': my_increment, "offset": my_offset}))
		if len(wp_obj_posts) == 0:
			break
		for apost in wp_obj_posts:
			apost = apost.content
			apost = apost.split("embed/",1)[1]
			#my_posts.add(apost) 
			my_posts.append(apost) 
			#try:
			#	print(apost.title)
			#except UnicodeEncodeError:
			#	print("'ascii' codec can't encode character.")
		my_offset += my_increment

	#print(wp_obj_posts)
	#print("---")
	
	print(my_posts)
	print("---")

	post_id = post.content.split("embed/",1)[1]
	print(post_id)
	#my_posts = sorted(my_posts)
	if post_id in my_posts:
		print("Dublicate post!!!\n")
		print("---")
	else:
		print("Posted!\n")
		print("---")
		post.id = wp.call(posts.NewPost(post))
		post.post_status = 'publish'
		wp.call(posts.EditPost(post.id, post))
		#wp.call(NewPost(post))


def youtube_search(options):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
	
	search_response = youtube.search().list(
		q=options.q,
		part="id,snippet",
		maxResults=options.maxResults
	).execute()

	videos = []

	for search_result in search_response.get("items", []):
		if search_result["resourceId"]["kind"] == "youtube#video":
			videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))	
			func_Create_WP_Post(search_result["snippet"]["title"], 
				"http://www.youtube.com/embed/" + search_result["id"]["videoId"])

	print("-----")
	print "Videos:\n", "\n".join(videos), "\n"


def youtube_parse_builtin_plst(options):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

	search_request = youtube.playlistItems().list(
		playlistId = options.playlistId,
		part = "snippet",
		maxResults = options.maxResults
	)

	search_response = search_request.execute()		

	video_dict = {}
	for search_result in search_response["items"]:
		if search_result["snippet"]["resourceId"]["kind"] == "youtube#video":
			video_dict.setdefault(search_result["snippet"]["title"], {'videoid':search_result["snippet"]["resourceId"]["videoId"], 'position':search_result["snippet"]["position"]})
			#video_dict[search_result["snippet"]["title"]] = search_result["snippet"]["resourceId"]["videoId"]

	return video_dict
	

if __name__ == "__main__":
	my_categories = {"Brand-New Tech":"PLrEnWoR732-CV75Y0BCvbVyGDtjoghNEg", 
				"Hot New Trailers":"PLrEnWoR732-CvU2EIng1mKhlXJHvaiAVM", 
				"Just-Released Music Videos":"PLrEnWoR732-D67iteOI6DPdJH1opjAuJt", 
				"Learn Something New":"PLrEnWoR732-DZV1Jc8bUpVTF_HTPbywpE",
				"Popular Right Now":"PLrEnWoR732-CANlyfrCKexT5JOze-HhDj", 
				"The Daily 'Aww'":"PLrEnWoR732-DN561GnxXKMlocLMc4v4jL",
				"Today's Funniest Clips":"PLrEnWoR732-AKYdZyzAnuf-MnPiw7rT4Q"}
	
	MAX_RESULTS = 50

	parser = OptionParser()
	parser.add_option("--playlistId", dest="playlistId", default="PLrEnWoR732-CV75Y0BCvbVyGDtjoghNEg")
	parser.add_option("--max-results", dest="maxResults", default=MAX_RESULTS)
	(options, args) = parser.parse_args()
	one_dict = youtube_parse_builtin_plst(options)
	
	parser = OptionParser()
	parser.add_option("--playlistId", dest="playlistId", default="PLrEnWoR732-CvU2EIng1mKhlXJHvaiAVM")
	parser.add_option("--max-results", dest="maxResults", default=MAX_RESULTS)
	(options, args) = parser.parse_args()
	two_dict = youtube_parse_builtin_plst(options)
	
	parser = OptionParser()
	parser.add_option("--playlistId", dest="playlistId", default="PLrEnWoR732-D67iteOI6DPdJH1opjAuJt")
	parser.add_option("--max-results", dest="maxResults", default=MAX_RESULTS)
	(options, args) = parser.parse_args()
	three_dict = youtube_parse_builtin_plst(options)
	
	parser = OptionParser()
	parser.add_option("--playlistId", dest="playlistId", default="PLrEnWoR732-DZV1Jc8bUpVTF_HTPbywpE")
	parser.add_option("--max-results", dest="maxResults", default=MAX_RESULTS)
	(options, args) = parser.parse_args()
	four_dict = youtube_parse_builtin_plst(options)
	
	parser = OptionParser()
	parser.add_option("--playlistId", dest="playlistId", default="PLrEnWoR732-CANlyfrCKexT5JOze-HhDj")
	parser.add_option("--max-results", dest="maxResults", default=MAX_RESULTS)
	(options, args) = parser.parse_args()
	five_dict = youtube_parse_builtin_plst(options)
	
	parser = OptionParser()
	parser.add_option("--playlistId", dest="playlistId", default="PLrEnWoR732-DN561GnxXKMlocLMc4v4jL")
	parser.add_option("--max-results", dest="maxResults", default=MAX_RESULTS)
	(options, args) = parser.parse_args()
	six_dict = youtube_parse_builtin_plst(options)
	
	parser = OptionParser()
	parser.add_option("--playlistId", dest="playlistId", default="PLrEnWoR732-AKYdZyzAnuf-MnPiw7rT4Q")
	parser.add_option("--max-results", dest="maxResults", default=MAX_RESULTS)
	(options, args) = parser.parse_args()
	seven_dict = youtube_parse_builtin_plst(options)


	#print(one_dict)
	for position in range(49, -1, -1):
		for video in one_dict:
			if one_dict[video]['position'] == position:
				#print one_dict[video]['videoid']  
				ctgry = 'Brand-New Tech'
				func_Create_WP_Post(video, "http://www.youtube.com/embed/" + one_dict[video]['videoid'], ctgry)
		for video in two_dict:
			if two_dict[video]['position'] == position:
				#print two_dict[video]['videoid']  
				ctgry = 'Hot New Trailers'
				func_Create_WP_Post(video, "http://www.youtube.com/embed/" + two_dict[video]['videoid'], ctgry)
		for video in three_dict:
			if three_dict[video]['position'] == position:
				#print three_dict[video]['videoid']  
				ctgry = 'Just-Released Music Videos'
				func_Create_WP_Post(video, "http://www.youtube.com/embed/" + three_dict[video]['videoid'], ctgry)
		for video in four_dict:
			if four_dict[video]['position'] == position:
				#print four_dict[video]['videoid']  
				ctgry = 'Learn Something New'
				func_Create_WP_Post(video, "http://www.youtube.com/embed/" + four_dict[video]['videoid'], ctgry)
		for video in five_dict:
			if five_dict[video]['position'] == position:
				#print five_dict[video]['videoid']  
				ctgry = 'Popular Right Now'
				func_Create_WP_Post(video, "http://www.youtube.com/embed/" + five_dict[video]['videoid'], ctgry)
		for video in six_dict:
			if six_dict[video]['position'] == position:
				#print six_dict[video]['videoid']  
				ctgry = "The Daily 'Aww'"
				func_Create_WP_Post(video, "http://www.youtube.com/embed/" + six_dict[video]['videoid'], ctgry)
		for video in seven_dict:
			if seven_dict[video]['position'] == position:
				#print seven_dict[video]['videoid']  
				ctgry = "Today's Funniest Clips"
				func_Create_WP_Post(video, "http://www.youtube.com/embed/" + seven_dict[video]['videoid'], ctgry)
			
	
'''
	for position in range(49, 0, -1):
		for ctgry in my_categories:
			parser = OptionParser()
			parser.add_option("--playlistId", dest="playlistId", default=my_categories[ctgry])
			parser.add_option("--max-results", dest="maxResults", default=50)
			(options, args) = parser.parse_args()

			video_dict = youtube_parse_builtin_plst(options, ctgry, position)
			#print(video_dict)
			for video in video_dict:
				func_Create_WP_Post(video, "http://www.youtube.com/embed/" + video_dict[video], ctgry)
	for i in range(1, 50):
		for ctgry in my_categories:
			parser = OptionParser()
			parser.add_option("--playlistId", dest="playlistId", default=my_categories[ctgry])
			parser.add_option("--max-results", dest="maxResults", default=i)
			(options, args) = parser.parse_args()

			video_dict = youtube_parse_builtin_plst(options, ctgry)
			for video in video_dict:
				func_Create_WP_Post(video, "http://www.youtube.com/embed/" + video_dict[video], ctgry)
'''
