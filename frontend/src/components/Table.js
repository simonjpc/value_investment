// src/components/Table.js
import React from 'react';

const Table = ({ data }) => {
  if (!data || data.length === 0) {
    return <div>No data available</div>;
  }

  const headers = Object.keys(data[0]);

  return (
    <div style={styles.tableContainer}>
      <table style={styles.table}>
        <thead>
          <tr>
            {headers.map((header, index) => (
              <th key={index} style={styles.header}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {headers.map((header, colIndex) => (
                <td key={colIndex} style={styles.cell}>{row[header]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const styles = {
    tableContainer: {
      maxHeight: '400px',
      overflowY: 'scroll',
      border: '0px solid #ccc',
      padding: '0px',
    },
    table: {
      width: '100%',
      borderCollapse: 'collapse',
    },
    headerContainer: {
      position: 'sticky',
      top: 0,
      backgroundColor: '#f2f2f2',
      zIndex: 1,
    },
    header: {
      border: '0px solid #ccc',
      padding: '10px',
      backgroundColor: '#f2f2f2',
      position: 'sticky',
      top: 0,
      zIndex: 1,
    },
    cell: {
      border: '1px solid #ccc',
      padding: '8px',
    },
  };

export default Table;
