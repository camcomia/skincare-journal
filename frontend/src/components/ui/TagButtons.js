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

const PillButton = styled.button`
  background: ${({ selected }) => selected ? 'linear-gradient(135deg, #f9a8d4 0%, #ec4899 100%)' : 'white'};
  color: ${({ selected }) => selected ? 'white' : '#f9a8d4'};
  border: 2px solid ${({ selected }) => selected ? 'transparent' : '#f9a8d4'};
  border-radius: 12px;
  padding: 12px 20px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  height: 45px;
  display: flex;
  align-items: center;
  transition: all 0.2s ease;
  box-shadow: ${({ selected }) => selected ? '0 4px 12px rgba(249, 168, 212, 0.3)' : '0 2px 4px rgba(0, 0, 0, 0.05)'};
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  opacity: 1 !important;
  isolation: isolate;
  z-index: 1;
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: ${({ selected }) => selected ? '0 6px 16px rgba(249, 168, 212, 0.4)' : '0 4px 8px rgba(0, 0, 0, 0.1)'};
  }
`;

const TagButtons = ({ 
  tags, 
  selectedTags, 
  onTagToggle,
  label = "Tags",
  disabled = false,
  ...props
}) => (
  <FilterGroup {...props}>
    <label>{label}:</label>
    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
      {tags.map(tag => (
        <PillButton
          key={tag}
          selected={selectedTags.includes(tag)}
          onClick={() => !disabled && onTagToggle(tag)}
          disabled={disabled}
        >
          {tag}
        </PillButton>
      ))}
    </div>
  </FilterGroup>
);

export default TagButtons;
