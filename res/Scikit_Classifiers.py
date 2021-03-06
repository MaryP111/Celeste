import numpy as np 
import pandas as pd 
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import f1_score


df=pd.read_csv('dataset4.csv')
print (df.shape)
print(df.tail())
print(df.isnull().sum())
# print (df.isnull().any()) #find empty columns
# print (df.isnull().any().any()) #check if there is empty value
# with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
print (df.shape)

X=df.iloc[:,0:8] #choose correct columns
y=df.iloc[:,9] #choose correct columns

fold_numbers=5 #constant for kfold

#Information about the dataset
targets=[]
for i in y:
	if (i not in targets):
		targets.append(i)
percentage=[]
times=[]
yList=list(y)
for j in targets:
	percentage.append("%.2f" %(yList.count(j)/len(yList)))
	times.append(yList.count(j))
print ("Targets: ",targets)
print ("Total number of samples: ",len(y))
print ("Samples that belong to each class: ",times)
print ("Percentage of each class: ",percentage)

#Feature extraction:
# pcaExtractor=PCA(n_components=5)
# X=pcaExtractor.fit_transform(X)

# Selecting features
#X=SelectKBest(k=80).fit_transform(X,y)

# Data standarization
sc=StandardScaler()
X=sc.fit_transform(X)

#Data normalization	
# X=preprocessing.scale(X)

#KNN
knnSimpleClf=KNeighborsClassifier(n_neighbors=41)
#k=np.arange(0,80,10)+1
#parameters={'n_neighbors':k}
#clf=GridSearchCV(knnSimpleClf,parameters,cv=5)
#clf.fit(X,y)
#print (clf.best_params_)
print ('Knn scoring: ',cross_val_score(knnSimpleClf,X,y,cv=fold_numbers).sum()/fold_numbers)

svm=SVC()
# Co=(0.01,1.0,10.0,100.0)
# kerns=('linear','rbf','poly')
# gammas=(0.01,1.0,10.0,100.0)
# params={'C':Co,'kernel':kerns,'gamma':gammas}
# clf=GridSearchCV(svm,params,cv=5)
# clf.fit(X,y)
# print (clf.best_params_)
svm=SVC(kernel='rbf',C=10,gamma=0.01)
print ('SVM score: ',cross_val_score(svm,X,y,cv=fold_numbers).sum()/fold_numbers)

#Forest
# criteria=('gini','entropy')
# estimators=np.arange(50,80,10)+1
# params={'criterion':criteria,'n_estimators':estimators}
# forest=RandomForestClassifier()
# clf=GridSearchCV(forest,params,cv=5)
# clf.fit(X,y)
# print (clf.best_params_)
forest=RandomForestClassifier(criterion='gini',n_estimators=51,n_jobs=-1)
print ('Forest scoring: ',cross_val_score(forest,X,y,cv=fold_numbers).sum()/fold_numbers)

#Logistic Regression
# logr=LogisticRegression()
# penalize=('l1','l2',)
# Co=(0.01,1.0,10.0,100.0)
# params={'C':Co,'penalty':penalize}
# clf=GridSearchCV(logr,params,cv=5)
# clf.fit(X,y)
# print (clf.best_params_)
logr=LogisticRegression(penalty='l1',C=1.0)
print ('Logistic scoring: ',cross_val_score(logr,X,y,cv=fold_numbers).sum()/fold_numbers)

#MLP
# learning_rates=(0.001,0.01,0.1)
# hidden_layers=((100,),(500,),(1000,))
# params={'learning_rate_init':learning_rates,'hidden_layer_sizes':hidden_layers}
# multiP=MLPClassifier()
# clf=GridSearchCV(multiP,params,cv=5)
# clf.fit(X,y)
# print (clf.best_params_)
multiP=MLPClassifier(learning_rate_init=0.001,hidden_layer_sizes=(1000,))
print ('MLP scoring: ',cross_val_score(multiP,X,y,cv=fold_numbers).sum()/fold_numbers)

#Naive Bayes
bayesian=GaussianNB()
print ('Bayesian naive scoring: ',cross_val_score(bayesian,X,y,cv=fold_numbers).sum()/fold_numbers)

#Majority wins!
#plurality=VotingClassifier([('knn',knnSimpleClf),('svm',svm),('forest',forest),('regression',logr),('mlp',multiP),('naive',bayesian)],voting='hard',n_jobs=1)
#print ('Plurality: ',cross_val_score(plurality,X,y,cv=fold_numbers).sum()/fold_numbers)

