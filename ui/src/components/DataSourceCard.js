import React from 'react';
import { Card, CardContent, Typography, ListGroup } from '@mui/material';

const DataSourceCard = ({ sources }) => (
  <Card>
    <CardContent>
      <Typography variant="h6" component="div">
        Data Sources
      </Typography>
      <ListGroup>
        {sources && sources.length > 0 ? (
          sources.map((source, index) => (
            <ListGroup.Item key={index}>{source}</ListGroup.Item>
          ))
        ) : (
          <ListGroup.Item>No data sources specified.</ListGroup.Item>
        )}
      </ListGroup>
    </CardContent>
  </Card>
);

export default DataSourceCard;