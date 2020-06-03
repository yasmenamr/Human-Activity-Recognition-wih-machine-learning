import os
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from datetime import datetime
from sklearn.metrics import f1_score
import joblib
import pandas as pd
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,VotingClassifier
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB,BernoulliNB



this_file_path= os.path.abspath(__file__)
dir_path=os.path.dirname(this_file_path)
log_path=os.path.join(dir_path,'log.csv')
#or
log_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'log.csv')
pickles_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'pickles')

train_PATH=os.path.dirname(os.path.abspath(__file__))

train_df = pd.read_csv(os.path.join(train_PATH, os.path.join("data", "train.csv")),index_col=False)
test_df = pd.read_csv(os.path.join(train_PATH, os.path.join("data", "test.csv")),index_col=False)

if not os.path.exists(pickles_path):
    os.mkdir(pickles_path)



# pre proccessig
X_train = train_df.drop(['Activity', 'subject'], axis=1)
Y_train= train_df['Activity']
X_test = test_df.drop(['Activity', 'subject'], axis=1)
Y_test = test_df['Activity']
scaler = StandardScaler()





def train(clf=LogisticRegression(random_state = 0)):

    #train the classifier
    pipe = Pipeline([
        ("scaling", scaler),
        ("classification", clf)
    ])

    pipe.fit(X_train,Y_train)
    y_pred=pipe.predict(X_test)
    f1_current= f1_score(Y_test,y_pred,average='macro')
    print(f1_current)

    #current time stamp
    timestamp= datetime.now().isoformat()

    clf_name=clf.__class__.__name__

    with open(log_path,'a+') as file:
        line ="{},{},{}".format(clf_name,f1_current,timestamp)
        file.write(line)



        clf_path=os.path.join(pickles_path,'clf.pkl')
        joblib.dump(pipe ,clf_path,compress=True)
def load_clf():

    clf_path = os.path.join(pickles_path, 'clf.pkl')

    if os.path.exists(clf_path):
            return  joblib.load(clf_path)
    else:
        return None




Classifiers=[DecisionTreeClassifier(),RandomForestClassifier(n_estimators=200),
               GradientBoostingClassifier(n_estimators=200),
               SVC(kernel='rbf', random_state = 0), LogisticRegression(random_state = 0),
               KNeighborsClassifier(n_neighbors = 10),GaussianNB(),
               BernoulliNB(),
               VotingClassifier(estimators=[('lr', LogisticRegression(multi_class='multinomial', random_state=1)),
                                            ('rf', RandomForestClassifier(n_estimators=200, random_state=1)),
                                            ('gnb', SVC(kernel ='rbf', random_state = 0,probability=True))],
                                voting='soft'
               )
             ]


if __name__=='__main__':
    train(clf=Classifiers[8])
    clf=load_clf()
    print(type(clf))



