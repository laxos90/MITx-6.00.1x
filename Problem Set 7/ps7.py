# 6.00.1x Problem Set 7
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from Tkinter import *


# -----------------------------------------------------------------------
#
# Problem Set 7

# ======================
# Code for retrieving and parsing RSS feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    :param url: a url
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        news_story = NewsStory(guid, title, subject, summary, link)
        ret.append(news_story)
    return ret


# ======================

# ======================
# Part 1
# Data structure design
# ======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link


# ======================
# Part 2
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        :param story: a NewsStory
        """
        raise NotImplementedError


# Whole Word Triggers
# Problems 2-5
class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word.lower()

    def is_word_in(self, text):
        lowercase_text = text.lower()
        text_without_punctuation = replace_punctuation_with_spaces(lowercase_text)
        words = text_without_punctuation.split()

        return self.word in words


def replace_punctuation_with_spaces(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, " ")

    return text


class TitleTrigger(WordTrigger):
    def evaluate(self, story):
        return WordTrigger.is_word_in(self, story.get_title())


class SubjectTrigger(WordTrigger):
    def evaluate(self, story):
        return WordTrigger.is_word_in(self, story.get_subject())


class SummaryTrigger(WordTrigger):
    def evaluate(self, story):
        return WordTrigger.is_word_in(self, story.get_summary())


# Composite Triggers
# Problems 6-8
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)


class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)
# TODO: OrTrigger


# Phrase Trigger
# Question 9

# TODO: PhraseTrigger


# ======================
# Part 3
# Filtering
# ======================

def filter_stories(stories, trigger_list):
    """
    :param trigger_list: a list of triggers
    :param stories: a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in trigger_list fires.
    """
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering)
    return stories


# ======================
# Part 4
# User-Specified Triggers
# ======================

def make_trigger(trigger_map, trigger_type, parameters, name):
    """
    Takes in a map of names to trigger instance, the type of trigger to make,
    and the list of parameters to the constructor, and adds a new trigger
    to the trigger map dictionary.

    :param trigger_map: dictionary with names as keys (strings) and triggers as values
    :param trigger_type: string indicating the type of trigger to make (ex: "TITLE")
    :param parameters: list of strings with the inputs to the trigger constructor (ex: ["world"])
    :param name: a string representing the name of the new trigger (ex: "t1")


    :returns a new instance of a trigger (ex: TitleTrigger, AndTrigger).
    """
    # TODO: Problem 11

def read_trigger_config(file_name):
    """
    :param file_name: a text file that contains information about triggers
    :returns a list of trigger objects that correspond to the rules set in the file file_name
    """

    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    trigger_file = open(file_name, "r")
    all_lines = [line.rstrip() for line in trigger_file.readlines()]
    lines = []
    for line in all_lines:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    triggers = []
    trigger_map = {}

    # Be sure you understand this code - we've written it for you,
    # but it's code you should be able to write yourself
    for line in lines:
        linesplit = line.split(" ")

        # Making a new trigger
        if linesplit[0] != "ADD":
            make_trigger(trigger_map, linesplit[1], linesplit[2:], linesplit[0])
        # Add the triggers to the list
        else:
            for name in linesplit[1:]:
                triggers.append(trigger_map[name])

    return triggers


import thread

SLEEP_TIME = 60  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    try:
        # These will probably generate a few hits...
        t1 = TitleTrigger("Obama")
        t2 = SubjectTrigger("Romney")
        t3 = PhraseTrigger("Election")
        t4 = OrTrigger(t2, t3)
        trigger_list = [t1, t4]


        # TODO: Problem 11
        # After implementing makeTrigger, uncomment the line below:
        # triggerlist = readTriggerConfig("triggers.txt")

        # **** from here down is about drawing ****
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)

        # Gather stories
        guid_shown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guid_shown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_summary())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guid_shown.append(newstory.get_guid())

        while True:
            print "Polling . . .",
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

            # Process the stories
            stories = filter_stories(stories, trigger_list)

            map(get_cont, stories)
            scrollbar.config(command=cont.yview)

            print "Sleeping..."
            time.sleep(SLEEP_TIME)

    except Exception as e:
        print e


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    thread.start_new_thread(main_thread, (root,))
    root.mainloop()
