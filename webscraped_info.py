import praw
import time
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk import classify
from nltk import NaiveBayesClassifier

def main():
    # Training model
    training_comments, training_score, testing_comments, testing_score = get_data("training.1600000.processed.noemoticon.csv")
    training_comments = tokenizer(training_comments)
    testing_comments = tokenizer(testing_comments)
    training = (list(zip(training_comments, training_score)))
    testing = (list(zip(testing_comments, testing_score)))
    training_set = [(feature_label(comment), score) for (comment, score) in training]
    testing_set = [(feature_label(comment), score) for (comment, score) in testing]
    classifier = NaiveBayesClassifier.train(training_set)
    print("Accuracy is", classify.accuracy(classifier, testing_set))
    # Model is trained

    subreddit_name = input("Subreddit would you like to search: ")
    word = input("Word of importance: ")
    relevant_comments = relevant_data(subreddit_name, word)
    relevant_comments = (list(tokenizer(relevant_comments)))

    classified_comments =[]
    for comments in relevant_comments:
        classified_comments.append([{comment:classifier.classify(feature_label(comment))} for comment in comments])
    print(classified_comments)
    pos = 0
    neg = 0
    total = 0
    for comment in classified_comments:
        for words in comment:
            for word in words:
                if words[word] == '4':
                    pos += 1
                else:
                    neg += 1
                total +=1

    print("The percentage of positivity is", pos/total)
    print("The percentage of negativity is", neg/total)
            
    
def feature_label(comment):
    comment = set(comment)
    my_dict = dict([(word, True) for word in comment])
    return my_dict

def get_data(filename):
    training_comments = []
    training_data = []
    testing_comments = []
    testing_data = []
    reader = 0
    students = open(filename, "r")
    read_file = csv.reader(students)
    iterator = 0
    for row in read_file:
        if iterator % 100 == 0:
            if iterator % 400 == 0:
                testing_comments.append(row[5])
                testing_data.append(row[0])
            else:
                training_comments.append(row[5])
                training_data.append(row[0])
        iterator += 1
    students.close()
    return training_comments, training_data, testing_comments, testing_data
    
def relevant_data(subreddit, word_of_interest):

    #Logs into Reddit
    reddit = praw.Reddit(
        client_id="cwduRY3F066SDFU1wzlV7Q",
        client_secret="w46roD2lBrOp3fR3Hm5o_NcfcmTang",
        password="tooC0mpl1cat3d-?",
        user_agent="Sentiment Analysis Bot test by u/Sentim3nt",
        username="Sentim3nt",
    )
    relevant_comments = []
    post_count = 0
    read_count = 0

    for submission in reddit.subreddit(subreddit).search(query = word_of_interest, sort = 'comments', time_filter = 'month', limit = 1):
        num_comments = submission.num_comments
        if(num_comments > 1000):
            post_limit = 8
        elif(num_comments > 500):
            post_limit = 16
        elif(num_comments > 250):
            post_limit = 32
        elif(num_comments > 125):
            post_limit = 64
        elif(num_comments > 64):
            post_limit = 128
        elif(num_comments > 64):
            post_limit = 256
        elif(num_comments > 32):
            post_limit = 512
        elif(num_comments > 16):
            post_limit = 1024
        else:
            post_limit = 2048


    #Sorts through first 100 posts in top of year within a given subreddit
    for submission in reddit.subreddit(subreddit).top(time_filter="year", limit = post_limit):

        #Live viewing of data collection
        post_count+=1
        print("Currently Reading Post", post_count, ":", submission.title)
        
        #Ensures no "MoreComments" object errors
        submission.comments.replace_more(limit=8, threshold=20)

        #Looks through top level comments
        comment_queue = submission.comments[:]

        while comment_queue:
            comment = comment_queue.pop(0)
            if hasattr(comment, 'body'):
                relevant_comments.append(comment.body)
                comment_queue.extend(comment.replies)
                read_count +=1
        print(read_count)

    return relevant_comments


def tokenizer(collected_comments):

    #Tokenizes each comment for easier cleaning and sorting
    start = time.time()

    #Cleans comments
    num = 0                                         
    while num < len(collected_comments):
        collected_comments[num] = special_cleaner(collected_comments[num], True)           
        collected_comments[num] = collected_comments[num].strip().lower()     #Lowers text
        collected_comments[num] = collected_comments[num].split()             #Tokenizes text
        collected_comments[num] = list(stop_word_cleaner(collected_comments[num]))  #Removes links and stopwords
        num += 1
    end=time.time()
    # collected_comments = stem_txt(collected_comments)
    print((end-start)/60, "minutes to tokenize", len(collected_comments), "comments")
    return collected_comments


def stop_word_cleaner(tokens):
    stop_words = stopwords.words('english')
    for index in range(0, len(stop_words)):
        stop_words[index] = special_cleaner(stop_words[index], True)
    stop_words = set(stop_words)
    stop_words.remove('not')
    cnt = 0
    while cnt < len(tokens):         
        if "@" in tokens[cnt] or "http" in tokens[cnt] or tokens[cnt] in stop_words:
            tokens.remove(tokens[cnt])
        else:
            cnt+=1
    return set(tokens)

def special_cleaner(str, flag):

    #Cleans a str of alphanumeric characters
    cleaned = ""
    index = 0
    while index < len(str):
        if flag == True and(str[index] == chr(0x2019) or str[index] == chr(0x2018) or str[index] == chr(0x0027) or str[index] == chr(0x0060) or str[index] == chr(0x00B4)):
             cleaned+=" "            
             if((index != 0 and str[index - 1] == 'n') and (index != len(str) - 1 and str[index + 1] == 't')):
                 cleaned+="not "
        elif(str[index]==chr(0x0040)):
            cleaned+=str[index]
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
    with open('trainingcomments.txt', 'w', encoding="utf-8") as file:
        file.write('{')
        for key in collected_comments.keys():
            file.write(",\n")
            file.write(str(key))
            file.write(":")
            file.write(str(collected_comments[key]))
        file.write('}')
    file.close()


def token_to_string(token_list):
    for cnt in range(0, len(token_list)):
        token_string = ""
        for index in range(0, len(token_list[cnt])):
            token_string += str(token_list[cnt][index]) + " "
        token_list[cnt] = token_string.strip()
    return token_list



if __name__ == '__main__':   # Runs main
    main()
