import React, { useEffect, useState } from 'react';


function App() {
  const [cbbiData, setCbbiData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/cbbi/latest')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not OK');
        }
        return response.json();
      })
      .then((data) => setCbbiData(data))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>BTC CBBI Index</h1>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {!cbbiData ? (
        <p>Loading...</p>
      ) : (
        <>
          <h2>Summary</h2>
          <p>Average Value: {cbbiData.summary.average_value}</p>
          <p>Live BTC Price: ${cbbiData.summary.live_btc_price.toLocaleString()}</p>
          <p>Max Date: {cbbiData.summary.max_date}</p>
          <p>Min Date: {cbbiData.summary.min_date}</p>
          <h2>Details</h2>
          <ul>
            {cbbiData.data.map((item, index) => (
              <li key={index}>
                <strong>{item.metric}:</strong> {item.value} (date: {item.date})
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;
