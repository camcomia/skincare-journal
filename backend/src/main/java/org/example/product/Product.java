package org.example.product;

import jakarta.persistence.*;

@Entity
@Table(name = "skincare_products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String brand;

    @Column(length = 1000)
    private String ingredientsList;

    private String starIngredients;
    private String productType;
    private Long price;

    public Product() {};

    public Product(Long id, String name, String brand, String ingredientsList, String starIngredients, String productType, Long price) {
        this.id = id;
        this.name = name;
        this.brand = brand;
        this.ingredientsList = ingredientsList;
        this.starIngredients = starIngredients;
        this.productType = productType;
        this.price = price;
    }

    // Getters and setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    public String getIngredientsList() {
        return ingredientsList;
    }

    public void setIngredientsList(String ingredientsList) {
        this.ingredientsList = ingredientsList;
    }

    public String getStarIngredients() {
        return starIngredients;
    }

    public void setStarIngredients(String starIngredients) {
        this.starIngredients = starIngredients;
    }

    public String getProductType() {
        return productType;
    }

    public void setProductType(String productType) {
        this.productType = productType;
    }

    public Long getPrice() {
        return price;
    }

    public void setPrice(Long price) {
        this.price = price;
    }
}