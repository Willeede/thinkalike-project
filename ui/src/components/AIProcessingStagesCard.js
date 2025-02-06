import React from 'react';
import { Card, CardContent, Typography, ListGroup } from '@mui/material';

const AIProcessingStagesCard = ({ stages }) => (
  <Card>
    <CardContent>
      <Typography variant="h6" component="div">
        AI Processing Stages
      </Typography>
      <ListGroup>
        {stages && stages.length > 0 ? (
          stages.map((stage, index) => (
            <ListGroup.Item key={index}>{stage}</ListGroup.Item>
          ))
        ) : (
          <ListGroup.Item>No AI processing stages specified.</ListGroup.Item>
        )}
      </ListGroup>
    </CardContent>
  </Card>
);

export default AIProcessingStagesCard;