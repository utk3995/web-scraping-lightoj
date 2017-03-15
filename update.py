import numpy as np
import os
import mechanize
from shutil import copyfile
from bs4 import BeautifulSoup
import requests
import re
import taggetter
import os.path

def save_images(body , quesitonCode):
    start = 0
    flag = 0
    sub = "src="
    while True:
        start = body.find(sub,start)
        if start == -1: return
        if (flag == 0):
        	flag = 1
        	directory = "./website/files/data/problems/desc/"+str(quesitonCode)
        	if not os.path.exists(directory):
        		os.makedirs(directory)
        newurl = "http://lightoj.com/"
        i = start+5
        while (body[i] != '"'):
        	newurl = newurl + body[i]
        	i = i+1
        #print newurl
        words = newurl.split("/")
        filename = words[7]
        filepathname = "./website/files/data/problems/desc/"+str(quesitonCode)+"/"+filename
        #print filepathname
        url = br.open(newurl)
        returnPage = url.read()
        output = open(filepathname,"wb")
        output.write(returnPage)
        output.close() 
        start += len(sub)


def get_forum_code(quesitonCode):
	url = br.open("http://www.lightoj.com/forum_showproblem.php?problem="+str(quesitonCode))
	returnPage = url.read() 
	words = returnPage.split("=")
	forumCode = words[5]
	words = forumCode.split("'")
	forumCode = words[0]
	return forumCode


def get_filelink(tag):
	newtag = ""
	for i in tag:
		if (i == ' '):
			newtag = newtag + '%20'
		elif (i == '/'):
			newtag = newtag + '-'
		else:
			newtag = newtag + i
	return newtag

def get_filename(tag):
	newtag = ""
	for i in tag:
		if (i == '/'):
			newtag = newtag + '-'
		else:
			newtag = newtag + i
	return newtag

def print_tags(tags,questionTitle,quesitonCode):
	count = 0;
	for tag in tags:
		global list_of_tags
		list_of_tags.append(tag)
		filelink = get_filelink(tag)
		filename = get_filename(tag)
		outfile.write('<a href= tags/'+filelink+'.html target="_blank">'+tag+'</a>');
		count = count + 1
		if (count != len(tags)):
			outfile.write(", ")
		if os.path.isfile('./website/files/tags/'+filename+'.html'):
			tagfile = open('./website/files/tags/'+filename+'.html',"a")
			tagfile.write('<a href=../'+str(quesitonCode)+'.html>'+questionTitle+'</a><br>\n');
			tagfile.close()
		else:
			tagfile = open('./website/files/tags/'+filename+'.html',"a")
			tagfile.write('<p align="right"> <a href="../../index.html"> Home </a></p>\n')
			tagfile.write('<center><h1>'+ tag +'</h1></center><br>\n');
			tagfile.write('<a href=../'+str(quesitonCode)+'.html>'+questionTitle+'</a><br>\n');
			tagfile.close()
	outfile.write("</h3><br/>")


def create_tag_index_file(list_of_tags):
	count = 1
	list_of_tags = set(list_of_tags)
	tagindex = open('./website/files/tags/index.html',"w")
	tagindex.write('<p align="right"> <a href="../../index.html"> Home </a></p>\n')
	tagindex.write('<center><h1>List of Tags</h1></center><br>\n');
	for tag in list_of_tags:
		filelink = get_filelink(tag)
		tagindex.write(str(count)+'. <a href= '+filelink+'.html target="_blank">'+tag+'</a><br/>')
		count = count + 1
	tagindex.close()


list_of_tags = []
count = 1
br = mechanize.Browser()
br.set_handle_robots(False)
br.open("http://www.lightoj.com/login_main.php")	   #Url that contains signin form
br.select_form(nr=0)
br['myuserid'] = ""	#see what is the name of txt input in form   #your user id here
br['mypassword'] = "" #your password here
result = br.submit().read()
if (result == "<script>location.href='login_success.php'</script>"):
    print "Login Success"
