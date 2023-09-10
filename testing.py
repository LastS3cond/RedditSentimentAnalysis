from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import csv
import time


def retrieve_from_csv(filename):
     file = open(filename, encoding="utf8")
     csvreader = csv.reader(file)
     for row in csvreader:
        return row[0] + "" + row[5]

    #  header =[]
    #  header = next(csvreader)
    #  rows = []
    #  for row in csvreader:
    #      rows.append(row)
    #  file.close()
    #  return list(zip(*rows))

# def tokenizer(collected_comments):

#     #Tokenizes each comment for easier cleaning and sorting

#     #Cleans comments
#     num = 0                                         
#     while num < len(collected_comments):
#         collected_comments[num] = special_cleaner(collected_comments[num], True)           
#         collected_comments[num] = collected_comments[num].strip().lower()     #Lowers text
#         collected_comments[num] = collected_comments[num].split()             #Tokenizes text
#         collected_comments[num] = stop_word_cleaner(collected_comments[num])  #Removes links and stopwords
#         num += 1
#     collected_comments = stem_txt(collected_comments)
#     return collected_comments


# def stop_word_cleaner(tokens):
#     stop_words = stopwords.words('english')
#     for index in range(0, len(stop_words)):
#         stop_words[index] = special_cleaner(stop_words[index], False)
#     stop_words = set(stop_words)
#     stop_words.remove('not')
#     cnt = 0
#     while cnt < len(tokens):         
#         if "https" in tokens[cnt] or tokens[cnt] in stop_words:
#             tokens.remove(tokens[cnt])
#         else:
#             cnt+=1
#     return tokens


# def special_cleaner(str, bool):

#     #Cleans a str of alphanumeric characters
#     cleaned = ""
#     index = 0
#     while index < len(str):
#         if bool == True and(str[index] == chr(0x2019) or str[index] == chr(0x2018) or str[index] == chr(0x0027) or str[index] == chr(0x0060) or str[index] == chr(0x00B4)):
#             cleaned+=" "            
#             if((index != 0 and str[index - 1] == 'n') and (index != len(str) - 1 and str[index + 1] == 't')):
#                 cleaned+="not "
#         elif str[index].isalnum() or str[index].isspace():
#             cleaned+=str[index]
#         index+=1
#     return cleaned



# def stem_txt(list_comments):
#     ss = SnowballStemmer('english')
#     for index in range(0, len(list_comments)):
#         str = " "
#         for w in list_comments[index]:
#             str+=ss.stem(w) + " "
#         list_comments[index] = str.split()
#     return list_comments


# def token_to_string(token_list):
#     for cnt in range(0, len(token_list)):
#         token_string = ""
#         for index in range(0, len(token_list[cnt])):
#             token_string += str(token_list[cnt][index]) + " "
#         token_list[cnt] = token_string.strip()
#     return token_list

# def save_to_file(collected_comments):

#     #Saves each comment into a file for proof of concept, and times it.
#     with open('trainingcomments.txt', 'w', encoding="utf-8") as file:
#         file.write('{')
#         for key in collected_comments.keys():
#             file.write(",\n")
#             file.write(str(key))
#             file.write(":")
#             file.write(str(collected_comments[key]))
#         file.write('}')
#     file.close()


classified_comments =[[{'mother': '4'}, {'potenti': '4'}, {'father': '0'}, {'not': '4'}, {'know': '4'}, {'parent': '4'}, {'mean': '4'}, {'children': '4'}, {'creat': '4'}, {'die': '4'}], [{'pretti': '4'}, {'clear': '4'}, {'peopl': '4'}, {'want': '4'}, {'like': '4'}, {'get': '4'}, {'12': '0'}, {'year': '4'}, {'old': '4'}, {'rape': '4'}, {'victm': '4'}, {'miscarriagesuffer': '4'}, {'lock': '4'}, {'cage': '4'}, {'life': '4'}, {'even': '4'}, {'execut': '4'}, {'state': '4'}, {'evil': '4'}, {'shit': '4'}, {'rape': '4'}, {'apologist': '4'}, {'downvot': '4'}], [{'delet': '4'}], [{'extrem': '4'}, {'minor': '4'}, {'case': '4'}, {'come': '4'}, {'abort': '4'}, {'argu': '4'}, {'ban': '4'}, {'gun': '4'}, {'mass': '4'}, {'shoot': '4'}], [{'not': '4'}, {'execut': '4'}, {'child': '4'}, {'due': '4'}, {'crime': '4'}, {'father': '0'}], [{'sex': '4'}, {'ed': '4'}, {'teach': '4'}, {'learn': '4'}, {'life': '4'}, {'creat': '4'}, {'ie': '4'}, {'sperm': '4'}, {'egg': '4'}, {'combin': '4'}, {'find': '0'}, {'best': '4'}, {'way': '4'}, {'prevent': '4'}, {'abstin': '4'}], [{'expect': '4'}, {'known': '4'}, {'risk': '4'}, {'action': '4'}, {'two': '4'}, {'differ': '0'}, {'thing': '4'}, {'still': '4'}, {'boil': '4'}, {'consent': '4'}, {'gambl': '4'}, {'not': '4'}, {'lose': '4'}, {'mental': '4'}]]
pos = 0 
neg = 0
total = 0
for comment in classified_comments:
    print(comment)
    for words in comment:
        print(words)
        for word in words:
            print(word, words[word])
            if words[word] == '4':
                pos += 1
            else:
                neg += 1
            total +=1
print(pos)
print(neg)
print("The percentage of positivity is", pos/total)


 