import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiSearch, FiX } from 'react-icons/fi';
import { PRODUCT_TYPES, SORT_OPTIONS, AVAILABLE_TAGS } from '../../constants/filterOptions';
import FilterSelectWithOptions from './FilterSelect';
import TagButtons from './TagButtons';

// Styled Components
const FilterBarContainer = styled(motion.div)`
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1.5rem;
  background: white !important;
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  position: relative;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  opacity: 1 !important;
  isolation: isolate;
  z-index: 1;
  

  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    padding: 1.5rem;
  }
`;

const SearchBar = styled(motion.div)`
  display: flex;
  align-items: center;
  background: white !important;
  border-radius: 16px;
  padding: 0.75rem 1.25rem;
  border: 2px solid #e2e8f0;
  flex: 1;
  min-width: 250px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  opacity: 1 !important;
  isolation: isolate;
  z-index: 1;
  

  
  &:focus-within {
    border-color: #f9a8d4;
    box-shadow: 0 4px 16px rgba(249, 168, 212, 0.15);
    transform: translateY(-2px);
  }
  
  input {
    border: none;
    outline: none;
    background: transparent;
    flex: 1;
    font-size: 1rem;
    font-weight: 500;
    
    &::placeholder {
      color: #a0aec0;
      font-weight: 400;
    }
  }
  
  .clear-search {
    background: none;
    border: none;
    color: #a0aec0;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    
    &:hover {
      background: #f7fafc;
      color: #4a5568;
      transform: scale(1.1);
    }
  }
`;

const FilterControls = styled.div`
  display: flex;
  gap: 1.5rem;
  align-items: center;
  flex-wrap: wrap;
  position: relative;
`;

const ClearButton = styled(motion.button)`
  display: flex;
  align-items: center;
  gap: 0.3rem;
  background: transparent !important;
  color: #f9a8d4;
  border: 1.5px solid #f9a8d4;
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  opacity: 1 !important;
  isolation: isolate;
  z-index: 1;
  

  
  &:hover {
    background: #f9a8d4;
    color: white;
    transform: translateY(-1px);
  }
`;


const FilterBar = ({
  searchInputValue,
  activeFilters,
  brands,
  onSearchChange,
  onSearchSubmit,
  onClearSearch,
  onProductTypeChange,
  onBrandChange,
  onSortChange,
  onTagToggle,
  onClearFilters,
  isApplyingFilters
}) => {
  const hasActiveFilters = activeFilters.productType || 
                          activeFilters.tags.length > 0 || 
                          activeFilters.brand || 
                          activeFilters.search;

  return (
    <FilterBarContainer
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ 
        duration: 0.8, 
        delay: 0.2,
        type: "spring",
        stiffness: 100,
        damping: 15
      }}
      whileHover={{ 
        y: -2,
        transition: { duration: 0.2 }
      }}
    >
      {/* Search Bar */}
      <SearchBar
        whileHover={{ scale: 1.02 }}
        transition={{ duration: 0.2 }}
      >
        <FiSearch style={{ color: '#a0aec0', marginRight: '0.75rem', fontSize: '1.1rem' }} />
        <input
          type="text"
          placeholder="Search products, brands, or ingredients... (Press Enter or click away)"
          value={searchInputValue}
          onChange={(e) => onSearchChange(e.target.value)}
          onBlur={(e) => onSearchSubmit(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault();
              onSearchSubmit(e.target.value);
            }
          }}
        />
        {activeFilters.search && (
          <motion.button
            className="clear-search"
            onClick={onClearSearch}
            aria-label="Clear search"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            <FiX />
          </motion.button>
        )}
      </SearchBar>
      
      {/* Filter Controls */}
      <FilterControls>
        {/* {isApplyingFilters && (
          <LoadingIndicator
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            Updating...
          </LoadingIndicator>
        )} */}
        
        {/* Type Filter */}
        <FilterSelectWithOptions
          value={activeFilters.productType}
          onChange={onProductTypeChange}
          options={PRODUCT_TYPES}
          placeholder="All Types"
          label="Type"
        />
        
        {/* Brand Filter */}
        <FilterSelectWithOptions
          value={activeFilters.brand}
          onChange={onBrandChange}
          options={brands}
          placeholder="All Brands"
          label="Brand"
        />
        
        {/* Sort Filter */}
        <FilterSelectWithOptions
          value={activeFilters.sortBy}
          onChange={onSortChange}
          options={SORT_OPTIONS}
          placeholder="Sort by"
          label="Sort"
        />
        
        {/* Tags Filter */}
        <TagButtons
          tags={AVAILABLE_TAGS}
          selectedTags={activeFilters.tags}
          onTagToggle={onTagToggle}
        />
        
        {/* Clear Filters Button */}
        {hasActiveFilters && (
          <ClearButton 
            onClick={onClearFilters}
            whileHover={{ scale: 1.05, y: -1 }}
            whileTap={{ scale: 0.95 }}
          >
            <FiX /> Clear Filters
          </ClearButton>
        )}
      </FilterControls>
    </FilterBarContainer>
  );
};

export default FilterBar;
