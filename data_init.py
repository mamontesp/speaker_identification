import os
import yaml
import shutil
import sidekit
import numpy as np
from tqdm import tqdm
from utils import convert_wav, safe_makedir, parse_yaml

class DataInitializer():
    """
    To build speaker verification model, one needs speech data from each speaker
    that is to be known by the system. The set of known speakers are in speaker
    recognition known as the (enrollment speakers), and a speaker is enrolled
    into the system when enrollment data from the speaker is processed to build
    its model.
    After the enrollment process, the performance of the speaker verification
    system can be evaluated using test data, which in an open set scenario, will
    consist of data from speakers in and outside the enrollment set.
    The set of all speakers involved in testing the system will be referred to
    as the test speakers.

    This class is for preprocessing and structure the preprocessed data
    into h5 files that will be used later for training and evaluating our models
    NOTE:All outputs of this script can be found in the directory self.task_dir
    """

    def __init__(self, conf_path):
        """
        This method parses the YAML configuration fiel which can be used for
        initializaing the member variables 
        Args: 
            conf_path (string): path of YAML configuration file
        """

        #Location of output files
        self.conf = parse_yaml(conf_path)
        self.task_dir = os.path.join(self.conf['outpath'], "task")
        #location of audio files
        self.audio_dir = os.path.join(self.conf['outpath'], "audio")
        #location of all the audio data
        self.data_dir = os.path.join(self.audio_dir, "data")
        #location of just the enrollment audio data
        self.enroll_dir = os.path.join(self.audio_dir, "enroll")
        #location of just the test audio data
        self.test_dir = os.path.join(self.audio_dir, "test")

    def preprocess_audio(self): 
        """
        Copy the crowdsourced-colombian spanish female recordings
        The whole audio data will be in 'data' directory, the enrolled
        data only will be in 'enroll', and the test data will be in 'test'
        """

        #remove the data directory if exists
        if os.path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)
        #iterate over speakers
        speakers = sorted(os.listdir(self.conf['inpath']))
        print(speakers)
        for sp in tqdm(speakers, desc="Converting Audio"):
            speaker_path = os.path.join(self.conf['inpath'], sp)
            if(os.path.isdir(speaker_path) == False):
                continue
            wav_filenames = os.listdir(speaker_path)
            for wav in wav_filenames:
                inwav = os.path.join(speaker_path, wav)
                outwav = os.path.join(self.data_dir, wav)
                convert_wav(inwav,
                            outwav,
                            no_channels = self.conf['no_channels'],
                            sampling_rate = self.conf['sampling_rate'],
                            bit_precision = self.conf['bit_precision'],
                            showWarning=True)
        
        #remove the enroll directory if exists
        if os.path.exists(self.enroll_dir):
            shutil.rmtree(self.enroll_dir)
        #remove the test directory if exists
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

        #create audio/enroll directory
        safe_makedir(self.enroll_dir)
        #create audio/test directory
        safe_makedir(self.test_dir)

        #parse num of sessions for configuration
        enroll_sessions = self.conf['enroll_sessions']
        test_sessions = self.conf['test_sessions']

        assert enroll_sessions + test_sessions <= 10,\
            "The summation of all sessions must be less than or equal 10"
        #iterate over all preprocessed waves
        wav_filenames = os.listdir(self.data_dir)
        for wav in tqdm(wav_filenames, desc="Copying enroll/test waves"):
            _, sess, _ = wav.split(".")
            inwav = os.path.join(self.data_dir, wav)
            if int(sess) <= enroll_sessions:
                outwav = os.path.join(self.enroll_dir, wav)
                shutil.copyfile(inwav, outwav)
            elif int(sess) <=enroll_sessions + test_sessions:
                outwav = os.path.join(self.test_dir, wav)
                shutil.copyfile(inwav, outwav)
    
    def create_id_map(self, group):
        """
        Idmap are used to store two lists of strings and to mapt them
        """
        assert group in ["enroll", "test"],\
            "Invalid group name!! Choose either 'enroll', 'test'"
        # Make enrollment (IdMap) file list
        group_dir = os.path.join(self.audio_dir, group)
        group_files = sorted(os.listdir(group_dir))
        #list of model IDs
        group_models = [files.split('.')[0] for files in group_files]
        #list of audio segments IDs
        group_segments = [group+"/"+f for f in group_files]

        #Generate idMap
        group_idmap =sidekit.IdMap()
        group_idmap.leftids = np.asarray(group_models)
        group_idmap.rightids = np.asarray(group_segments)
        group_idmap.start = np.empty(group_idmap.rightids.shape, '|O')
        group_idmap.stop = np.empty(group_idmap.rightids.shape, '|O')

        if group_idmap.validate():
            group_idmap.write(os.path.join(self.task_dir, group+'_idmap.h5'))
            #Generate tv_idmap and plda_idmap as well
            if group == "enroll":
                group_idmap.write(os.path.join(self.task_dir, 'tv_idmap.h5'))
                group_idmap.write(os.path.join(self.task_dir, 'plda_idmap.h5'))
        else:
            raise RuntimeError('Problems with creating idMap file')
    
    def create_test_trials(self):
        """
        Ndx objects store trials index information i.e., combination of 
        model and segment IDs that should be evakuated by the system which
        will produce a score for those trials.
        """
        #Make list of test segments
        test_data_dir = os.path.join(self.audio_dir, "test") #test data directory
        test_files = sorted(os.listdir(test_data_dir))
        test_files = ["test/"+f for f in test_files]

        #Make lists for trial definitions, and write to file
        test_models = []
        test_segments = []
        test_labels = []
        
        #Get enrolled speakers
        enrolled_speakers =set([])
        for filename in os.listdir(os.path.join(self.audio_dir, "enroll")):
            enrolled_speakers.add(filename.split(".")[0])
        enrolled_speakers = sorted(enrolled_speakers)

        for model in tqdm(enrolled_speakers, desc="Creating Test Cases"):
            for segment in sorted(test_files):
                test_model = segment.split(".")[0].split("/")[-1]
                test_models.append(model)
                test_segments.append(segment)
                #Compare gender and speaker ID for each test file
                if test_model == model:
                    test_labels.append('target')
                else:
                    test_labels.append('nontarget')
        with open(os.path.join(self.task_dir, "test_trials.txt"), "w") as fh:
            for i in range(len(test_models)):
                fh.write(test_models[i]+' '+test_segments[i]+' '+test_labels[i]+'\n')

    def create_ndx(self):
        """
        Key are used to store information about which trial is a target trial
        and which one is a non-target (or impostor) trial.
        """
        key = sidekit.Key.read_txt(os.path.join(self.task_dir, "test_trials.txt"))
        ndx = key.to_ndx()
        if ndx.validate():
            ndx.write(os.path.join(self.task_dir, 'test_ndx.h5'))
        else:
            raise RuntimeError('Problems with creating Ndx file')

    def create_structure_data(self):
        """
        """
        self.preprocess_audio()
        self.create_id_map("enroll")
        self.create_id_map("test")
        self.create_test_trials()
        self.create_ndx()
        print("Done!")



if __name__ == "__main__":
    conf_filename = "conf.yaml"
    init = DataInitializer(conf_filename)
    init.create_structure_data()

