import React from 'react';
import styled from 'styled-components';
import { FiPlus, FiX } from 'react-icons/fi';
import { useHistory } from 'react-router-dom';

// Styled Components
const StatusContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
`;

const EmptyStateCard = styled.div`
  background: white;
  border-radius: 16px;
  padding: 2rem;
  max-width: 500px;
  margin: 0 auto;
  border: 1px solid #e2e8f0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
`;

const Message = styled.p`
  color: #2d3748;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  font-weight: 500;
`;

const SuggestionsList = styled.div`
  color: #4a5568;
  font-size: 0.95rem;
  text-align: left;
  margin-top: 1rem;
`;

const SuggestionsTitle = styled.p`
  margin-bottom: 0.5rem;
  font-weight: 500;
`;

const SuggestionsUl = styled.ul`
  text-align: left;
  margin: 0.5rem 0;
  padding-left: 1.5rem;
  line-height: 1.6;
`;

const ActionButton = styled.button`
  background: ${props => props.variant === 'primary' ? 'linear-gradient(135deg, #f9a8d4 0%, #ec4899 100%)' : 'transparent'};
  color: ${props => props.variant === 'primary' ? 'white' : '#f9a8d4'};
  border: ${props => props.variant === 'primary' ? 'none' : '1px solid #f9a8d4'};
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(249, 168, 212, 0.3);
  }
`;

const EmptyState = ({ 
  totalProductsInSystem, 
  onClearFilters, 
  onAddFirstProduct 
}) => {
  const history = useHistory();

  const handleAddFirstProduct = () => {
    if (onAddFirstProduct) {
      onAddFirstProduct();
    } else {
      history.push('/add');
    }
  };

  return (
    <StatusContainer>
      <EmptyStateCard>
        <Message>
          {totalProductsInSystem === 0 
            ? 'No products found. Add your first product!' 
            : 'No products match your current filters.'
          }
        </Message>
        
        {totalProductsInSystem > 0 && (
          <SuggestionsList>
            <SuggestionsTitle>Try adjusting your filters:</SuggestionsTitle>
            <SuggestionsUl>
              <li>Clear your search terms</li>
              <li>Try different product types</li>
              <li>Select different brands</li>
              <li>Remove some tag filters</li>
              <li>Use broader search terms</li>
            </SuggestionsUl>
            <ActionButton onClick={onClearFilters}>
              <FiX /> Clear All Filters
            </ActionButton>
          </SuggestionsList>
        )}
        
        {totalProductsInSystem === 0 && (
          <ActionButton variant="primary" onClick={handleAddFirstProduct}>
            <FiPlus /> Add Your First Product
          </ActionButton>
        )}
      </EmptyStateCard>
    </StatusContainer>
  );
};

export default EmptyState;
