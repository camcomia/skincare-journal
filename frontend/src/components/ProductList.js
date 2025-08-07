// ProductList.js
import React from 'react';
import styled, { keyframes } from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { FiPlus, FiArrowUp } from 'react-icons/fi';
import { useHistory } from 'react-router-dom';

// Import extracted components
import ProductCard from './ui/ProductCard';
import FilterBar from './ui/FilterBar';
import EmptyState from './ui/EmptyState';
import { useProductList } from './common/useProductList';

// Animations
const pulse = keyframes`
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
`;

const float = keyframes`
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
`;

// Styled Components
const Container = styled(motion.div)`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  min-height: 100vh;
  position: relative;
  
  &::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 20% 80%, rgba(249, 168, 212, 0.3) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(236, 72, 153, 0.3) 0%, transparent 50%),
      radial-gradient(circle at 40% 40%, rgba(251, 207, 232, 0.2) 0%, transparent 50%);
    pointer-events: none;
    z-index: -1;
  }
  
  @media (min-width: 768px) {
    padding: 0 2rem;
  }
`;

const Header = styled(motion.div)`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
  padding: 2rem 0;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  }
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
`;

const AnimatedHeader = styled(motion.h1)`
  color: white;
  font-size: 2.8rem;
  margin: 0;
  font-family: 'Playfair Display', serif;
  font-weight: 600;
  background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
  letter-spacing: 0.3px;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, #f9a8d4, #ec4899);
    animation: expand 2s ease-out forwards;
  }
  
  @keyframes expand {
    to { width: 100%; }
  }
`;

const ProductCount = styled(motion.p)`
  color: white;
  margin: 0.75rem 0 0 0;
  font-size: 1.1rem;
  font-weight: 500;
  letter-spacing: 0.5px;
  position: relative;
  
  &::before {
    content: '✨';
    position: absolute;
    left: -25px;
    top: 50%;
    transform: translateY(-50%);
    animation: ${pulse} 2s ease-in-out infinite;
  }
`;

const ProductGrid = styled(motion.div)`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
  isolation: isolate;
  z-index: 1;
  position: relative;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
`;

const Button = styled(motion.button)`
  background: ${props => props.primary ? 'linear-gradient(135deg, #f9a8d4 0%, #ec4899 100%)' : 'transparent'};
  color: ${props => props.primary ? 'white' : '#f9a8d4'};
  border: 2px solid #f9a8d4;
  padding: 12px 24px;
  border-radius: 12px;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(249, 168, 212, 0.3);
  }
`;

const FloatingUpButton = styled(motion.button)`
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: linear-gradient(135deg, #f9a8d4 0%, #ec4899 100%);
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(249, 168, 212, 0.3);
  z-index: 1000;
  animation: ${float} 3s ease-in-out infinite;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(249, 168, 212, 0.4);
  }
`;

const Spinner = styled.div`
  border: 3px solid rgba(255, 255, 255, 0.5);
  border-top: 3px solid white;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const LoadingOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255,255,255,0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  z-index: 5;
`;

const LoadingContent = styled.div`
  background: rgba(255,255,255,0.9);
  padding: 1rem 2rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
`;

const EndMessage = styled(motion.div)`
  text-align: center;
  padding: 2rem;
`;

const EndText = styled.p`
  color: rgba(255,255,255,0.7);
  font-style: italic;
`;

const LoadingMoreContainer = styled.div`
  text-align: center;
  padding: 2rem;
`;

const LoadingMoreText = styled.p`
  color: white;
  margin-top: 1rem;
`;

// Animation variants
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20, scale: 0.9 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      type: "spring",
      stiffness: 100,
      damping: 15
    }
  }
};

const headerVariants = {
  hidden: { opacity: 0, x: -50 },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 0.8,
      ease: "easeOut"
    }
  }
};

