from clustering.clustering_pipeline import ClusteringPipeline
import matplotlib.pyplot as plt 

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--backup', action='store_true')
    group.add_argument('--experiment', action='store_true')

    clust_pipeline = ClusteringPipeline()
    # Parse and print the results
    args = parser.parse_args()
    if args.backup:
        print("Backup Mode for repeatability check!")
        print("Load Processed data...")
        clust_pipeline.load_processed_data()
    
    elif args.experiment:
        print("Experiment Mode")
        print("Load Raw data...")
        clust_pipeline.load_raw_data()
        print("Launch data preprocessing...")
        clust_pipeline.preprocessing()
        
    print("Launch Graph Creation and Clustering...")
    clusters = clust_pipeline.clustering(constraint=27)

    print("Plot results...")
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    for i, c in enumerate(clusters):
        topics_count = c.get_topics_count()
        axs[i//2, i % 2].bar(topics_count.keys(),
                            topics_count.values(), width=.3, color='g')
        axs[i//2, i % 2].set_title(str(c))
    plt.savefig('data/images/quality_eval.png')
    plt.show()
