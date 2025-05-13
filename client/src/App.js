import { useState } from "react";
import "./App.css";

function App() {
  const [target, setTarget] = useState("");
  const [gifUrl, setGifUrl] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const iso = new Date(target).toISOString();
const url = `http://localhost:5050/timer?target=${encodeURIComponent(iso)}`;
    setGifUrl(url);
  };

  return (
    <div className="App">
      <h1>Email Countdown GIF Generator</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Target Date & Time:
          <input
            type="datetime-local"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            required
          />
        </label>
        <button type="submit">Generate GIF</button>
      </form>

      {gifUrl && (
        <div className="output">
          <h2>Preview</h2>
          <img src={gifUrl} alt="Countdown Timer" width="263" height="63" />

          <h3>Embed Code:</h3>
          <code>
            {`<img src="${gifUrl}" alt="Countdown Timer" width="263" height="63">`}
          </code>
        </div>
      )}
    </div>
  );
}

export default App;
