classified_comments = [[{"a":4}, {"b":0}],[{"c":4}, {"d":0}]]
pos = 0
neg = 0
total = 0
for comment in classified_comments:
    for words in comment:
        for word in words:
            if words[word] == 4:
                pos += 1
            else:
                neg += 1
            total +=1

print("The percentage of positive comments is", pos/total)