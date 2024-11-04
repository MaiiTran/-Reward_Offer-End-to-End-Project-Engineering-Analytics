import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
import scipy 
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, dendrogram 
from sklearn.cluster import KMeans 
from sklearn.decomposition import PCA 
import pickle 

df_segmentation = pd.read_csv("customer_segmentation_data.csv", index_col = 0)
scaler = StandardScaler()
segmentation_std = scaler.fit_transform(df_segmentation)

## (PCA) PRINCIPAL COMPONENT ANALYSIS (PCA)
### Rule of thumb: keep 80% of variance 
pca = PCA()
pca.fit(segmentation_std)
pca.explained_variance_ratio_

# plt.figure(figsize = (12,9))
# plt.plot(range(1,5), pca.explained_variance_ratio_.cumsum(), marker = 'o', linestyle = '--')
# plt.title('Explained Variance by Componenets')
# plt.xlabel('Number of Components')
# plt.ylabel('Cumulative Explained Variance')
# plt.show()

pca = PCA(n_components = 3)
pca.fit(segmentation_std)

## PCA Results 
# pca.components_
# df_pca_comp = pd.DataFrame(data = pca.components_, 
#                            columns = df_segmentation.columns.values, 
#                            index = ['Component 1', 'Component 2', 'Component 3'])

# sns.heatmap(df_pca_comp, 
#             vmin = -1, 
#             vmax = 1, 
#             cmap = 'RdBu',
#             annot = True)
# plt.yticks([0,1,2],
#            ['Component 1', 'Component 2', 'Component 3'], 
#            fontsize = 9)
# plt.show()
# Component 1: Income focused; Component 2: Basic identified features such as age and gender; Component 3: Membership time focused 

scores_pca = pca.transform(segmentation_std)


## KMEANS CLUSTERING WITH PCA  -- Use the combined method to get the better result 
wcss = []
for i in range(1,11):
    kmeans_pca = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans_pca.fit(scores_pca)
    wcss.append(kmeans_pca.inertia_)

# # plt.figure(figsize = (10,8))
# # plt.plot(range(1,11), wcss, marker = 'o', linestyle = '--')
# # plt.xlabel('Number of Clusters')
# # plt.ylabel('WCSS')
# # plt.title('K_means with PCA')
# # plt.show()

kmeans_pca = KMeans(n_clusters = 4, init = 'k-means++', random_state = 42)
kmeans_pca.fit(scores_pca)

df_segm_pca_kmeans = pd.concat([df_segmentation.reset_index(drop = True), pd.DataFrame(scores_pca)] , axis = 1)
df_segm_pca_kmeans.columns.values[-3:] = ['Component 1', 'Component 2', 'Component 3']
df_segm_pca_kmeans['Segment K-Means PCA'] = kmeans_pca.labels_

df_segm_pca_kmeans_freq = df_segm_pca_kmeans.groupby(['Segment K-Means PCA']).mean()
print(df_segm_pca_kmeans_freq)

df_segm_pca_kmeans['Legend'] = df_segm_pca_kmeans['Segment K-Means PCA'].map({0: 'lower_income',
                                1: 'older_people',
                                2: 'well_off',
                                3: 'longtime_member'})

x_axis = df_segm_pca_kmeans['Component 2']
y_axis = df_segm_pca_kmeans['Component 1']
plt.figure(figsize = (10,8))
sns.scatterplot(x = x_axis, y = y_axis, hue = df_segm_pca_kmeans['Legend'], palette= ['#E09664','#456672','#FDDF97','#6C4343'])
plt.title('Clusters by PCA Components')
plt.show()
