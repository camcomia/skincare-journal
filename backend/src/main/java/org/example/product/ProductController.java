package org.example.product;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.logging.Logger;

// ProductController.java
@RestController
@RequestMapping("/api/products")
@CrossOrigin(origins = "http://localhost:3000")
public class ProductController {
    
    private static final Logger logger = Logger.getLogger(ProductController.class.getName());
    
    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private ProductService productService;

    // Legacy endpoint for backward compatibility
    @GetMapping("/all")
    public ResponseEntity<List<Product>> getAllProducts() {
        try {
            List<Product> products = productRepository.findAll();
            logger.info("Retrieved " + products.size() + " products via legacy endpoint");
            return ResponseEntity.ok(products);
        } catch (Exception e) {
            logger.severe("Error retrieving all products: " + e.getMessage());
            return ResponseEntity.internalServerError().build();
        }
    }

    // New paginated endpoint with filtering
    @GetMapping
    public ResponseEntity<PaginatedResponse<Product>> getProducts(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int limit,
            @RequestParam(required = false) String productType,
            @RequestParam(required = false) String tags,
            @RequestParam(required = false) String brand,
            @RequestParam(required = false) String search,
            @RequestParam(required = false) String sortBy) {
        
        try {
            // Validate parameters
            if (page < 1) {
                logger.warning("Invalid page number: " + page + ", setting to 1");
                page = 1;
            }
            if (limit < 1 || limit > 100) {
                logger.warning("Invalid limit: " + limit + ", setting to 10");
                limit = 10;
            }
            
            // Log the request for debugging
            logger.info(String.format("Fetching products - Page: %d, Limit: %d, Type: %s, Tags: %s, Brand: %s, Search: %s, Sort: %s", 
                page, limit, productType != null ? productType : "null", tags != null ? tags : "null", 
                brand != null ? brand : "null", search != null ? search : "null", sortBy != null ? sortBy : "null"));
            
            Pageable pageable = PageRequest.of(page - 1, limit); // Spring Data uses 0-based indexing
            Page<Product> productPage = productService.findProductsWithFilters(pageable, productType, tags, brand, search, sortBy);
            
            PaginatedResponse<Product> response = new PaginatedResponse<>(
                productPage.getContent(),
                productPage.getTotalElements(),
                page,
                limit,
                productPage.getTotalPages()
            );
            
            logger.info(String.format("Returning %d products (page %d of %d, total: %d)", 
                productPage.getContent().size(), page, productPage.getTotalPages(), productPage.getTotalElements()));
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.severe("Error fetching products: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<Product> getProduct(@PathVariable Long id) {
        try {
            return productRepository.findById(id)
                    .map(product -> {
                        logger.info("Retrieved product with ID: " + id);
                        return ResponseEntity.ok(product);
                    })
                    .orElseGet(() -> {
                        logger.warning("Product not found with ID: " + id);
                        return ResponseEntity.notFound().build();
                    });
        } catch (Exception e) {
            logger.severe("Error retrieving product with ID " + id + ": " + e.getMessage());
            return ResponseEntity.internalServerError().build();
        }
    }

    @PostMapping
    public ResponseEntity<Product> createProduct(@RequestBody Product product) {
        try {
            if (product == null) {
                logger.warning("Attempted to create null product");
                return ResponseEntity.badRequest().build();
            }
            
            Product savedProduct = productRepository.save(productService.titleCaseProduct(product));
            logger.info("Created new product with ID: " + savedProduct.getId());
            return ResponseEntity.ok(savedProduct);
        } catch (Exception e) {
            logger.severe("Error creating product: " + e.getMessage());
            return ResponseEntity.internalServerError().build();
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<Product> updateProduct(@PathVariable Long id, @RequestBody Product product) {
        try {
            if (product == null) {
                logger.warning("Attempted to update product with null data for ID: " + id);
                return ResponseEntity.badRequest().build();
            }
            
            if (!productRepository.existsById(id)) {
                logger.warning("Attempted to update non-existent product with ID: " + id);
                return ResponseEntity.notFound().build();
            }
            
            product.setId(id);
            Product updatedProduct = productRepository.save(productService.titleCaseProduct(product));
            logger.info("Updated product with ID: " + id);
            return ResponseEntity.ok(updatedProduct);
        } catch (Exception e) {
            logger.severe("Error updating product with ID " + id + ": " + e.getMessage());
            return ResponseEntity.internalServerError().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        try {
            if (!productRepository.existsById(id)) {
                logger.warning("Attempted to delete non-existent product with ID: " + id);
                return ResponseEntity.notFound().build();
            }
            
            productRepository.deleteById(id);
            logger.info("Deleted product with ID: " + id);
            return ResponseEntity.ok().build();
        } catch (Exception e) {
            logger.severe("Error deleting product with ID " + id + ": " + e.getMessage());
            return ResponseEntity.internalServerError().build();
        }
    }

    // Test endpoint for debugging filter functionality
    @GetMapping("/test-filters")
    public ResponseEntity<String> testFilters(
            @RequestParam(required = false) String productType,
            @RequestParam(required = false) String tags) {
        
        try {
            StringBuilder result = new StringBuilder();
            result.append("Filter Test Results:\n");
            result.append("==================\n");
            result.append("Product Type: ").append(productType != null ? productType : "null").append("\n");
            result.append("Tags: ").append(tags != null ? tags : "null").append("\n\n");
            
            // Get all products for testing
            List<Product> allProducts = productRepository.findAll();
            result.append("Total products in database: ").append(allProducts.size()).append("\n\n");
            
            // Test tag matching on first few products
            int testCount = Math.min(5, allProducts.size());
            result.append("Testing tag matching on first ").append(testCount).append(" products:\n");
            
            for (int i = 0; i < testCount; i++) {
                Product product = allProducts.get(i);
                boolean matches = productService.productMatchesTags(product, tags);
                result.append(String.format("%d. %s (ID: %d) - Matches: %s\n", 
                    i + 1, product.getName(), product.getId(), matches ? "YES" : "NO"));
            }
            
            logger.info("Filter test completed for type: " + productType + ", tags: " + tags);
            return ResponseEntity.ok(result.toString());
        } catch (Exception e) {
            logger.severe("Error in filter test: " + e.getMessage());
            return ResponseEntity.internalServerError().body("Error: " + e.getMessage());
        }
    }

    // Get unique brands for dropdown
    @GetMapping("/brands")
    public ResponseEntity<List<String>> getBrands() {
        try {
            List<String> brands = productService.getUniqueBrands();
            logger.info("Returning " + brands.size() + " unique brands");
            return ResponseEntity.ok(brands);
        } catch (Exception e) {
            logger.severe("Error fetching brands: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.badRequest().build();
        }
    }
}
