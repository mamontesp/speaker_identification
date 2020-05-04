import sidekit
import numpy as np

# The feature server will be used to load and concatenate cepstral coefficients
# and log-energy from a single HDF5 file

#Once these features loaded, only the first 13 coefficients are retained and post-processed
#Post processing includes the following steps
# 1. Rasta filtering
# 2. Addition of the temporal context first and second derivatives, DCT-PCA or Shifted Delta Cepstra
# 3. Normalization of the features using either Cepstral Mean Variance Normalization (cmvn), Cepstral Mean Substraction (cms) or Short Term Gaussianization (stg)
# 4. Frame selection according to the VAD labels that are loaded, if VAD is included in the data-list

server = sidekit.FeaturesServer(features_extractor = None,
                                feature_filename_structure = "../results/{}.h5",
                                sources = None,
                                dataset_list = ["energy", "cep", "vad"],
                                mask = "[0-12]",
                                feat_norm = "cmnv",
                                global_cmvn = None,
                                dct_pca = False,
                                dct_pca_config = None,
                                sdc = False,
                                sdc_config = None,
                                delta = True,
                                double_delta = True,
                                delta_filter  = None,
                                context = None,
                                traps_dct_nb = None,
                                rasta = True,
                                keep_all_features = True)

features, label = server.load()

ubm = sidekit.Mixture()

ubm.EM_split(features_server=server, 
             feature_list = features,
             distrib_nb = 1024,
             iterations = (1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8),
             num_thread=10,
             save_partial=False,
             ceil_cov=10,
             floor_cov=1e-2
            )

ubm.EM_convert_full(features_server = server, 
                    iterations = 2)

#Train an i-vector extractor
fa = sidekit.FactorAnalyser()
fa.total_variability(stat_server_filename, 
                    ubm,
                    tv_rank,
                    nb_iter=20,
                    min_div=True,
                    tv_init=None,
                    batch_size=300,
                    save_init=False,
                    output_file_name=None,
                    num_thread=1
                    )

#Extract i-vectors in a single process
fa = sidekit.FactorAnalyser()
iv, iv_uncertainty = fa.extract_ivectors(ubm,
                                        stat_server_filename,
                                        prefix='',
                                        batch_size=300,
                                        uncertainty = False,
                                        num_thread =1)