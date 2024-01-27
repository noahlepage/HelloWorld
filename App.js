import { useState } from "react";
import { View, StyleSheet, Button } from "react-native";
import { Audio } from "expo-av";

export default function App() {
  const [recording, setRecording] = useState();
  const [permissionResponse, requestPermission] = Audio.usePermissions();

  async function startRecording() {
    try {
      if (permissionResponse.status !== "granted") {
        console.log("Requesting permission...");
        await requestPermission();
      }
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      console.log("Starting recording..");
      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(recording);
      console.log("Recording started");
    } catch (err) {
      console.error("Failed to start recording", err);
    }
  }

  async function stopRecording() {
    console.log("Stopping recording..");
    setRecording(undefined);
    await recording.stopAndUnloadAsync();
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: false,
    });
    const uri = recording.getURI();
    console.log("Recording stopped and stored at", uri);
  }

// Big-daddy-js
const backendAddress = 'localhost';
const socket = new WebSocket(`ws://${backendAddress}:8765`);

// Handle connection open
socket.addEventListener('open', (event) => {
    console.log('WebSocket connection opened');

    // Now that the connection is open, you can start sending audio data if needed
    // For example, you might want to initiate audio recording here
    // ...

    // Send a test audio data after the connection is open (replace this with actual audio data)
    sendAudioData("Test audio data");
});

// Handle incoming messages (audio data or response data)
socket.addEventListener('message', (event) => {
    console.log('Received data:', event.data);

    // Check if it's audio data or response data and handle accordingly
    if (event.data.startsWith("Recognition result:")) {
        // Handle response data
        const recognitionResult = event.data.replace("Recognition result:", "").trim();
        console.log('Recognition result:', recognitionResult);
    } else {
        // Handle audio data
        console.log('Received audio data:', event.data);
    }
});

// Handle connection close
socket.addEventListener('close', (event) => {
    console.log('WebSocket connection closed');
});

// Send audio data to the backend
function sendAudioData(audioData) {
    // Check if the WebSocket connection is open before sending data
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(audioData);
    } else {
        console.error('WebSocket connection is not open.');
    }
}

// end of BigDaddy.js



  return (
    <View style={styles.container}>
      <Button
        title={recording ? "Stop Recording" : "Start Recording"}
        onPress={recording ? stopRecording : startRecording}
      />
    </View>
  );


}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    backgroundColor: "#ecf0f1",
    padding: 10,
  },
});
