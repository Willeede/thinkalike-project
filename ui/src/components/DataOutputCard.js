// src/components/DataOutputCard.js
import React from 'react';
import { Card, CardContent, Typography, ListGroup } from '@mui/material';

const DataOutputCard = ({ outputs }) => (
  <Card>
    <CardContent>
      <Typography variant="h6" component="div">
        Data Outputs
      </Typography>
      <ListGroup>
        {outputs && outputs.length > 0 ? (
          outputs.map((output, index) => (
            <ListGroup.Item key={index}>{output}</ListGroup.Item>
          ))
        ) : (
          <ListGroup.Item>No data outputs specified.</ListGroup.Item>
        )}
      </ListGroup>
    </CardContent>
  </Card>
);

export default DataOutputCard;