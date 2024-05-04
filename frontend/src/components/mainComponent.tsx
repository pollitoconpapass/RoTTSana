import { Button, Paper, Typography, Snackbar } from '@mui/material';
import React, { useState } from 'react';

const MainComponent: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [audioSrc, setAudioSrc] = useState<Blob>();
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [errorSnackbarOpen, setErrorSnackbarOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const startRecording = () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
     .then(streamData => {
        setStream(streamData);
        const recorder = new MediaRecorder(streamData);
        setMediaRecorder(recorder);

        recorder.addEventListener('dataavailable', (event) => {
          if (event.data.size > 0) {
            uploadRecording(event.data);
          }
        });

        recorder.start();
        setIsRecording(true);
      })
     .catch(error => {
        console.error('Error:', error);
      });
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
      setIsRecording(false);
    }
  };

  const uploadRecording = (blob: Blob) => {
    const formData = new FormData();
    formData.append('audio_file', blob, 'recorded_audio.webm');

    fetch('http://localhost:8085/stt-general/', {
      method: 'POST',
      body: formData
    })
   .then(response => response.text())
   .then(data => {
      setTranscription(data);
      sendToTranslationEndpoint(data);
    })
   .catch(error => {
      console.error('Error:', error);
    });
  };

  const sendToTranslationEndpoint = (text: string) => {
    fetch('http://localhost:8085/translate-free/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: text
      })
    })
   .then(response => response.text())
   .then(data => {
      setTranslatedText(data);
      generateAudioFromTranslatedText(data);
    })
   .catch(error => {
      console.error('Error:', error);
    });
  };

  const generateAudioFromTranslatedText = (text: string) => {
    fetch('http://localhost:8085/tts-general/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: text
      })
    })
   .then(response => response.arrayBuffer())
   .then(async (audioMP3) => {
      const blob = new Blob([audioMP3], { type: 'audio/wav' });
      setAudioSrc(blob);
    })
   .catch(error => {
      setErrorMessage('Error generating audio from translated text');
      setErrorSnackbarOpen(true);
      console.error('Error:', error);
    });
  };

  return (
    <>
      <Snackbar
        open={errorSnackbarOpen}
        autoHideDuration={6000}
        onClose={() => setErrorSnackbarOpen(false)}
        message={errorMessage}
      />
      <title>Voice Translator</title>
      <h1 style={{ color: '#192c80' }}>RoTTSana</h1>
      <br />
      <h3 style={{ color: '#120707' }}>Habla / Rimay </h3>

      <Button variant="contained" color="primary" onClick={startRecording} disabled={isRecording}>
        Start
      </Button>
      <Button variant="contained" color="secondary" onClick={stopRecording} disabled={!isRecording}>
        Stop 
      </Button>
      <br />
      <br />
      <br />

      {transcription && (
        <Paper elevation={3} variant="outlined" style={{ borderRadius: '20px', padding: '20px', marginBottom: '20px', backgroundColor: '#a886d1', color: '#120707' }}>
          <Typography variant="h6" color={'#120707'}>TRANSCRIPCION / NISQAMANTA</Typography>
          <Typography variant="body1">{transcription}</Typography>
        </Paper>
      )}

      <br />
      <br />
      <br />

      {translatedText && (
        <Paper elevation={3} variant="outlined" style={{ borderRadius: '20px', padding: '20px', marginBottom: '20px', backgroundColor: '#a886d1', color: '#120707' }}>
          <Typography variant="h6" color={'#120707'}>TRADUCCION / TIKRAY</Typography>
          <Typography variant="body1">{translatedText}</Typography>
        </Paper>
      )}

      <br />
      {audioSrc && (
        <audio controls autoPlay src={URL.createObjectURL(audioSrc)} />
      )}

      <footer style={{ position: 'absolute', bottom: 0, left: 0, right: 0, backgroundColor: '#192c80', color: '#ffffff', padding: '20px', textAlign: 'center' }}>
        <Typography variant="body1">
          © 2024 Adina | Privacy Policy | Contact Us
        </Typography>
      </footer>
    </>
  );
};

export default MainComponent;