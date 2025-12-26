import React, { useState } from "react";
import axios from "axios";

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [resultImage, setResultImage] = useState(null);
  const [llmReport, setLlmReport] = useState("");
  const [defects, setDefects] = useState([]);
  const [chartImage, setChartImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setPreview(file ? URL.createObjectURL(file) : null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setError("");
    setResultImage(null);
    setLlmReport("");
    setDefects([]);
    setChartImage(null);
    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      const res = await axios.post("http://localhost:8000/detect", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResultImage(res.data.result_image);
      setLlmReport(res.data.llm_report);
      setDefects(res.data.defects);
      setChartImage(res.data.chart_image);
    } catch (err) {
      setError("Detection failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-4">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-blue-700 mb-2">Chip Defect Detection</h1>
        <p className="text-gray-600">Upload a chip image to detect defects and get a professional report.</p>
      </header>
      <div className="bg-white shadow-lg rounded-lg p-6 w-full max-w-xl flex flex-col items-center">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="mb-4"
        />
        {preview && (
          <img src={preview} alt="Preview" className="w-64 h-48 object-contain mb-4 border rounded" />
        )}
        <button
          onClick={handleUpload}
          disabled={!selectedFile || loading}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Detecting..." : "Detect Defects"}
        </button>
        {error && <p className="text-red-500 mt-2">{error}</p>}
      </div>
      {resultImage && (
        <div className="mt-8 w-full max-w-xl">
          <h2 className="text-xl font-semibold mb-2">Detection Result</h2>
          <img src={resultImage} alt="Result" className="w-full object-contain border rounded mb-4" />
        </div>
      )}
      {llmReport && (
        <div className="mt-8 w-full max-w-xl bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">LLM Report</h2>
          <pre className="whitespace-pre-wrap text-gray-800">{llmReport}</pre>
        </div>
      )}
      {chartImage && (
        <div className="mt-8 w-full max-w-xl bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Defect Frequency Chart</h2>
          <img src={chartImage} alt="Defect Chart" className="w-full object-contain" />
        </div>
      )}
    </div>
  );
}
