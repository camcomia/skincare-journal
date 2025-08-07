import React from 'react';
import styled from 'styled-components';

const FilterGroup = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  height: 45px;
  
  label {
    font-weight: 600;
    color: #2d3748;
    font-size: 0.9rem;
    white-space: nowrap;
  }
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: stretch;
    height: auto;
    gap: 0.5rem;
  }
`;

const FilterSelect = styled.select`
  padding: 12px 20px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 500;
  background: white !important;
  color: #2d3748;
  cursor: pointer;
  min-width: 140px;
  height: 45px;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  opacity: 1 !important;
  isolation: isolate;
  z-index: 1;
  
  &:focus {
    border-color: #f9a8d4;
    box-shadow: 0 4px 12px rgba(249, 168, 212, 0.15);
    outline: none;
  }
  
  &:hover {
    border-color: #f9a8d4;
  }
`;

const FilterSelectWithOptions = ({ 
  value, 
  onChange, 
  options, 
  placeholder = "Select option",
  label,
  disabled = false,
  ...props
}) => (
  <FilterGroup>
    <label>{label}:</label>
    <FilterSelect 
      value={value} 
      onChange={onChange}
      disabled={disabled}
      {...props}
    >
      <option value="">{placeholder}</option>
      {options.map(option => (
        <option key={option.value || option} value={option.value || option}>
          {option.label || option}
        </option>
      ))}
    </FilterSelect>
  </FilterGroup>
);

export default FilterSelectWithOptions;