else:
    print "Login Failure"


indexfile = open('./website/index.html','w')
indexfile.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n')
indexfile.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
indexfile.write('\t<title>List of Problems</title>\n')
indexfile.write('<body style="background: white; font-family: Helvetica">\n')
indexfile.write('<h1> List of solved problems </h1>\n')

indexfile.write('<h2> <a href="files/tags/"> Search by Tags </a></h2><br/>\n')

fil = "./website/files/tags/*"
os.system('rm '+fil)


for file in os.listdir("./source_cpp/"):
	if file.endswith(".cpp"):
		copyfile('./source_cpp/'+file,'./input.cpp')
		os.system("./convertor")
		copyfile('./output.cpp','./converted_cpp/'+file)
		os.system("rm output.cpp")
		os.system("rm input.cpp")


for file in os.listdir("./converted_cpp/"):
	if file.endswith(".cpp"):
		words = file.split(".")
		quesitonCode = words[0]
		print quesitonCode
		url = br.open("http://lightoj.com/volume_showproblem.php?problem="+str(quesitonCode))
		returnPage = url.read() 
		returnHtml = open('temphtml.html','w')
		returnHtml.write(returnPage)
		returnHtml.close()
		os.system("./probStatementExtractor")
		pageTitle = br.title()
		words = pageTitle.split("::")
		questionTitle = words[1]
		words = questionTitle.split("-")
		problemName = words[1]
		probStatementFile = open('probstatement.txt','r')
		problemStatement = probStatementFile.read()

		#getting tags
		forumCode = get_forum_code(quesitonCode)
		tags = taggetter.get_tags(forumCode)
		#getting tags


		save_images(problemStatement,quesitonCode)

		indexfile.write(str(count)+'. ')
		count = count + 1
		indexfile.write('<a href=files/'+str(quesitonCode)+'.html>'+questionTitle+'</a><br>\n')

		outfile = open('./website/files/'+quesitonCode+'.html','w')
		infile  = open('./converted_cpp/'+quesitonCode+'.cpp','r')

		outfile.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n')
		outfile.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
		outfile.write('<head>\n')
		outfile.write('\t<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n')
		outfile.write('\t<title>'+questionTitle+'</title>\n')
		outfile.write('\t<script type="text/javascript" src="../scripts/shCore.js"></script>\n')
		outfile.write('\t<script type="text/javascript" src="../scripts/shBrushCpp.js"></script>\n')
		outfile.write('\t<link type="text/css" rel="stylesheet" href="../styles/shCoreDefault.css"/>\n')
		outfile.write('\t<script type="text/javascript">SyntaxHighlighter.all();</script>\n')
		outfile.write('</head>\n')
		outfile.write('<body style="background: white; font-family: Helvetica">\n')
		outfile.write('<p align="right"> <a href="../index.html"> Home </a></p>\n')
		outfile.write('<h1>Question Code : '+str(quesitonCode)+'</h1>\n')
		outfile.write('<h1>Problem Name : <a href=http://lightoj.com/volume_showproblem.php?problem='+str(quesitonCode)+' target="_blank" >'+problemName+'</a></h1><br/>\n')
		outfile.write('<h3>Problem Tags : \n')
		print_tags(tags,questionTitle,quesitonCode)
		outfile.write('<h3>Problem Statement : </h3>\n')
		outfile.write(problemStatement+'<br/>');
		outfile.write('<h3>Code : </h3>\n')
		outfile.write('<pre class="brush: cpp;">\n')
		#file input
		input_str = infile.read()
		outfile.write(input_str);
		#file input
		outfile.write('</body>\n')
		outfile.write('</pre>\n')
		outfile.write('</html>\n')
		outfile.close()
		os.system("rm probstatement.txt")
		os.system("rm temphtml.html")

create_tag_index_file(list_of_tags)
indexfile.write('</body>\n')
indexfile.write('</html>\n')
indexfile.close()