import sidekit
import numpy as np
from os import listdir
from os.path import isfile, join

mypath = '../dataset/crowdsourced-colombian-spanish/es_co_female'
onlyfiles_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles_without_ext_list= []
for f in onlyfiles_list:
    onlyfiles_without_ext_list.append(f.split('.')[0])

print(onlyfiles_without_ext_list)
channel_list = np.zeros_like(onlyfiles_without_ext_list, dtype = int)

extractor = sidekit.FeaturesExtractor(audio_filename_structure="../dataset/crowdsourced-colombian-spanish/es_co_female/{}.wav",
                                      feature_filename_structure="../results/crowdsourced-colombian-spanish/es_co_female/{}.h5",
                                      sampling_frequency=None, 
                                      lower_frequency=200,
                                      higher_frequency=3800,
                                      filter_bank="log",
                                      filter_bank_size=24,
                                      window_size=0.025,
                                      shift=0.01,
                                      ceps_number=20,
                                      vad="snr",
                                      snr=40,
                                      pre_emphasis=0.97,
                                      save_param=["vad", "energy", "cep", "fb"],
                                      keep_all_features=True)



extractor.save_list(show_list=onlyfiles_without_ext_list,
                    channel_list=channel_list,
                    num_thread=10)