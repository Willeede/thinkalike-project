import React from 'react';
import { Card, CardContent, Typography, ListGroup } from '@mui/material';

const DataTransformationCard = ({ transformations }) => (
  <Card>
    <CardContent>
      <Typography variant="h6" component="div">
        Data Transformations
      </Typography>
      <ListGroup>
        {transformations && transformations.length > 0 ? (
          transformations.map((transformation, index) => (
            <ListGroup.Item key={index}>{transformation}</ListGroup.Item>
          ))
        ) : (
          <ListGroup.Item>No data transformations specified.</ListGroup.Item>
        )}
      </ListGroup>
    </CardContent>
  </Card>
);

export default DataTransformationCard;