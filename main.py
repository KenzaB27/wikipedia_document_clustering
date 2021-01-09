from clustering.clustering_pipeline import ClusteringPipeline

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
        clust_pipeline.load_processed_data()
    elif args.experiment:
        print("Experiment Mode")
        clust_pipeline.load_raw_data()
        clust_pipeline.preprcessing()
        
    clust_pipeline.clustering(constraint=10)