package org.example.product;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    
    // Find by product type with pagination
    Page<Product> findByProductTypeIgnoreCase(String productType, Pageable pageable);
    
    // Find by ingredients containing specific tags (case-insensitive)
    @Query("SELECT p FROM Product p WHERE LOWER(p.ingredientsList) LIKE LOWER(CONCAT('%', :tag, '%'))")
    Page<Product> findByTagsContainingIgnoreCase(@Param("tag") String tag, Pageable pageable);
    
    // Find by both product type and tags
    @Query("SELECT p FROM Product p WHERE LOWER(p.productType) = LOWER(:productType) AND LOWER(p.ingredientsList) LIKE LOWER(CONCAT('%', :tag, '%'))")
    Page<Product> findByProductTypeAndTagsContainingIgnoreCase(@Param("productType") String productType, @Param("tag") String tag, Pageable pageable);
    
    // Find all products with pagination (already provided by JpaRepository)
    // Page<Product> findAll(Pageable pageable);
}

