import React from 'react';
import Table from './Table';

const Section = ({ title, data }) => {
  return (
    <div style={styles.section}>
      <h2 style={styles.header}>{title}</h2>
      <Table data={data} />
    </div>
  );
};

const styles = {
  section: {
    width: '45%',
    margin: '10px',
  },
  header: {
    textAlign: 'center',
    marginBottom: '10px',
  },
};

export default Section;