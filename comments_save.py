import praw
import time
import csv
from pmaw import PushshiftAPI
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

def main():
    #Requests for a name and word, and then runs it through the methods
    # subreddit_name = input("Subreddit would you like to search: ")
    # word = input("Word of importance: ")
    # training_comments, training_score = get_data(subreddit_name, word)
    # training_comments = token_to_string(tokenizer(training_comments))
    # print(training_comments)
    relevant_comments, relevant_upvotes, training_comments, training_upvotes = get_data('python', 'linux')
    relevant_comments = tokenizer(relevant_comments)
    relevant_upvotes = sentimentify(relevant_upvotes)
    training_comments = tokenizer(training_comments)
    training_upvotes = sentimentify(training_upvotes)



# Collects data (comments) that include a word of interests within a subreddit, looking through top of year

def get_data(subreddit, word_of_interest):

    #Logs into Reddit
    reddit = praw.Reddit(
        client_id="cwduRY3F066SDFU1wzlV7Q",
        client_secret="w46roD2lBrOp3fR3Hm5o_NcfcmTang",
        password="tooC0mpl1cat3d-?",
        user_agent="Sentiment Analysis Bot test by u/Sentim3nt",
        username="Sentim3nt",
    )

    #Collects training dataset
    #Sets up counters for data collection information
    scan_count = 0
    post_count= 0
    read_count = 0
    start = time.time()
    relevant_comments = []
    relevant_upvotes = []
    training_comments = []
    training_upvotes = []
    post_limit = 0

    for submission in reddit.subreddit(subreddit).top(time_filter="year", limit = 1):
        num_comments = submission.num_comments
        if(num_comments >= 8000):
            post_limit = 1
        elif(num_comments > 4000):
            post_limit = 2
        elif(num_comments > 2000):
            post_limit = 4
        elif(num_comments > 1000):
            post_limit = 8
        elif(num_comments > 500):
            post_limit = 16
        elif(num_comments > 250):
            post_limit = 32
        elif(num_comments > 125):
            post_limit = 64
        elif(num_comments > 64):
            post_limit = 128
        else:
            post_limit = 300



    #Sorts through first 100 posts in top of year within a given subreddit
    for submission in reddit.subreddit(subreddit).top(time_filter="year", limit = post_limit):

        #Live viewing of data collection
        title = submission.title
        post_count+=1
        print("Currently Reading Post", post_count, ":", submission.title)
        
        #Ensures no "MoreComments" object errors
        submission.comments.replace_more(limit=None)

        #Looks through top level comments
        level_list = []
        for i in range(len(submission.comments[:])):
            level_list.append(1)
        comment_queue = list(zip(submission.comments[:],level_list))
        while comment_queue:

            #Reads through a comment, checks if the specified word is present. If so, it collects the comment. 
            comment, level = comment_queue.pop(0)
            read_count+=1
            if(word_of_interest in comment.body):
                relevant_comments.append(comment.body)
                relevant_upvotes.append(float(comment.score*level)/submission.score)
            else:
                training_comments.append(comment.body)
                training_upvotes.append(float(comment.score*level)/submission.score)
            reply_level = []
            for i in range(len(comment.replies)):
                reply_level.append(level*3)
            comment_queue.extend(list(zip(comment.replies,reply_level)))



    for submission in reddit.subreddit(subreddit).search(query = word_of_interest, sort = 'comments', time_filter = 'year'):
        num_comments = submission.num_comments
        if(num_comments > 4000):
            post_limit = 3
        elif(num_comments > 2000):
            post_limit = 6
        elif(num_comments > 1000):
            post_limit = 12
        elif(num_comments > 500):
            post_limit = 24
        elif(num_comments > 250):
            post_limit = 48
        elif(num_comments > 125):
            post_limit = 96
        elif(num_comments > 64):
            post_limit = 192
        else:
            post_limit = 384

    post_count = 0
    #Ends time, and then prints data
    for submission in reddit.subreddit(subreddit).search(query = word_of_interest, sort = 'comments', time_filter = 'all', limit = post_limit):

        #Live viewing of data collection
        title = submission.title
        post_count+=1
        print("Currently Scanning Post", post_count, ":", submission.title)
        
        #Ensures no "MoreComments" object errors
        submission.comments.replace_more(limit=None)

        #Looks through top level comments
        while comment_queue:

            #Reads through a comment, checks if the specified word is present. If so, it collects the comment. 
            comment, level = comment_queue.pop(0)
            scan_count+=1
            if(word_of_interest in comment.body):
                relevant_comments.append(comment.body)
                relevant_upvotes.append(float(comment.score*level)/submission.score)
            reply_level = []
            for i in range(len(comment.replies)):
                reply_level.append(level*3)
            comment_queue.extend(list(zip(comment.replies,reply_level)))

    end=time.time()
    print((end-start)/60, "minutes to read", read_count, "comments and scan", scan_count, "comments")
    return relevant_comments, relevant_upvotes, training_comments, training_upvotes


def tokenizer(collected_comments):

    #Tokenizes each comment for easier cleaning and sorting
    start = time.time()

    #Cleans comments
    num = 0                                         
    while num < len(collected_comments):
        collected_comments[num] = special_cleaner(collected_comments[num], True)           
        collected_comments[num] = collected_comments[num].strip().lower()     #Lowers text
        collected_comments[num] = collected_comments[num].split()             #Tokenizes text
        collected_comments[num] = stop_word_cleaner(collected_comments[num])  #Removes links and stopwords
        num += 1
    end=time.time()
    collected_comments = stem_txt(collected_comments)
    print((end-start)/60, "minutes to tokenize", len(collected_comments), "comments")
    return collected_comments


def stop_word_cleaner(tokens):
    stop_words = stopwords.words('english')
    for index in range(0, len(stop_words)):
        stop_words[index] = special_cleaner(stop_words[index], False)
    stop_words = set(stop_words)
    cnt = 0
    while cnt < len(tokens):         
        if "https" in tokens[cnt] or tokens[cnt] in stop_words:
            tokens.remove(tokens[cnt])
        else:
            cnt+=1
    return tokens


def special_cleaner(str, bool):

    #Cleans a str of alphanumeric characters
    cleaned = ""
    index = 0
    while index < len(str):
        if bool == True and (str[index] == chr(0x2019) or str[index] == chr(0x2018) or str[index] == chr(0x0027) or str[index] == chr(0x0060) or str[index] == chr(0x00B4)):
            cleaned+=" "
        elif str[index].isalnum() or str[index].isspace():
            cleaned+=str[index]
        index+=1
    return cleaned


def stem_txt(list_comments):
    ss = SnowballStemmer('english')
    for index in range(0, len(list_comments)):
        str = " "
        for w in list_comments[index]:
            str+=ss.stem(w) + " "
        list_comments[index] = str.split()
    return list_comments


def save_to_file(collected_comments):

    #Saves each comment into a file for proof of concept, and times it.
    start = time.time()
    with open('relevantcomments.txt', 'w', encoding="utf-8") as file:
        for item in collected_comments:
            file.write("[ ")
            for word in item:
                file.write("[" + word + "] ")
            file.write(" ]\n\n")
    end = time.time()
    print((end-start)/60, "minutes to save each collected comment to a file")


def token_to_string(token_list):
    for cnt in range(0, len(token_list)):
        token_string = ""
        for index in range(0, len(token_list[cnt])):
            token_string += str(token_list[cnt][index]) + " "
        token_list[cnt] = token_string.strip()
    return token_list

def sentimentify(score_list):
        print(score_list)




if __name__ == '__main__':   # Runs main
    main()
