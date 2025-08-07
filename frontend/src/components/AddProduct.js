import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiArrowLeft, FiPlus, FiPackage, FiDollarSign, FiStar, FiList } from 'react-icons/fi';

// Constants
const API_BASE_URL = 'http://localhost:8080/api/products';


// Styled Components
const Container = styled(motion.div)`
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
  min-height: 100vh;
  
  @media (min-width: 768px) {
    padding: 0 2rem;
  }
`;

const FormCard = styled(motion.div)`
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: 100%;
  position: relative;
  

`;

const Header = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
    pointer-events: none;
  }
  
  @media (max-width: 768px) {
    padding: 1.5rem;
  }
`;

const Title = styled(motion.h2)`
  margin: 0;
  font-family: 'Playfair Display', serif;
  font-weight: 600;
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  letter-spacing: 0.3px;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    font-size: 1.7rem;
  }
`;

const Content = styled.div`
  padding: 2rem;
  
  @media (max-width: 768px) {
    padding: 1.5rem;
  }
`;

const Form = styled(motion.form)`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const FormSection = styled(motion.div)`
  display: grid;
  gap: 1rem;
  
  @media (min-width: 768px) {
    grid-template-columns: 1fr 1fr;
  }
`;

const FormGroup = styled(motion.div)`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled(motion.label)`
  color: #4a5568;
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  
  &::before {
    content: '✨';
    position: absolute;
    left: -20px;
    opacity: 0;
    transition: opacity 0.3s;
  }
  
  &:hover::before {
    opacity: 1;
  }
`;

const Input = styled(motion.input)`
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  background: white;
  transition: all 0.3s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    transform: translateY(-1px);
  }

  &::placeholder {
    color: #a0aec0;
  }
`;

const TextArea = styled(motion.textarea)`
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  min-height: 120px;
  resize: vertical;
  background: white;
  transition: all 0.3s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    transform: translateY(-1px);
  }

  &::placeholder {
    color: #a0aec0;
  }
`;

const Select = styled(motion.select)`
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    transform: translateY(-1px);
  }
`;

const ButtonGroup = styled(motion.div)`
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const Button = styled(motion.button)`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 14px 28px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  flex: 1;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.6s;
  }
  
  &:hover::before {
    left: 100%;
  }

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  }
`;

const BackButton = styled(motion.button)`
  background: transparent;
  color: #667eea;
  padding: 14px 28px;
  border: 2px solid #667eea;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  flex: 1;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
    transition: left 0.6s;
  }
  
  &:hover::before {
    left: 100%;
  }

  &:hover {
    background: #667eea;
    color: white;
    transform: translateY(-2px);
  }
`;

// Animation variants
const containerVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.8,
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 0.5
    }
  }
};

function AddProduct() {
  const [formData, setFormData] = useState({
    name: '',
    brand: '',
    ingredientsList: '',
    starIngredients: '',
    productType: '',
    price: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(API_BASE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        alert('Product added successfully!');
        window.history.back();
      } else {
        alert('Error adding product');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error adding product');
    }
  };

  return (
    <Container
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <FormCard
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        whileHover={{ y: -2 }}
      >
        <Header>
          <Title
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            whileHover={{ scale: 1.05 }}
          >
            <FiPlus /> Add New Product
          </Title>
        </Header>
        
        <Content>
          <Form
            onSubmit={handleSubmit}
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            <FormSection variants={itemVariants}>
              <FormGroup>
                <Label>
                  <FiPackage /> Product Name
                </Label>
                <Input
                  type="text"
                  name="name"
                  placeholder="Enter product name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  whileFocus={{ scale: 1.02 }}
                />
              </FormGroup>
              
              <FormGroup>
                <Label>
                  <FiPackage /> Brand
                </Label>
                <Input
                  type="text"
                  name="brand"
                  placeholder="Enter brand name"
                  value={formData.brand}
                  onChange={handleChange}
                  required
                  whileFocus={{ scale: 1.02 }}
                />
              </FormGroup>
            </FormSection>
            
            <FormSection variants={itemVariants}>
              <FormGroup>
                <Label>
                  <FiStar /> Star Ingredients
                </Label>
                <Input
                  type="text"
                  name="starIngredients"
                  placeholder="e.g., Hyaluronic Acid, Vitamin C"
                  value={formData.starIngredients}
                  onChange={handleChange}
                  required
                  whileFocus={{ scale: 1.02 }}
                />
              </FormGroup>
              
              <FormGroup>
                <Label>
                  <FiPackage /> Product Type
                </Label>
                <Select
                  name="productType"
                  value={formData.productType}
                  onChange={handleChange}
                  required
                  whileFocus={{ scale: 1.02 }}
                >
                  <option value="">Select Product Type</option>
                  <option value="Cleanser">Cleanser</option>
                  <option value="Toner">Toner</option>
                  <option value="Moisturizer">Moisturizer</option>
                  <option value="Serum">Serum</option>
                  <option value="Sunscreen">Sunscreen</option>
                  <option value="Other">Other</option>
                </Select>
              </FormGroup>
            </FormSection>
            
            <FormGroup variants={itemVariants}>
              <Label>
                <FiDollarSign /> Price
              </Label>
              <Input
                type="number"
                name="price"
                placeholder="Enter price"
                value={formData.price}
                onChange={handleChange}
                required
                whileFocus={{ scale: 1.02 }}
              />
            </FormGroup>
            
            <FormGroup variants={itemVariants}>
              <Label>
                <FiList /> Full Ingredients List
              </Label>
              <TextArea
                name="ingredientsList"
                placeholder="Enter the complete ingredients list"
                value={formData.ingredientsList}
                onChange={handleChange}
                required
                whileFocus={{ scale: 1.02 }}
              />
            </FormGroup>
            
            <ButtonGroup variants={itemVariants}>
              <BackButton 
                type="button"
                onClick={() => window.history.back()}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <FiArrowLeft /> Back
              </BackButton>
              <Button 
                type="submit"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <FiPlus /> Add Product
              </Button>
            </ButtonGroup>
          </Form>
        </Content>
      </FormCard>
    </Container>
  );
}

export default AddProduct; 