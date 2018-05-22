""" Tools to convert various dataformats into the format basic_srl internally uses """

import logging
import os

from .formats import read_corpus  

def concatenate_corpora(resource_manager, corpora_names_in, corpus_name_out):
    """ Concantenates each sentence and annotation files for a list of names. Result are sentence and annotation
    files that contain all data from the input corpora

    Args:
        corpora_names_in (list): List of corpora name that will be concatenated
        corpus_name_out: The corpus that will be generated by concatenating data from corpora_names_in 
    """

    output_sentence_file = resource_manager.get_sentences_file(corpus_name_out)    
    output_annotation_file = resource_manager.get_frame_annotations_file(corpus_name_out)

    if os.path.isfile(output_sentence_file) and os.path.isfile(output_annotation_file):
        logging.info('Corpus in [%s] and [%s] already exists, skip concatenation!', output_sentence_file, output_annotation_file)        
        return 
        
    logging.info('Concatenating %s to [%s] and [%s]', corpora_names_in, output_sentence_file, output_annotation_file)

    sentence_id = 0      
    with open(output_annotation_file, 'w') as af, open(output_sentence_file, 'w') as sf:
        for corpus in corpora_names_in:
            in_frame_annotations_file = resource_manager.get_frame_annotations_file(corpus)
            in_sentence_file = resource_manager.get_sentences_file(corpus)
            sentences, annotations = read_corpus(in_sentence_file, in_frame_annotations_file)

            logging.info('Appending [%s]', corpus)

            for sentence_entry, frame_entries in zip(sentences, annotations):

                sf.write(sentence_entry.to_line())
                sf.write('\n')

                for frame_entry in frame_entries:
                    frame_entry.sentence_number = sentence_id
                    af.write(frame_entry.to_line())
                    af.write('\n')

                sentence_id += 1            



