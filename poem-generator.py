#--------------------------------------------------------------------------
#
#                            Poem Generator Program
#
#--------------------------------------------------------------------------

# Import statements 
from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from threading import Timer
import http.client
import random

# Global Variables
root = Tk()
var = StringVar()
key = None

# This is input module. Also has a part where to extract the URL from web
# Collect the relevant urls from the search engine for the
# user supplied keyword
# You can make a seperate input part and put all the validation I have explained.
def collect_urls():
    global key
    try:
        # Define and set an agent
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]

        # Build the URL
        # This part needs a proper construction format
        url = "http://www.google.com/search?q="+ key +"&start="

        # Open the page and parse through the BeautifulSoup
        page = opener.open(url)
        soup = BeautifulSoup(page, "html.parser")

        # Open a fle and write all the links
        # Links can be obtained tagged with 'cite'
        file = open("links.txt", "w")
        for cite in soup.find_all('cite'):
            file.write(cite.text)
            file.write("\n")

        # Close the file
        file.close()
        
    except (urllib.request.HTTPError, urllib.request.URLError, http.client.HTTPException, BaseException):
         pass


	
# Validate the collected URLS and retain only the valid ones 
# Not all collected URL may be valid. Remove all such invalid ones. More can be added here
# example we dont want any youtube links   
def validate_urls():
    wfile = open("rlink.txt", "w")
    with open('links.txt') as rfile:
        for line in rfile:
            if line.find("www") >= 0 and \
               line.find("youtube") == -1 and \
               line.find("facebook") == -1 and \
               line.find("imdb") == -1 and \
               line.find("...") == -1:
                wfile.write(line)
                
    wfile.close()
    rfile.close()


# This part is the get the data from the collected URL
# the data is written to file	
def get_data():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    wfile = open("data.txt", "w")
    rfile = open('rlink.txt', "r")

    with open("rlink.txt") as rfile:
        for line in rfile:
            try:
                if line.startswith('http'):
                    page = opener.open(line)
                else:
                    page = opener.open("http://"+line)

                soup = BeautifulSoup(page,"html.parser")

            except(urllib.request.HTTPError, urllib.request.URLError, http.client.HTTPException, http.client.IncompleteRead, BaseException):
                continue

            for script in soup(["script", "style"]):
                script.extract()
            try:
                result = soup.get_text().lower()
                wfile.write(result)
            except (SystemError, UnicodeEncodeError):
                continue

    wfile.close()
    rfile.close()

	
# This will clean the data
# Remove all the white spaces
# more can be added here	
def clean_data():
    file = open("data.txt", "r")
    new = open("clean_data.txt", "w")
    for line in file:
        if line.rstrip():
            new.write(line)

    file.close()
    new.close()

	
# make the lines into 4 words	
def make_four():
    file = open("clean_data.txt", "r")
    four = open("make_four.txt", "w")
    count =  0
    
    for line in file:
        nline = line.split()
        if len(nline) >= 4:
            four.write(nline[0]+" "+nline[1]+" "+ nline[2]+" "+ nline[3])
            four.write("\n")

    file.close()
    four.close()
            

# Generate the poem
# Logic can be as per convience			
def write_poem():
    global key
    flag = 0
    l1 = 0
    l2 = 0
    l3 = 0
    l4 = 0
    
    file = open("make_four.txt", "r")
    poem = open("poem.txt", "w")
    count = 0
    line_list = []
    
    for line in file:
        line_list.append(line)
    list_length = len(line_list)
    list_length = list_length - 1

    for ll in line_list:
        if key in ll:
            line_list[l1] = ''.join([i for i in line_list[l1] if not i.isdigit()])
            poem.write(ll)
            flag = 1
            break

    if flag == 0:
        l1 = random.randrange(list_length)
        line_list[l1] = ''.join([i for i in line_list[l1] if not i.isdigit()])
        poem.write(line_list[l1])
    else:
        l1 = random.randrange(list_length)

    l2 = random.randrange(list_length)
    if l2 == l1:
        l2 = l2 + 5
        if l2 > list_length:
            l2 = 0
    line_list[l2] = ''.join([i for i in line_list[l2] if not i.isdigit()])
    poem.write(line_list[l2])

    l3 = random.randrange(list_length)
    if l3 == l1 or l3 == l2:
        l3 = l1 + 1
        if l3 > list_length:
            l3 = 0
    line_list[l3] = ''.join([i for i in line_list[l3] if not i.isdigit()])
    poem.write(line_list[l3])

    l4 = random.randrange(list_length)
    if l4 == l1 or l4 == l2 or l4 == l3:
        l4 = list_length
    line_list[l4] = ''.join([i for i in line_list[l4] if not i.isdigit()])
    poem.write(line_list[l4])
        
    file.close()
    poem.close()
    activate_result_window()

def display_poem():
    global key
    root.destroy()
    results = Tk()
    results.geometry("800x600")
    results.title("Poem Results")
    l = []
    poem = open("poem.txt", "r")
    for line in poem:
        l.append(line)

    label = Label(results, text="Poem on " + key, fg = "black", font = "Verdana 20 bold")
    label.pack()
    label.place(relx=0.5, rely=0.1, anchor=CENTER)

    text = Text(results)
    text.insert(INSERT, l[0]+"\n"+l[1]+"\n"+l[2]+"\n"+l[3])
    text.pack()
    text.place(relx=0.5, rely=0.5, anchor=CENTER)

    

def activate_result_window():
    # Reset the elements in the GUI
    rB = Button(root, text ="Check Poem", command = display_poem)
    rB.pack()
    rB.place(relx=0.5, rely=0.85, anchor=CENTER, height=30, width=150)

    label = Label(root, text="...PROCESSED...",
		 fg = "black",
		 font = "Verdana 20 bold")
    label.pack()
    label.place(relx=0.5, rely=0.65, anchor=CENTER)

    processing_bar = ttk.Progressbar(root, orient='horizontal', mode='indeterminate')
    processing_bar.place(relx=0.5, rely=0.75, anchor=CENTER)
    processing_bar.stop()
    
# Main function to aggregate all
def poem_generator():
    collect_urls()
    validate_urls()
    get_data()
    clean_data()
    make_four()
    write_poem()

def progress():
    global key

    key = var.get()
    label = Label(root, text="...PROCESSING...",
		 fg = "black",
		 font = "Verdana 20 bold")
    label.pack()
    label.place(relx=0.5, rely=0.65, anchor=CENTER)
    processing_bar = ttk.Progressbar(root, orient='horizontal', mode='indeterminate')
    processing_bar.place(relx=0.5, rely=0.75, anchor=CENTER)
    processing_bar.start(30)

    t = Timer(3, poem_generator)
    t.start()
   

def main():
    
    root.geometry("1000x600")
    root.title("Poem Generator")

    image = PhotoImage(file="logo.gif")
    labelp = Label(image=image)
    labelp.pack()
    labelp.place(relx=0.5, rely=0.2, anchor=CENTER)

    key_display = Label(root, text="Enter Key Word for Poem")
    key_display.pack()
    key_display.place(relx=0.2, rely=0.4, anchor=CENTER)
    
    user_input = Entry(root, bd=7,textvariable=var)
    user_input.pack()
    user_input.place(relx=0.5, rely=0.4, anchor=CENTER)

    B = Button(root, text ="-- Run --", command = progress)
    B.pack()
    B.place(relx=0.5, rely=0.5, anchor=CENTER, height=50, width=150)
    
    root.mainloop()

main()
