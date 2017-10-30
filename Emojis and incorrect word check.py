from textblob import TextBlob

print ("Check of polarity for emojies");
list = [":(",":)",":'(",":D","^_^",":p",":/",";)"]

for i in range(0,8):

    emoji = TextBlob(list[i])
    
    if emoji.sentiment.polarity > 0:
        print (list[i] + ' is positive')
    elif emoji.sentiment.polarity == 0:
        print (list[i] + ' is neutral')
    else:
        print (list[i] + ' is negative')    

print ("Check for incorrect words");

incorrectList=["I havv goood speling!","I slepy yestarday","what's up maan?","Wht boy is theare"];

for i in range(0,4):
    word=TextBlob(incorrectList[i]);
    print ("correct statement for -> "+incorrectList[i]+" is ");
    print(word.correct())
