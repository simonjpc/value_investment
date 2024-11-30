import React from 'react';
import Section from './Section';

const MainContainer = ({ ncavData, epsxData }) => {
  return (
    <div style={styles.container}>
      <Section title="NCAV" data={ncavData} />
      <Section title="EPSX" data={epsxData} />
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'space-around',
    padding: '20px',
  },
};

export default MainContainer;