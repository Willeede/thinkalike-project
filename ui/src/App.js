import React from 'react';
import DynamicForm from './components/DynamicForm'; // Import DynamicForm component

function App() {
  // Example schema for DynamicForm
  const formSchema = {
    formTitle: "User Registration",
    fields: [
      {
        type: "text",
        name: "firstName",
        label: "First Name",
        placeholder: "Enter your first name"
      },
      {
        type: "email",
        name: "email",
        label: "Email Address",
        placeholder: "Enter your email"
      },
      {
        type: "password",
        name: "password",
        label: "Password",
        placeholder: "Enter your password"
      }
    ]
  };

  return (
    <div className="App">
      <h1>Welcome to ThinkAlike UI!</h1>
      <DynamicForm schema={formSchema} /> {/* Render DynamicForm component, passing the schema as a prop */}
    </div>
  );
}

export default App;