import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiArrowLeft, FiEdit2, FiPackage, FiDollarSign, FiStar, FiList } from 'react-icons/fi';

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
`;

const Header = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  
  @media (max-width: 768px) {
    padding: 1.5rem;
  }
`;

const Title = styled.h2`
  margin: 0;
  font-family: 'Playfair Display', serif;
  font-weight: 600;
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  letter-spacing: 0.3px;
  
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

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const FormSection = styled.div`
  display: grid;
  gap: 1rem;
  
  @media (min-width: 768px) {
    grid-template-columns: 1fr 1fr;
  }
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  color: #4a5568;
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Input = styled.input`
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  background: white;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  &::placeholder {
    color: #a0aec0;
  }
`;

const TextArea = styled.textarea`
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  min-height: 120px;
  resize: vertical;
  background: white;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  &::placeholder {
    color: #a0aec0;
  }
`;

const Select = styled.select`
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  background: white;
  cursor: pointer;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const ButtonGroup = styled.div`
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

  &:hover {
    background: #667eea;
    color: white;
    transform: translateY(-2px);
  }
`;

function EditProduct() {
  const { id } = useParams();
  const [formData, setFormData] = useState({
    name: '',
    brand: '',
    ingredientsList: '',
    starIngredients: '',
    productType: '',
    price: ''
  });

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/${id}`);
        if (response.ok) {
          const product = await response.json();
          setFormData({
            name: product.name || '',
            brand: product.brand || '',
            ingredientsList: product.ingredientsList || '',
            starIngredients: product.starIngredients || '',
            productType: product.productType || '',
            price: product.price || ''
          });
        } else {
          alert('Error fetching product');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Error fetching product');
      }
    };
    
    if (id) {
      fetchProduct();
    }
  }, [id]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        alert('Product updated successfully!');
        window.history.back();
      } else {
        alert('Error updating product');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error updating product');
    }
  };

  return (
    <Container
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <FormCard>
        <Header>
          <Title>
            <FiEdit2 /> Edit Product
          </Title>
        </Header>
        
        <Content>
          <Form onSubmit={handleSubmit}>
            <FormSection>
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
                />
              </FormGroup>
            </FormSection>
            
            <FormSection>
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
            
            <FormGroup>
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
              />
            </FormGroup>
            
            <FormGroup>
              <Label>
                <FiList /> Full Ingredients List
              </Label>
              <TextArea
                name="ingredientsList"
                placeholder="Enter the complete ingredients list"
                value={formData.ingredientsList}
                onChange={handleChange}
                required
              />
            </FormGroup>
            
            <ButtonGroup>
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
                <FiEdit2 /> Update Product
              </Button>
            </ButtonGroup>
          </Form>
        </Content>
      </FormCard>
    </Container>
  );
}

export default EditProduct; 