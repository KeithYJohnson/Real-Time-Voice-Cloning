from pathlib import Path
from synthesizer.inference import Synthesizer
from vocoder import inference
import numpy as np
import os
from ipdb import set_trace as st

class CelebrityTextRequestHandler(object):

    def __init__(self, syn_model_dir="synthesizer/saved_models/logs-pretrained/", low_mem=False, voc_model_fpath="vocoder/saved_models/pretrained/pretrained.pt", pre_trained_embeddings="pre_trained_embeddings"):
        self.celebrity_map = {}

        ## Load the models one by one.
        print("Preparing the synthesizer and the vocoder")
        self.synthesizer = Synthesizer(Path(syn_model_dir).joinpath("taco_pretrained"), low_mem=low_mem)
        inference.load_model(Path(voc_model_fpath))

        self.load_all_embeddings(pre_trained_embeddings)

    def load_all_embeddings(self, pre_trained_embeddings):
        files = os.listdir(pre_trained_embeddings)
        for file_name in files:
            file_name_sanitized = file_name.split(".")[0]
            embedding = np.load(os.path.join(pre_trained_embeddings, file_name))
            self.celebrity_map[file_name_sanitized] = embedding

    def get_embedding_from_celebrity(self, celebrity):
        return self.celebrity_map.get(celebrity, None)

    def call_synth_and_vocoder(self, text, celebrity):
        # The synthesizer works in batch, so you need to put your data in a list or numpy array
        texts = [text]
        embed = self.get_embedding_from_celebrity(celebrity)
        if embed is not None:
            raise ValueError('Celebrity {} not found in mapping!'.format(celebrity))
        embeds = [embed]
        # If you know what the attention layer alignments are, you can retrieve them here by
        # passing return_alignments=True
        specs = self.synthesizer.synthesize_spectrograms(texts, embeds)
        spec = specs[0]
        print("Created the mel spectrogram")
        
        ## Generating the waveform
        print("Synthesizing the waveform:")
        # Synthesizing the waveform is fairly straightforward. Remember that the longer the
        # spectrogram, the more time-efficient the vocoder.
        return inference.infer_waveform(spec)

    def upload_to_s3(generated_wav):
        pass

    def handle(self, text, celebrity):
        print("handle text: {}, celebrity: {}".format(text, celebrity))
        generated_wav = self.call_synth_and_vocoder(text, celebrity)
        self.upload_to_s3(generated_wav)
