// DynamicForm.js (or DynamicForm.jsx)
import React from 'react';

const DynamicForm = ({ schema }) => {
  // 1. Process the schema prop (JSON object)
  const { formTitle, fields, validation, actions, layout } = schema;

  // 2. Render the form title (optional)
  const renderFormTitle = () => {
    if (formTitle) {
      return <h2>{formTitle}</h2>;
    }
    return null;
  };

  // 3. Render form fields based on schema (now with input type-specific rendering)
  const renderFields = () => {
    if (!fields || !Array.isArray(fields)) {
      return <p>No fields defined in schema.</p>; // Handle case with no fields
    }

    return fields.map((field, index) => {
      const { type, name, label, placeholder, defaultValue, validationRules, ...rest } = field; // Extract field properties

      let inputElement;

      // Render input element based on field.type
      switch (type) {
        case 'text':
          inputElement = <input type="text" id={name} name={name} placeholder={placeholder} defaultValue={defaultValue} />;
          break;
        case 'email':
          inputElement = <input type="email" id={name} name={name} placeholder={placeholder} defaultValue={defaultValue} />;
          break;
        case 'password':
          inputElement = <input type="password" id={name} name={name} placeholder={placeholder} defaultValue={defaultValue} />;
          break;
        case 'number': // Example of another basic type (we'll implement fully in next steps)
          inputElement = <input type="number" id={name} name={name} placeholder={placeholder} defaultValue={defaultValue} />;
          break;
        case 'dropdown': // Example of another basic type (we'll implement fully in next steps)
        case 'select':
          inputElement = <select id={name} name={name} defaultValue={defaultValue}> {/* Options will be added later */} </select>;
          break;
        case 'checkbox': // Example of another basic type (we'll implement fully in next steps)
          inputElement = <input type="checkbox" id={name} name={name} defaultValue={defaultValue} />;
          break;
        case 'radio': // Example of another basic type (we'll implement fully in next steps)
          inputElement = <input type="radio" id={name} name={name} defaultValue={defaultValue} />;
          break;
        default:
          inputElement = <p>Unknown field type: {type}</p>; // Handle unknown types
      }

      return (
        <div key={index} className="form-field">
          <label htmlFor={name}>{label}</label>
          {inputElement} {/* Render the input element */}
        </div>
      );
    });
  };

  // 4. Render the entire form
  return (
    <form className="dynamic-form">
      {renderFormTitle()} {/* Render form title */}
      {renderFields()}     {/* Render form fields */}
      {/* Add form-level validation display area here (future step) */}
      {/* Add action buttons here (e.g., Submit, Reset - future step) */}
    </form>
  );
};

export default DynamicForm;