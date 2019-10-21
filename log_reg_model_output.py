import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("sb_passes.csv")

#remove non normal pass types, GK drop kicks, throws and no-touch passes
open_play_df = df[(df["type"]=="Normal")&
                  (df["body_part"]!="Drop Kick")&
                  (df["body_part"]!="Keeper Arm")&
                  (df["body_part"]!="No Touch")]

#drop Nan cols & player info
open_play_df = open_play_df.dropna()
open_play_df = open_play_df[['start_x', 'start_y', 'end_x', 'end_y', 'outcome',
                             'length', 'angle', 'height', 'backheel', 'deflected',
                             'cross', 'cut_back', 'switch', 'body_part', 'technique',
                             'pressure']]

#format columns 
categorical_cols = ['height','body_part','technique']
scale_cols  = ['length','angle','start_x','start_y','end_x','end_y']

#normalise numerical cols
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

for col in scale_cols:
    open_play_df['{}'.format(col)] = scaler.fit_transform(open_play_df['{}'.format(col)].values.reshape(-1,1))
    
#encode dummy vars
open_play_df = pd.get_dummies(data=open_play_df, columns=categorical_cols)

#build logistic regression model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

log_r = LogisticRegression()

X = open_play_df[['start_x', 'start_y', 'end_x', 'end_y','length', 'angle',
                  'backheel', 'deflected', 'cross', 'cut_back', 'switch', 'pressure',
                  'height_Ground Pass', 'height_High Pass', 'height_Low Pass',
                  'body_part_Head', 'body_part_Left Foot', 'body_part_Other',
                  'body_part_Right Foot', 'technique_Normal', 'technique_Through Ball']]

y = open_play_df.outcome.values

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=12)

log_r.fit(X_train,y_train)

#accuracy
print("% passes predicted correctly: {:.1f}%".format(log_r.score(X_test,y_test)*100))

print("Dataset pass accuracy: {:.1f}%".format((sum(open_play_df.outcome.tolist())/len(open_play_df.index))*100))

prediction = log_r.predict(X_test)
from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, prediction)
print(confusion_matrix)

from sklearn import metrics
y_pred_proba = log_r.predict_proba(X_test)[::,1]

fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)

#plot ROC Curve
plt.plot(fpr,tpr,label="AUC: {:.3f}".format(auc))
plt.title("ROC Curve - xP model")
plt.xlabel("False Positive rate")
plt.ylabel("True Positive rate")
plt.legend(loc=4)
plt.plot([0, 1], [0, 1], color='black', lw=1, linestyle='-')
plt.savefig('roc_curve_sb_passing.jpg',dpi=400,bbox_inches='tight', edgecolor='none')
plt.show()


import statsmodels.api as sm

logistic_regression = sm.Logit(y,X)
result = logistic_regression.fit()
print(result.summary())


#next steps:
#variable selection
#test on 2019/20 WSL data, player evaluation






