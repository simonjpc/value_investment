// src/App.js
import React, { useEffect, useState } from 'react';
import MainContainer from './components/MainContainer';

const App = () => {
  const [ncavData, setNcavData] = useState([]);
  const [epsxData, setEpsxData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const ncavResponse = await fetch(`${process.env.REACT_APP_API_URL}/api/ncav`);
        const epsxResponse = await fetch(`${process.env.REACT_APP_API_URL}/api/epsx`);

        if (!ncavResponse.ok || !epsxResponse.ok) {
          throw new Error('Network response was not ok');
        }

        const ncavData = await ncavResponse.json();
        const epsxData = await epsxResponse.json();

        setNcavData(ncavData);
        setEpsxData(epsxData);
        setLoading(false);
      } catch (error) {
        setError(error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="App">
      <MainContainer ncavData={ncavData} epsxData={epsxData} />
    </div>
  );
};

export default App;
