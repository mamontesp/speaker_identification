import sidekit
import numpy as np
import os

group = "test"
output_dir="../results"
audio_dir=output_dir+"/audio"
feat_dir=output_dir+"/feat"

in_files = os.listdir(os.path.join(audio_dir, group))
feat_dir = os.path.join(feat_dir, group)

extractor = sidekit.FeaturesExtractor(audio_filename_structure=os.path.join(audio_dir, group, "{}"),
                                      feature_filename_structure=os.path.join(feat_dir, "{}.h5"),
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

#Prepare file lists
#show_list: list if IDs of the show to process
show_list = np.unique(np.hstack([in_files]))

#channel_list: list of channel indices corresponding to each show
channel_list = np.zeros_like(show_list, dtype=int)

# save the features in feat_dir where the resulting-files parameters
# are always concatenated in the following order:
# (energy, fb, cep, bnf, vad_label).
# SKIPPED: list to track faulty-files
SKIPPED = []
for show, channel in zip(show_list, channel_list):
    try:
        extractor.save(show, channel)
    except RuntimeError:
        print ("SKIPPED")
        SKIPPED.append(show)
        continue

print("Number of skipped files: "+str(len(SKIPPED)))
for show in SKIPPED:
    print(show)

    