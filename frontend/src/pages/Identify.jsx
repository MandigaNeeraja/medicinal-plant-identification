import { useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import api, { getErrorMessage } from '../api/client';

export default function Identify() {
  const fileInputRef = useRef(null);
  const [preview, setPreview] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFile = (file) => {
    if (!file) return;
    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
  };

  const handlePredict = async () => {
    if (!selectedFile) {
      toast.error('Please select an image first');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    setLoading(true);

    try {
      const response = await api.post('/predictions/predict', formData);
      setResult(response.data.data);
      if (response.data.data.success) {
        toast.success('Plant identified successfully');
      } else {
        toast.error(response.data.data.message || 'Could not identify plant');
      }
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="space-y-8">
      <section className="card">
        <h1 className="text-3xl font-bold gradient-text">Identify a plant</h1>
        <p className="mt-2 text-white/70">Upload a clear leaf image for AI-powered identification.</p>
      </section>

      <section className="card">
        <div
          className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-purple-400/30 bg-white/5 px-6 py-16 text-center transition hover:border-purple-400/60"
          onClick={() => fileInputRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            handleFile(e.dataTransfer.files[0]);
          }}
        >
          <div className="text-4xl">📷</div>
          <p className="mt-4 font-medium">Click or drag and drop a leaf image</p>
          <p className="mt-1 text-sm text-white/50">PNG, JPG, WEBP up to 16MB</p>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => handleFile(e.target.files[0])}
          />
        </div>

        {preview && (
          <div className="mt-6 grid gap-6 lg:grid-cols-2">
            <img src={preview} alt="Preview" className="max-h-96 w-full rounded-2xl object-cover" />
            <div className="flex flex-col gap-3">
              <button type="button" onClick={handlePredict} disabled={loading} className="btn-primary">
                {loading ? 'Analyzing...' : 'Identify plant'}
              </button>
              <button type="button" onClick={reset} className="btn-secondary">
                Choose another image
              </button>
            </div>
          </div>
        )}
      </section>

      {result && (
        <section className="card">
          {result.success ? (
            <>
              <h2 className="text-2xl font-bold">{result.plant}</h2>
              <div className="mt-4">
                <div className="mb-2 flex justify-between text-sm">
                  <span>Confidence</span>
                  <span>{Math.round(result.confidence * 100)}%</span>
                </div>
                <div className="h-3 overflow-hidden rounded-full bg-white/10">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-purple-500 to-cyan-400"
                    style={{ width: `${Math.round(result.confidence * 100)}%` }}
                  />
                </div>
              </div>
              {result.medicinal_uses?.length > 0 && (
                <div className="mt-6">
                  <h3 className="font-semibold">Medicinal uses</h3>
                  <ul className="mt-2 space-y-2 text-white/80">
                    {result.medicinal_uses.map((use) => (
                      <li key={use} className="rounded-lg bg-white/5 px-3 py-2 text-sm">
                        {use}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <div className="mt-6 flex flex-wrap gap-3">
                <Link to={`/plant/${result.plant}`} className="btn-secondary">
                  View plant details
                </Link>
                <Link to={`/chat/${result.plant}`} className="btn-primary">
                  Chat with AI
                </Link>
              </div>
            </>
          ) : (
            <div>
              <h2 className="text-xl font-semibold text-red-300">Could not identify plant</h2>
              <p className="mt-2 text-white/70">{result.message}</p>
            </div>
          )}
        </section>
      )}
    </div>
  );
}
