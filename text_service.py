import numpy as np
import pandas as pd
import ftfy
from functools import partial
import hdbscan
import umap
from sentence_transformers import SentenceTransformer
from tqdm.notebook import trange
from hyperopt import fmin, tpe, hp, STATUS_OK, space_eval, Trials


class TextService():

    def __init__(self):
        self.model_st1 = SentenceTransformer('sentence-transformers/LaBSE')
        self.model_st2 = SentenceTransformer('clip-ViT-B-32')
        self.model_st3 = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')
        self.model_st3.max_seq_length = 512


    def embed(self, model, sentences):
        embeddings = model.encode(sentences, show_progress_bar=True)
        return embeddings


    def generate_clusters(self, message_embeddings, n_neighbors, n_components, 
    min_cluster_size,min_samples = None,random_state = None):
        umap_embeddings = (umap.UMAP(n_neighbors = n_neighbors,
        n_components = n_components,metric = 'cosine',
        random_state=random_state).fit_transform(message_embeddings))
        clusters = hdbscan.HDBSCAN(min_cluster_size = min_cluster_size,
        min_samples = min_samples,metric='euclidean',gen_min_span_tree=True,
                             cluster_selection_method='eom').fit(umap_embeddings)
        return clusters


    def score_clusters(self, clusters, prob_threshold = 0.05):
        cluster_labels = clusters.labels_
        label_count = len(np.unique(cluster_labels))
        total_num = len(clusters.labels_)
        cost = (np.count_nonzero(clusters.probabilities_ < prob_threshold)/total_num)
        return label_count, cost


    def objective(self, params, embeddings, label_lower, label_upper):
        clusters = self.generate_clusters(embeddings, 
                                 n_neighbors = params['n_neighbors'], 
                                 n_components = params['n_components'], 
                                 min_cluster_size = params['min_cluster_size'],
                                 random_state = params['random_state'])   
        label_count, cost = self.score_clusters(clusters, prob_threshold = 0.05)
        if (label_count < label_lower) | (label_count > label_upper):
            penalty = 0.15 
        else:
            penalty = 0   
        loss = cost + penalty
        return {'loss': loss, 'label_count': label_count, 'status': STATUS_OK}


    def bayesian_search(self, embeddings, space, label_lower, label_upper, max_evals=100):
        trials = Trials()
        fmin_objective = partial(self.objective, 
                             embeddings=embeddings, 
                             label_lower=label_lower,
                             label_upper=label_upper)
        best = fmin(fmin_objective, 
                space = space, 
                algo=tpe.suggest,
                max_evals=max_evals, 
                trials=trials)
        best_params = space_eval(space, best)
        best_loss = trials.best_trial['result']['loss']
        print ('best:')
        print (best_params)
        print (f"number of clusters: {trials.best_trial['result']['label_count']}")
        print (f"loss: {trials.best_trial['result']['loss']}")
        best_clusters = self.generate_clusters(embeddings, 
                                      n_neighbors = best_params['n_neighbors'], 
                                      n_components = best_params['n_components'], 
                                      min_cluster_size = best_params['min_cluster_size'],
                                      random_state = best_params['random_state'])
        return best_params, best_clusters, trials, best_loss
  

    def plot_clusters(self, embeddings, clusters, n_neighbors=15, min_dist=0.1):
        umap_data = umap.UMAP(n_neighbors=n_neighbors, 
                          n_components=2, 
                          min_dist = min_dist,  
                          #metric='cosine',
                          random_state=42).fit_transform(embeddings)
        result = pd.DataFrame(umap_data, columns=['x', 'y'])
        result['labels'] = clusters.labels_
        return (result)


    def processText(self, data):
        data_short = []
        data_long=[]
        for x in data:
            data_long.append(str(x))
            data_short.append(str(x)[:75])
        embeddings_st1 = self.embed(self.model_st1, data_long)
        embeddings_st2 = self.embed(self.model_st2, data_short)
        embeddings_st3 = self.embed(self.model_st3, data_long)
        print('Generated All Embeddings Successfully')

        hspace = {
            "n_neighbors": hp.choice('n_neighbors', range(3,16)),
            "n_components": hp.choice('n_components', range(3,16)),
            "min_cluster_size": hp.choice('min_cluster_size', range(2,16)),
            "random_state": 42
            }

        label_lower = 30
        label_upper = 100
        max_evals = 100

        best_params_st1, best_clusters_st1, trials_st1, loss1 = self.bayesian_search(embeddings_st1, 
                                                                 space=hspace, 
                                                                 label_lower=label_lower, 
                                                                 label_upper=label_upper, 
                                                                 max_evals=max_evals)
        print('Bayesian Search for ST1 Successful')
        best_params_st2, best_clusters_st2, trials_st2, loss2 = self.bayesian_search(embeddings_st2, 
                                                                 space=hspace, 
                                                                 label_lower=label_lower, 
                                                                 label_upper=label_upper, 
                                                                 max_evals=max_evals)
        print('Bayesian Search for ST2 Successful')
        best_params_st3, best_clusters_st3, trials_st3, loss3 = self.bayesian_search(embeddings_st3, 
                                                                 space=hspace, 
                                                                 label_lower=label_lower, 
                                                                 label_upper=label_upper, 
                                                                 max_evals=max_evals)
        print('Bayesian Search for ST3 Successful')
        print('ALL Bayesian Search Completed')   

        losses = [loss1, loss2, loss3]
        min_loss = min(losses)    
        i = losses.index(min_loss)
        embeddings = [embeddings_st1, embeddings_st2, embeddings_st3]
        best_clusters = [best_clusters_st1, best_clusters_st2, best_clusters_st3]
        emb = embeddings[i]
        bc = best_clusters[i]
        x = self.plot_clusters(emb, bc)
        print('Plotting Completed')
        
        x['docs'] = data
        print('Dataframe of Results Created')

        #x.to_csv('output.csv')
        #x.to_excel('output.xlsx')

        return x.to_dict(orient="records")

'''   
if __name__ == "__main__":
    df = pd.read_csv('genz_twitter.csv')
    data = df['clean'].tolist()
    tps = TextService()
    preds = tps.processText(data)
    print(preds)
    '''