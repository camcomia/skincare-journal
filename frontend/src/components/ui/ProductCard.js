import React from 'react';
import styled, { keyframes } from 'styled-components';
import { motion } from 'framer-motion';
import { FiEdit2, FiTrash2, FiStar, FiPackage } from 'react-icons/fi';
import { useHistory } from 'react-router-dom';

// Animations

const float = keyframes`
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-3px); }
`;

// Styled Components
const Card = styled(motion.div)`
  background: white !important;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  height: 450px; /* Increased height to accommodate expanded content */
  min-height: 450px;
  position: relative;
  overflow: hidden;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  opacity: 1 !important;
  isolation: isolate;
  z-index: 1;
  

  
  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
  }
  
  @media (max-width: 768px) {
    padding: 1rem;
    height: auto;
    min-height: 400px;
  }
`;

const CardHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  position: relative;
  flex-shrink: 0; /* Prevent header from shrinking */
`;

const ProductName = styled(motion.h2)`
  font-size: 1.1rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
  flex: 1;
  padding-right: 170px;
  line-height: 1.3;
  position: relative;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* Limit to 2 lines */
  -webkit-box-orient: vertical;
  overflow: hidden;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, #f9a8d4, #ec4899);
    transition: width 0.3s ease;
  }
  
  &:hover::after {
    width: 100%;
  }
