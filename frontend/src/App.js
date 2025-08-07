// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import ProductList from './components/ProductList';
import AddProduct from './components/AddProduct';
import EditProduct from './components/EditProduct';
import styled, { keyframes } from 'styled-components';
import { motion } from 'framer-motion';

// Floating animation for particles
const float = keyframes`
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  25% { transform: translateY(-20px) rotate(90deg); }
  50% { transform: translateY(-10px) rotate(180deg); }
  75% { transform: translateY(-30px) rotate(270deg); }
`;

const sparkle = keyframes`
  0%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
  50% { opacity: 1; transform: scale(1) rotate(180deg); }
`;

const Container = styled.div`
  background: linear-gradient(135deg, #f9a8d4 0%, #ec4899 100%);
  min-height: 100vh;
  padding: 1rem;
  font-family: 'Inter', sans-serif;
  position: relative;
  overflow: hidden;
  
  @media (min-width: 768px) {
    padding: 2rem;
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 20% 80%, rgba(249, 168, 212, 0.3) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(236, 72, 153, 0.3) 0%, transparent 50%),
      radial-gradient(circle at 40% 40%, rgba(251, 207, 232, 0.2) 0%, transparent 50%);
    pointer-events: none;
    z-index: 1;
  }
  
  /* Global override to ensure all cards are opaque */
  * {
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
  }
  
  /* Specifically target product cards */
  [data-testid="product-card"], 
  .product-card,
  div[style*="background: white"] {
    background: white !important;
    opacity: 1 !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    isolation: isolate !important;
    z-index: 1 !important;
  }
`;

const FloatingParticle = styled.div`
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  animation: ${float} 6s ease-in-out infinite;
  animation-delay: ${props => props.delay}s;
  left: ${props => props.left}%;
  top: ${props => props.top}%;
  z-index: 2;
`;

const SparkleParticle = styled.div`
  position: absolute;
  width: 6px;
  height: 6px;
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
  animation: ${sparkle} 3s ease-in-out infinite;
  animation-delay: ${props => props.delay}s;
  left: ${props => props.left}%;
  top: ${props => props.top}%;
  z-index: 3;
`;

const TitleContainer = styled.div`
  position: relative;
  z-index: 10;
`;

const Title = styled(motion.h1)`
  color: white;
  text-align: center;
  font-family: 'Playfair Display', serif;
  font-weight: 700;
  font-size: 3.5rem;
  margin-bottom: 1rem;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  letter-spacing: 0.5px;
  position: relative;
  
  @media (max-width: 768px) {
    font-size: 2.8rem;
  }
  
  @media (max-width: 480px) {
    font-size: 2.4rem;
  }
  

`;

const GlowText = styled.span`
  background: linear-gradient(45deg, #ffffff, #f0f0f0, #ffffff);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 3s ease-in-out infinite;
  
  @keyframes shimmer {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
  }
`;

function App() {
  // Generate floating particles
  const particles = Array.from({ length: 15 }, (_, i) => ({
    id: i,
    left: Math.random() * 100,
    top: Math.random() * 100,
    delay: Math.random() * 6
  }));

  // Generate sparkle particles
  const sparkles = Array.from({ length: 8 }, (_, i) => ({
    id: i,
    left: Math.random() * 100,
    top: Math.random() * 100,
    delay: Math.random() * 3
  }));

  return (
    <Router>
      <Container>
        {/* Floating particles */}
        {particles.map(particle => (
          <FloatingParticle
            key={particle.id}
            left={particle.left}
            top={particle.top}
            delay={particle.delay}
          />
        ))}
        
        {/* Sparkle particles */}
        {sparkles.map(sparkle => (
          <SparkleParticle
            key={sparkle.id}
            left={sparkle.left}
            top={sparkle.top}
            delay={sparkle.delay}
          />
        ))}
        
        <TitleContainer>
          <Title
            initial={{ opacity: 0, y: -50, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ 
              duration: 1.2, 
              ease: "easeOut",
              type: "spring",
              stiffness: 100
            }}
            whileHover={{ 
              scale: 1.05,
              textShadow: "0 8px 16px rgba(0, 0, 0, 0.3)"
            }}
          >
            <GlowText>My Skincare Journal</GlowText> ✨
          </Title>
        </TitleContainer>
        
        <Switch>
          <Route exact path="/" component={ProductList} />
          <Route path="/add" component={AddProduct} />
          <Route path="/edit/:id" component={EditProduct} />
        </Switch>
      </Container>
    </Router>
  );
}

export default App;