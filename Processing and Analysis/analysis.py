import numpy as np
import pandas as pd
from scipy.stats import shapiro, kruskal, norm
import matplotlib.pyplot as plt
from scikit_posthocs import posthoc_conover
import statsmodels.api as sm

def shapiro_kruskal_conover(data):
    features = [ 'emotion', 'we_count', 'past_future', 'F_score', 'toxicity',
                'severe_toxicity', 'identity_attack', 'insult', 'profanity', 'threat', 'inflammatory', 'politeness'] #'communityA', 'politenessA'
    for feature in features:
        data[feature] = 2*(data[feature] - data[feature].min()) / (data[feature].max() - data[feature].min()) - 1
        #print("Feature: ", feature)

        p1 = data.loc[data['platform'] == 'tumblr', feature]
        p2 = data.loc[data['platform'] == 'reddit', feature]
        p3 = data.loc[data['platform'] == 'twitch', feature]
        p4 = data.loc[data['platform'] == '4chan', feature]
        #names = ['tumblr', 'reddit', 'twitch', '4chan']
        #print('Shapiro:')
        for i, platform in enumerate([p1, p2, p3, p4]):
            stat, p = shapiro(platform)
            #print(names[i], stat * 1000 // 10 / 100, p * 1000 // 10 / 100, p > 0.01)

        stat, p = kruskal(p1, p2, p3, p4)
        #print('Kruskal: ' + str(stat * 1000 // 10 / 100) + ',' + str(p))

        conover_results = posthoc_conover(data, val_col=feature, group_col='platform')
        #print(conover_results)


data = pd.read_csv('data.csv')
data['emotion'] =data['positive_emotion'] + data['negative_emotion']
shapiro_kruskal_conover(data)

data['communityA'] = data['emotion'] +data[ 'we_count']+data['past_future']-data['F_score']
data['politenessA'] = data['politeness'] - (data['insult']+data['profanity']+data['threat']+data['toxicity']+data['inflammatory']+data['severe_toxicity'] )
data['communityA'] = (np.array(data['communityA'])-np.mean(data['communityA']))/np.std(data['communityA'])
data['politenessA'] =(np.array(data['politenessA'])- np.mean(data['politenessA']))/np.std(data['politenessA'])

for feature in ['communityA','politenessA']:
    for platform in ['tumblr','reddit','twitch','4chan']:
        sample = data.loc[data['platform'] == platform, feature]
        #print(platform,str(min(sample)), str(np.mean(sample)), str(max(sample)), str(np.std(sample)))
        stat, p = shapiro(sample)
        print(platform, stat * 1000 // 10 / 100, p * 1000 // 10 / 100, p > 0.01)

    p1 = data.loc[data['platform'] == 'tumblr', feature]
    p2 = data.loc[data['platform'] == 'reddit', feature]
    p3 = data.loc[data['platform'] == 'twitch', feature]
    p4 = data.loc[data['platform'] == '4chan', feature]
    stat, p = kruskal(p1, p2, p3, p4)
    print('Kruskal: ' + str(stat * 1000 // 10 / 100) + ',' + str(p))

    conover_results = posthoc_conover(data, val_col=feature, group_col='platform')
    print(conover_results)

Y = data['politenessA'].values.astype('float')
X1 = data['communityA'].values.astype('float')
X2 = [int(data.loc[i, 'platform'] == 'tumblr') for i in range(len(data)) ]
X3 = [int(data.loc[i, 'platform'] == 'twitch') for i in range(len(data)) ]
X4 = [int(data.loc[i, 'platform'] == '4chan') for i in range(len(data)) ]
X5 = np.multiply(X1,X2)
X6 = np.multiply(X1,X3)
X7 = np.multiply(X1,X4)
X = np.column_stack((X1, X2, X3,X4,X5,X6,X7))
X = sm.add_constant(X)
ols_model = sm.OLS(Y, X)
ols_model = ols_model.fit()
resid = ols_model.resid
fitted = ols_model.fittedvalues
plt.scatter(fitted, resid, c='hotpink')
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.show()
print(ols_model.summary())

expected_quantiles = norm.ppf(np.linspace(0.01, 0.99, len(np.sort(resid))))
plt.scatter(expected_quantiles, np.sort(resid), c='hotpink')
plt.xlabel('Theoretical Quantiles')
plt.ylabel('Sample Quantiles')
plt.plot(np.sort(resid), np.sort(resid), color='darkorchid')
plt.show()