function ProductList() {
  const history = useHistory();
  
  // Use the custom hook for all product list logic
  const {
    // State
    products,
    loading,
    error,
    expandedIngredients,
    showScrollUp,
    hasMore,
    loadingMore,
    totalProductsInSystem,
    isApplyingFilters,
    activeFilters,
    brands,
    searchInputValue,
    
    // Actions
    handleSearchChange,
    handleSearchSubmit,
    clearSearch,
    handleProductTypeChange,
    handleBrandChange,
    handleSortChange,
    handleTagToggle,
    clearFilters,
    toggleIngredients,
    deleteProduct,
    scrollToTop
  } = useProductList();

  // Loading state
  if (loading) {
    return (
      <Container>
        <div style={{ textAlign: 'center', padding: '4rem 2rem' }}>
          <Spinner />
          <p style={{ color: 'white', marginTop: '1rem', fontSize: '1.1rem' }}>Loading products...</p>
        </div>
      </Container>
    );
  }

  // Error state
  if (error) {
    return (
      <Container>
        <div style={{ textAlign: 'center', padding: '4rem 2rem' }}>
          <p style={{ color: '#fed7d7' }}>{error}</p>
          <Button onClick={() => window.location.reload()}>Retry</Button>
        </div>
      </Container>
    );
  }

  return (
    <Container
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <Header
        variants={headerVariants}
        initial="hidden"
        animate="visible"
      >
        <div>
          <AnimatedHeader
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            My Products
          </AnimatedHeader>
          <ProductCount
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            {products.length} of {totalProductsInSystem} products
          </ProductCount>
        </div>
        <Button 
          primary 
          onClick={() => history.push('/add')}
          whileHover={{ scale: 1.05, y: -2 }}
          whileTap={{ scale: 0.95 }}
          style={{
            background: 'linear-gradient(135deg, #f9a8d4 0%, #ec4899 100%)',
            boxShadow: '0 8px 25px rgba(249, 168, 212, 0.3)',
            border: 'none',
            fontSize: '1rem',
            padding: '14px 28px'
          }}
        >
          <FiPlus /> Add New Product
        </Button>
      </Header>
      
      {/* Filter Bar */}
      <FilterBar
        searchInputValue={searchInputValue}
        activeFilters={activeFilters}
        brands={brands}
        onSearchChange={handleSearchChange}
        onSearchSubmit={handleSearchSubmit}
        onClearSearch={clearSearch}
        onProductTypeChange={handleProductTypeChange}
        onBrandChange={handleBrandChange}
        onSortChange={handleSortChange}
        onTagToggle={handleTagToggle}
        onClearFilters={clearFilters}
        isApplyingFilters={isApplyingFilters}
      />
      
      {/* Products Section with Animation */}
      <AnimatePresence mode="wait">
        <motion.div
          key={`products-${JSON.stringify(activeFilters)}`}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.5 }}
        >
          {products.length === 0 ? (
            <EmptyState
              totalProductsInSystem={totalProductsInSystem}
              onClearFilters={clearFilters}
            />
          ) : (
            <div style={{ position: 'relative' }}>
              <ProductGrid
                variants={containerVariants}
                initial="hidden"
                animate="visible"
              >
                {products.map((product, index) => (
                  <motion.div
                    key={product.id}
                    variants={itemVariants}
                    style={{ 
                      background: 'white !important',
                      borderRadius: '20px',
                      isolation: 'isolate',
                      zIndex: 1,
                      opacity: '1 !important',
                      backdropFilter: 'none !important',
                      WebkitBackdropFilter: 'none !important',
                      position: 'relative'
                    }}
                    whileHover={{ 
                      scale: 1.02,
                      y: -5,
                      transition: { duration: 0.2 }
                    }}
                  >
                    <ProductCard
                      product={product}
                      index={index}
                      expandedIngredients={expandedIngredients}
                      onToggleIngredients={toggleIngredients}
                      onDeleteProduct={deleteProduct}
                      onEditProduct={(id) => history.push(`/edit/${id}`)}
                    />
                  </motion.div>
                ))}
              </ProductGrid>
              {isApplyingFilters && (
                <LoadingOverlay>
                  <LoadingContent>
                    <Spinner />
                    <span style={{ color: '#2d3748', fontWeight: 500 }}>Updating products...</span>
                  </LoadingContent>
                </LoadingOverlay>
              )}
            </div>
          )}
          
          {loadingMore && hasMore && (
            <LoadingMoreContainer>
              <Spinner />
              <LoadingMoreText>Loading more products...</LoadingMoreText>
            </LoadingMoreContainer>
          )}
          
          {!hasMore && products.length > 0 && (
            <EndMessage
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.7 }}
            >
              <EndText>
                You've reached the end of your products
              </EndText>
            </EndMessage>
          )}
        </motion.div>
      </AnimatePresence>
      
      {showScrollUp && (
        <FloatingUpButton 
          onClick={scrollToTop} 
          aria-label="Back to top"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          <FiArrowUp />
        </FloatingUpButton>
      )}
    </Container>
  );
}

export default ProductList;