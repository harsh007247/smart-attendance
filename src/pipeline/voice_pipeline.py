from resemblyzer import VoiceEncoder,preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder

def get_voice_embedding(audio_bytes):
    try:
        encoder=load_voice_encoder()
        audio , sr=librosa.load(io.BytesIO(audio_bytes),sr=16000)
        wav=preprocess_wav(audio)
        embedding=encoder.embed_utterance(wav)
        return embedding
    except Exception as e:
        st.error("Voice Recog Error")
        return None


def identify_speaker(new_embedding,candidate_dict,threshold=0.65):
    if not new_embedding or not candidate_dict:
        return None,0

    best_sid=None
    best_score= -1.0

    for sid,stored_embedding in candidate_dict.items():
        if stored_embedding:
            similarity=np.dot(new_embedding,stored_embedding)
            if similarity>best_score:
                best_score=similarity
                best_sid=sid
    if best_score>=threshold:
        return best_sid,best_score

    return None,best_score

def process_bulk_audio(audio_bytes,candidate_dict,threshold=0.65):
    try:
        encoder=load_voice_encoder()

        audio , sr= librosa.load(io.BytesIO(audio_bytes),sr=16000)
        segments=librosa.effects.split(audio,top_db=30)#top_db means 30db se uper i voices ko detect kr lega means kmm aawaz ko bhi pkd lega agr high kr dege toh sirf jyada tej voices ko kr paagga    
        identified_result={}

        for start,end in segments:
            if (end-start) < sr * 0.5:
                continue
            segment_audio=audio[start:end]
            wav=preprocess_wav(segment_audio)
            embediding=encoder.embed_utterance(wav)

            sid, score = identify_speaker(embediding,candidate_dict,threshold)

            if sid:
                if sid not in identify_speaker or score> identified_result[sid]:
                    identified_result[sid]= score

        return identified_result
    except Exception as e:
        st.error("Bulk Progress error")
        return {}
