import React, { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Grid,
  Typography,
  LinearProgress,
  Switch,
} from "@mui/material";
import { motion } from "framer-motion";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import DeleteIcon from "@mui/icons-material/Delete";

function App() {
  const [files, setFiles] = useState([]);
  const [previews, setPreviews] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  // Toggle Dark Mode
  const toggleDarkMode = () => setDarkMode(!darkMode);

  // Handle File Selection
  const handleFileChange = (e) => {
    const uploadedFiles = Array.from(e.target.files);
    setFiles(uploadedFiles);
    setPreviews(uploadedFiles.map((file) => URL.createObjectURL(file)));
    setResults([]);
  };

  // Drag & Drop Events
  const handleDragOver = (e) => {
    e.preventDefault();
    setDragActive(true);
  };
  const handleDragLeave = () => setDragActive(false);
  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles(droppedFiles);
    setPreviews(droppedFiles.map((file) => URL.createObjectURL(file)));
    setResults([]);
  };

  // Remove all files
  const removeImages = () => {
    setFiles([]);
    setPreviews([]);
    setResults([]);
  };

  // Upload & Predict
  const handleUpload = async () => {
    if (files.length === 0) {
      alert("Please upload at least one image!");
      return;
    }

    setLoading(true);
    const predictions = [];

    for (const file of files) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const res = await fetch("http://127.0.0.1:8000/predict/", {
          method: "POST",
          body: formData,
        });
        const data = await res.json();

        predictions.push({
          name: file.name,
          predicted_class: data.predicted_class || "Unknown",
          confidence: parseFloat(data.confidence) || 0,
        });
      } catch (error) {
        predictions.push({ name: file.name, predicted_class: "Error", confidence: 0 });
      }
    }

    setResults(predictions);
    setLoading(false);
  };

  return (
    <Box
      minHeight="100vh"
      bgcolor={darkMode ? "#1e1e1e" : "#f9fafb"}
      color={darkMode ? "white" : "black"}
      display="flex"
      flexDirection="column"
    >
      {/* HEADER */}
      <Box bgcolor={darkMode ? "#222" : "#4caf50"} p={3} textAlign="center">
        <Typography variant="h4" color="white" fontWeight="bold">
          🌱 KissanAI - Crop Disease Detection
        </Typography>
        <Typography variant="subtitle1" color="white">
          Upload multiple leaf images to detect plant diseases
        </Typography>
        <Switch checked={darkMode} onChange={toggleDarkMode} color="default" /> 
        <Typography variant="caption" color="white">Dark Mode</Typography>
      </Box>

      {/* MAIN CONTENT */}
      <Box flexGrow={1} display="flex" justifyContent="center" alignItems="center" p={3}>
        <Card sx={{ width: "85%", maxWidth: 850, p: 3, boxShadow: 6, borderRadius: 3, bgcolor: darkMode ? "#333" : "white" }}>
          <CardContent>
            <Typography variant="h6" align="center" gutterBottom>
              Upload the leaf image
            </Typography>

            {/* Drag & Drop Zone */}
            <Box
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              sx={{
                border: `2px dashed ${dragActive ? "#4caf50" : "#aaa"}`,
                borderRadius: 2,
                p: 3,
                textAlign: "center",
                bgcolor: dragActive ? "#d0f5d0" : darkMode ? "#444" : "#fafafa",
                cursor: "pointer",
                mb: 2,
              }}
            >
              <input type="file" multiple onChange={handleFileChange} accept="image/*" style={{ display: "none" }} id="fileInput" />
              <label htmlFor="fileInput">
                <CloudUploadIcon sx={{ fontSize: 50, color: "#4caf50" }} />
                <Typography variant="body1">Drag & Drop or Click to Upload</Typography>
              </label>
            </Box>

            {/* Action Buttons */}
            <Box textAlign="center" mb={2}>
              {files.length > 0 && (
                <Button startIcon={<DeleteIcon />} color="error" variant="outlined" sx={{ mr: 2 }} onClick={removeImages}>
                  Clear All
                </Button>
              )}
              <Button variant="contained" color="success" onClick={handleUpload} disabled={loading}>
                {loading ? "Predicting..." : "Predict"}
              </Button>
            </Box>

            {/* Image Previews */}
            <Grid container spacing={2} justifyContent="center">
              {previews.map((src, index) => (
                <Grid item xs={6} sm={4} md={3} key={index}>
                  <motion.img
                    src={src}
                    alt="preview"
                    style={{
                      width: "100%",
                      borderRadius: 8,
                      boxShadow: "0px 2px 6px rgba(0,0,0,0.2)",
                    }}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.3 }}
                  />
                </Grid>
              ))}
            </Grid>

            {/* Loader */}
            {loading && <Box textAlign="center" mt={2}><CircularProgress /></Box>}

            {/* Results */}
            {results.length > 0 && (
              <Box mt={3}>
                <Typography variant="h6">🔍 Results:</Typography>
                {results.map((res, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ y: 30, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ duration: 0.4 }}
                  >
                    <Card sx={{ p: 2, my: 1, background: darkMode ? "#555" : "#f1f8e9" }}>
                      <Typography variant="subtitle1" fontWeight="bold">{res.name}</Typography>
                      <Typography>Prediction: {res.predicted_class}</Typography>
                      <Typography>Confidence: {res.confidence}%</Typography>
                      <LinearProgress variant="determinate" value={res.confidence} sx={{ mt: 1 }} />
                    </Card>
                  </motion.div>
                ))}
              </Box>
            )}
          </CardContent>
        </Card>
      </Box>

      {/* FOOTER */}
      <Box bgcolor={darkMode ? "#222" : "#4caf50"} p={2} textAlign="center" color="white">
        <Typography variant="body2">🚀 Developed by Muhammad Anas</Typography>
      </Box>
    </Box>
  );
}

export default App;
