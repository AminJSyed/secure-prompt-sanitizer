import { useCallback, useState } from "react";
import "./App.css";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function App() {
  const [text, setText] = useState("");
  const [manualMasks, setManualMasks] = useState("");
  const [userGoal, setUserGoal] = useState("");
  const [files, setFiles] = useState([]);
  const [pastedImages, setPastedImages] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const allFiles = [...files, ...pastedImages];

  const handlePaste = useCallback((event) => {
    const items = event.clipboardData?.items || [];
    const newImages = [];

    for (const item of items) {
      if (item.type.startsWith("image/")) {
        const file = item.getAsFile();

        if (file) {
          const namedFile = new File(
            [file],
            `pasted-screenshot-${Date.now()}.png`,
            { type: file.type || "image/png" }
          );

          newImages.push(namedFile);
        }
      }
    }

    if (newImages.length > 0) {
      event.preventDefault();
      setPastedImages((prev) => [...prev, ...newImages]);
    }
  }, []);

  const handleFileSelect = (event) => {
    const selected = Array.from(event.target.files || []);
    setFiles((prev) => [...prev, ...selected]);
  };

  const removeFile = (indexToRemove) => {
    const fileToRemove = allFiles[indexToRemove];

    if (fileToRemove.name.startsWith("pasted-screenshot-")) {
      setPastedImages((prev) => prev.filter((file) => file !== fileToRemove));
    } else {
      setFiles((prev) => prev.filter((file) => file !== fileToRemove));
    }
  };

  const copyToClipboard = async (value) => {
    await navigator.clipboard.writeText(value);
  };

  const sanitize = async () => {
    if (!text.trim() && allFiles.length === 0) {
      alert("Please paste text, paste a screenshot, or attach a file first.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("text", text);
      formData.append("user_goal", userGoal);
      formData.append("manual_masks", manualMasks);

      for (const file of allFiles) {
        formData.append("files", file);
      }

      const response = await fetch(`${API_BASE_URL}/sanitize`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `API error: ${response.status}`);
      }

      setResult(data);
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page">
      <section className="hero">
        <h1>🔐 Secure Prompt Sanitizer</h1>
        <p>
          Paste logs, code, configs, screenshots, or files. Everything is
          processed locally before you share a safe query with public AI.
        </p>
        <div className="warning">
          Local MVP: No cloud AI calls. Review sanitized output before sharing.
        </div>
      </section>

      <section className="card">
        <label>What do you want help with?</label>
        <input
          value={userGoal}
          onChange={(event) => setUserGoal(event.target.value)}
          placeholder="Example: Help me fix this Docker error / API 401 / Jenkins pipeline failure"
        />

        <label>Manual masking list</label>
        <textarea
          value={manualMasks}
          onChange={(event) => setManualMasks(event.target.value)}
          placeholder="Optional: Add one sensitive value per line. These will be replaced with <MANUAL_MASK>."
          rows={4}
        />

        <label>Main input</label>
        <div className="composer" onPaste={handlePaste}>
          <textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Paste your error/log here. You can also paste a screenshot directly into this box."
            rows={10}
          />

          <div className="composerFooter">
            <label className="attachButton" title="Attach file">
              +
              <input
                type="file"
                multiple
                accept=".png,.jpg,.jpeg,.webp,.txt,.log,.json,.yaml,.yml,.env"
                onChange={handleFileSelect}
              />
            </label>

            <button onClick={sanitize} disabled={loading}>
              {loading ? "Processing..." : "Sanitize and Generate Safe Query"}
            </button>
          </div>
        </div>

        {allFiles.length > 0 && (
          <div className="files">
            <strong>Attached / pasted files:</strong>

            <div className="fileGrid">
              {allFiles.map((file, index) => {
                const isImage = file.type.startsWith("image/");
                const previewUrl = isImage ? URL.createObjectURL(file) : null;

                return (
                  <div className="filePreviewCard" key={`${file.name}-${index}`}>
                    {isImage ? (
                      <a href={previewUrl} target="_blank" rel="noreferrer">
                        <img
                          src={previewUrl}
                          alt={file.name}
                          className="imagePreview"
                        />
                      </a>
                    ) : (
                      <div className="fileIcon">📄</div>
                    )}

                    <div className="fileMeta">
                      <span className="fileName">{file.name}</span>
                      <span className="fileHint">
                        {isImage ? "Click to open image" : "Attached file"}
                      </span>
                    </div>

                    <button onClick={() => removeFile(index)}>Remove</button>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </section>

      {result && (
        <section className="results">
          <h2>Detected Sensitive Items</h2>

          {result.findings.length > 0 ? (
            <div className="findingBox">
              Detected and masked {result.findings.length} sensitive item(s).
            </div>
          ) : (
            <div className="infoBox">
              No obvious secrets detected. Review manually before sharing.
            </div>
          )}

          {result.findings.length > 0 && (
            <table>
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Preview</th>
                </tr>
              </thead>
              <tbody>
                {result.findings.map((finding, index) => (
                  <tr key={index}>
                    <td>{finding.type}</td>
                    <td>{finding.preview}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          <div className="resultGrid">
            <div>
              <div className="resultHeader">
                <h2>Sanitized Text</h2>
                <button onClick={() => copyToClipboard(result.sanitized_text)}>
                  Copy
                </button>
              </div>
              <pre>{result.sanitized_text}</pre>
            </div>

            <div>
              <div className="resultHeader">
                <h2>Generated Safe Query</h2>
                <button onClick={() => copyToClipboard(result.safe_query)}>
                  Copy
                </button>
              </div>
              <pre>{result.safe_query}</pre>
            </div>
          </div>
        </section>
      )}
    </main>
  );
}

export default App;
