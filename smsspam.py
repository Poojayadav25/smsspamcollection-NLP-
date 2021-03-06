import pandas as pd
messages=pd.read_csv('smsspamcollection\SMSSpamCollection', sep='\t', names=['label','message'])

import re
import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

corpus=[]
for i in range(0, len(messages)):
    review=re.sub('[^a-zA-Z]',' ',messages['message'][i])
    review=review.lower()
    review=review.split()
    
    review=[ps.stem(word) for word in review if not word in stopwords.words('english')]
    review=' '.join(review)
    corpus.append(review)
    
    
## creating bag of words
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000)
x=cv.fit_transform(corpus).toarray()

y=pd.get_dummies(messages['label'])
y=y.iloc[:,1].values

#train test splitfrom sklearn.metrics import accuracy_score

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x ,y,test_size=0.20,random_state=0)

#training the model
from sklearn.naive_bayes import MultinomialNB
spam_detect_model=MultinomialNB().fit(x_train,y_train)

y_pred=spam_detect_model.predict(x_test)

from sklearn.metrics import confusion_matrix
comfusion_m=confusion_matrix(y_test,y_pred)


from sklearn.metrics import accuracy_score
accuracy=accuracy_score(y_test,y_pred)

