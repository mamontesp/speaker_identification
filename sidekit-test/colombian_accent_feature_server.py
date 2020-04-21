import sidekit
import numpy as np

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
                                