`;

const BrandBadge = styled(motion.div)`
  position: absolute;
  top: 0;
  right: 0;
  background: linear-gradient(135deg, #f9a8d4 0%, #ec4899 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  flex-shrink: 0;
  animation: ${float} 3s ease-in-out infinite;
  

`;

const CardContent = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1; /* Take up remaining space */
  min-height: 0; /* Allow content to shrink */
`;

const BadgesRow = styled.div`
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-start;
  flex-shrink: 0; /* Prevent badges from shrinking */
`;

const Badge = styled(motion.span)`
  background: ${props => props.type === 'price' ? 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)' : 'rgba(249, 168, 212, 0.1)'};
  color: ${props => props.type === 'price' ? 'white' : '#f9a8d4'};
  padding: 0.25rem 0.75rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  height: 28px;
  white-space: nowrap;
  position: relative;
  
  &:hover {
    transform: scale(1.05);
  }
`;

const TagsRow = styled.div`
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 0.5rem;
  align-items: baseline;
  justify-content: flex-start;
  min-height: 24px;
  line-height: 1;
  flex-shrink: 0; /* Prevent tags from shrinking */
`;

const Tag = styled(motion.span)`
  background: rgba(249, 168, 212, 0.1);
  color: #f9a8d4;
  padding: 0.3rem 0.6rem;
  border-radius: 8px;
  font-size: 0.7rem;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 26px;
  min-height: 26px;
  max-height: 26px;
  white-space: nowrap;
  line-height: 1;
  vertical-align: baseline;
  flex-shrink: 0;
  position: relative;
  border: 1px solid rgba(249, 168, 212, 0.2);
  transition: all 0.2s ease;
  
  &:hover {
    transform: scale(1.05);
    background: rgba(249, 168, 212, 0.15);
    border-color: rgba(249, 168, 212, 0.4);
  }
`;

const IngredientsSection = styled.div`
  margin-top: 0.5rem;
  flex: 1; /* Take up remaining space */
  min-height: 0; /* Allow content to shrink */
  display: flex;
  flex-direction: column;
  max-height: ${props => props.expanded ? '180px' : '80px'}; /* Limit height when expanded */
  overflow-y: ${props => props.expanded ? 'auto' : 'hidden'}; /* Add scroll when expanded */
  position: relative;
  
  /* Custom scrollbar styling */
  &::-webkit-scrollbar {
    width: 4px;
  }
  
  &::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 2px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #f9a8d4;
    border-radius: 2px;
  }
  
  &::-webkit-scrollbar-thumb:hover {
    background: #ec4899;
  }
`;

const IngredientsText = styled.p`
  color: #4a5568;
  font-size: 0.8rem;
  line-height: 1.4;
  margin: 0;
  display: ${props => props.expanded ? 'block' : '-webkit-box'};
  -webkit-line-clamp: ${props => props.expanded ? 'unset' : '3'}; /* Limit to 3 lines when not expanded */
  -webkit-box-orient: ${props => props.expanded ? 'unset' : 'vertical'};
  overflow: ${props => props.expanded ? 'visible' : 'hidden'};
  flex: 1; /* Take up remaining space */
  min-height: 0; /* Allow content to shrink */
  word-break: break-word;
  padding-right: ${props => props.expanded ? '8px' : '0'}; /* Add padding for scrollbar */
`;

const ExpandButton = styled(motion.button)`
  background: none;
  border: none;
  color: #f9a8d4;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  padding: 0.5rem 1rem;
  margin-top: 0.5rem;
  text-align: center;
  border-radius: 8px;
  transition: all 0.2s ease;
  width: 100%;
  
  &:hover {
    background: rgba(249, 168, 212, 0.1);
    transform: scale(1.05);
  }
  
  &:active {
    transform: scale(0.95);
  }
`;

const ActionsRow = styled.div`
  display: flex;
  gap: 0.5rem;
  margin-top: auto; /* Push to bottom */
  justify-content: flex-end;
  flex-shrink: 0; /* Prevent actions from shrinking */
`;

const ActionButton = styled(motion.button)`
  background: ${props => props.variant === 'primary' ? 'linear-gradient(135deg, #f9a8d4 0%, #ec4899 100%)' : 'transparent'};
  color: ${props => props.variant === 'primary' ? 'white' : '#f9a8d4'};
  border: 2px solid #f9a8d4;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(249, 168, 212, 0.3);
  }
`;

const formatPrice = (price) => {
  if (!price || price === 0) return '₱0';
  return `₱${parseFloat(price).toLocaleString()}`;
};

const getTags = (ingredientsList = '') => {
  const tags = [];
  const ingredients = ingredientsList.toLowerCase();
  
  // Check for alcohol content
  const hasAlcohol = ingredients.includes('alcohol') || 
                    ingredients.includes('ethanol') || 
                    ingredients.includes('denatured') ||
                    ingredients.includes('alcohol denat');
  
  // Check for fragrance content
  const hasFragrance = ingredients.includes('fragrance') || 
                       ingredients.includes('parfum') || 
                       ingredients.includes('perfume');
  
  // Check for oil content
  const hasOil = ingredients.includes('oil') || 
                 ingredients.includes('argan') || 
                 ingredients.includes('squalane') ||
                 ingredients.includes('coconut oil') ||
                 ingredients.includes('olive oil') ||
                 ingredients.includes('jojoba oil');
  
  // Add tags based on what's NOT present
  if (!hasAlcohol) {
    tags.push('alcohol-free');
  }
  if (!hasFragrance) {
    tags.push('fragrance-free');
  }
  if (!hasOil) {
    tags.push('oil-free');
  }
  
  // Sensitive Skin Friendly if no irritants
  if (!hasFragrance && !hasAlcohol && !hasOil) {
    tags.push('sensitive skin friendly');
  }
  
  return tags;
};

const ProductCard = ({ 
  product, 
  index, 
  expandedIngredients, 
  onToggleIngredients, 
  onDeleteProduct,
  onEditProduct 
}) => {
  const history = useHistory();
  const isExpanded = expandedIngredients[product.id];
  const tags = getTags(product.ingredientsList);
  const INGREDIENTS_EXPAND_THRESHOLD = 120;

  return (
    <Card
      data-testid="product-card"
      className="product-card"
      initial={{ opacity: 0, y: 20, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ 
        duration: 0.6, 
        delay: index * 0.1,
        type: "spring",
        stiffness: 100,
        damping: 15
      }}
      whileHover={{ 
        y: -8,
        transition: { duration: 0.2 }
      }}
    >
      <CardHeader>
        <ProductName
          whileHover={{ scale: 1.02 }}
          transition={{ duration: 0.2 }}
        >
          {product.name}
        </ProductName>
        <BrandBadge
          whileHover={{ scale: 1.05 }}
          transition={{ duration: 0.2 }}
        >
          {product.brand}
        </BrandBadge>
      </CardHeader>

      <CardContent>
        <BadgesRow>
          <Badge 
            type="type"
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.2 }}
          >
            <FiPackage size={12} />
            {product.productType}
          </Badge>
          <Badge 
            type="price"
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.2 }}
          >
            {formatPrice(product.price)}
          </Badge>
        </BadgesRow>

        {product.starIngredients && (
          <div style={{ marginTop: '0.5rem', marginBottom: '0.5rem' }}>
            <div style={{ 
              fontSize: '0.8rem', 
              fontWeight: 600, 
              color: '#f9a8d4',
              marginBottom: '0.2rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.25rem'
            }}>
              ⭐ Star Ingredients:
            </div>
            <div style={{ 
              fontSize: '0.75rem', 
              color: '#4a5568',
              lineHeight: '1.3'
            }}>
              {product.starIngredients}
            </div>
          </div>
        )}

        {product.ingredientsList && (
          <>
            <IngredientsSection expanded={isExpanded}>
              <IngredientsText expanded={isExpanded}>
                    {product.ingredientsList}
              </IngredientsText>
            </IngredientsSection>
            {product.ingredientsList.length > INGREDIENTS_EXPAND_THRESHOLD && (
              <ExpandButton 
                onClick={() => onToggleIngredients(product.id)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {isExpanded ? 'Show less' : 'Show more'}
              </ExpandButton>
            )}
          </>
        )}

        {tags.length > 0 && (
          <TagsRow>
            {tags.map((tag, tagIndex) => (
              <Tag 
                key={tag}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ 
                  duration: 0.3, 
                  delay: tagIndex * 0.1 
                }}
                whileHover={{ scale: 1.1 }}
              >
                {tag}
              </Tag>
            ))}
          </TagsRow>
        )}
      </CardContent>

      <ActionsRow>
        <ActionButton 
          onClick={() => onEditProduct(product.id)}
          whileHover={{ scale: 1.05, y: -2 }}
          whileTap={{ scale: 0.95 }}
        >
          <FiEdit2 size={14} />
          Edit
        </ActionButton>
        <ActionButton 
          variant="primary" 
          onClick={() => history.push(`/journal/${product.id}`)}
          whileHover={{ scale: 1.05, y: -2 }}
          whileTap={{ scale: 0.95 }}
        >
          <FiStar size={14} />
          Journal
        </ActionButton>
        <ActionButton 
          onClick={() => onDeleteProduct(product.id)}
          whileHover={{ scale: 1.05, y: -2 }}
          whileTap={{ scale: 0.95 }}
        >
          <FiTrash2 size={14} />
          Delete
        </ActionButton>
      </ActionsRow>
    </Card>
  );
};

export default ProductCard;
