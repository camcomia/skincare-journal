package org.example.product;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;
import java.util.stream.Collectors;
import java.util.ArrayList;
import org.springframework.data.domain.PageImpl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class ProductService {

    private static final Logger logger = LoggerFactory.getLogger(ProductService.class);

    @Autowired
    private ProductRepository productRepository;

    public String toTitleCase(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        return Arrays.stream(input.toLowerCase().split(" "))
                .map(word -> !word.isEmpty()
                        ? Character.toUpperCase(word.charAt(0)) + word.substring(1)
                        : word)
                .collect(Collectors.joining(" "));
    }

    public Product titleCaseProduct(Product product){
        product.setIngredientsList(toTitleCase(product.getIngredientsList()));
        product.setStarIngredients(toTitleCase(product.getStarIngredients()));

        return product;
    }

    public Page<Product> findProductsWithFilters(Pageable pageable, String productType, String tags, String brand, String search, String sortBy) {
        logger.info("Finding products with filters - Type: " + productType + ", Tags: " + tags + ", Brand: " + brand + ", Search: " + search + ", Sort: " + sortBy);
        
        List<Product> allProducts = productRepository.findAll();
        List<Product> filteredProducts = new ArrayList<>();
        
        // Apply filters
        for (Product product : allProducts) {
            boolean matchesFilters = true;
            
            // Brand filter
            if (brand != null && !brand.trim().isEmpty()) {
                if (!product.getBrand().equalsIgnoreCase(brand.trim())) {
                    matchesFilters = false;
                }
            }
            
            // Search filter (search in name, brand, and ingredients)
            if (search != null && !search.trim().isEmpty()) {
                String searchLower = search.toLowerCase().trim();
                String productName = product.getName() != null ? product.getName().toLowerCase() : "";
                String productBrand = product.getBrand() != null ? product.getBrand().toLowerCase() : "";
                String productIngredients = product.getIngredientsList() != null ? product.getIngredientsList().toLowerCase() : "";
                
                if (!productName.contains(searchLower) && 
                    !productBrand.contains(searchLower) && 
                    !productIngredients.contains(searchLower)) {
                    matchesFilters = false;
                }
            }
            
            // Product type filter
            if (productType != null && !productType.trim().isEmpty()) {
                if (!product.getProductType().equalsIgnoreCase(productType.trim())) {
                    matchesFilters = false;
                }
            }
            
            // Tags filter
            if (tags != null && !tags.trim().isEmpty() && matchesFilters) {
                String[] tagArray = tags.split(",");
                logger.info("Processing tags: " + tags + " for product: " + product.getName());
                
                for (String tag : tagArray) {
                    String tagTrimmed = tag.trim();
                    boolean productMatchesTag = false;
                    
                    // Use the same tag detection logic as the frontend
                    switch (tagTrimmed.toLowerCase()) {
                        case "alcohol-free":
                            productMatchesTag = !containsBadAlcohol(product.getIngredientsList());
                            logger.info("Alcohol-free check for " + product.getName() + ": " + productMatchesTag);
                            break;
                        case "fragrance-free":
                            productMatchesTag = !containsFragrance(product.getIngredientsList());
                            logger.info("Fragrance-free check for " + product.getName() + ": " + productMatchesTag);
                            break;
                        case "oil-free":
                            boolean hasOilInIngredients = containsOil(product.getIngredientsList());
                            boolean hasOilInName = productNameContainsOil(product.getName());
                            productMatchesTag = !hasOilInIngredients && !hasOilInName;
                            logger.info("Oil-free check for " + product.getName() + ": ingredients=" + hasOilInIngredients + ", name=" + hasOilInName + ", result=" + productMatchesTag);
                            break;
                        case "sensitive skin friendly":
                            boolean hasIrritants = containsSensitiveSkinIrritants(product.getIngredientsList());
                            boolean hasOil = containsOil(product.getIngredientsList()) || productNameContainsOil(product.getName());
                            productMatchesTag = !hasIrritants && !hasOil;
                            logger.info("Sensitive skin friendly check for " + product.getName() + ": irritants=" + hasIrritants + ", oil=" + hasOil + ", result=" + productMatchesTag);
                            break;
                        default:
                            productMatchesTag = false;
                            logger.info("Unknown tag: " + tagTrimmed);
                            break;
                    }
                    
                    if (!productMatchesTag) {
                        matchesFilters = false;
                        logger.info("Product " + product.getName() + " does not match tag: " + tagTrimmed);
                        break;
                    }
                }
            }
            
            if (matchesFilters) {
                filteredProducts.add(product);
            }
        }
        
        // Apply sorting
        if (sortBy != null && !sortBy.trim().isEmpty()) {
            sortProducts(filteredProducts, sortBy);
        }
        
        // Apply pagination manually
        int totalElements = filteredProducts.size();
        int totalPages = (int) Math.ceil((double) totalElements / pageable.getPageSize());
        int startIndex = (int) pageable.getOffset();
        int endIndex = Math.min(startIndex + pageable.getPageSize(), totalElements);
        
        List<Product> pageContent = new ArrayList<>();
        if (startIndex < totalElements) {
            pageContent = filteredProducts.subList(startIndex, endIndex);
        }
        
        logger.info("Filtered products: " + filteredProducts.size() + ", Page content: " + pageContent.size() + ", Total pages: " + totalPages);
        
        return new PageImpl<>(pageContent, pageable, totalElements);
    }
    
    private void sortProducts(List<Product> products, String sortBy) {
        switch (sortBy.toLowerCase()) {
            case "name":
                products.sort((p1, p2) -> p1.getName().compareToIgnoreCase(p2.getName()));
                break;
            case "name-desc":
                products.sort((p1, p2) -> p2.getName().compareToIgnoreCase(p1.getName()));
                break;
            case "price":
                products.sort((p1, p2) -> {
                    double price1 = p1.getPrice() != null ? p1.getPrice() : 0;
                    double price2 = p2.getPrice() != null ? p2.getPrice() : 0;
                    return Double.compare(price1, price2);
                });
                break;
            case "price-desc":
                products.sort((p1, p2) -> {
                    double price1 = p1.getPrice() != null ? p1.getPrice() : 0;
                    double price2 = p2.getPrice() != null ? p2.getPrice() : 0;
                    return Double.compare(price2, price1);
                });
                break;
            case "brand":
                products.sort((p1, p2) -> p1.getBrand().compareToIgnoreCase(p2.getBrand()));
                break;
            case "date":
                products.sort((p1, p2) -> {
                    if (p1.getId() != null && p2.getId() != null) {
                        return p1.getId().compareTo(p2.getId()); // Assuming ID reflects creation order
                    }
                    return 0;
                });
                break;
            default:
                // Default to name sorting
                products.sort((p1, p2) -> p1.getName().compareToIgnoreCase(p2.getName()));
                break;
        }
    }

    /**
     * Advanced tag matching logic that matches frontend expectations
     */
    public boolean productMatchesTags(Product product, String tags) {
        if (tags == null || tags.isEmpty()) {
            return true;
        }
        
        String[] tagArray = tags.split(",");
        String ingredients = product.getIngredientsList().toLowerCase();
        
        for (String tag : tagArray) {
            String trimmedTag = tag.trim();
            
            switch (trimmedTag.toLowerCase()) {
                case "alcohol-free":
                    if (containsBadAlcohol(ingredients)) return false;
                    break;
                case "fragrance-free":
                    if (containsFragrance(ingredients)) return false;
                    break;
                case "oil-free":
                    if (containsOil(ingredients)) return false;
                    break;
                case "sensitive skin friendly":
                    if (containsSensitiveSkinIrritants(ingredients) || containsOil(ingredients)) return false;
                    break;
                default:
                    // For any other tags, do a simple contains check
                    if (!ingredients.contains(trimmedTag.toLowerCase())) {
                        return false;
                    }
                    break;
            }
        }
        return true;
    }

    /**
     * Check if ingredients contain bad alcohols
     */
    private boolean containsBadAlcohol(String ingredients) {
        if (ingredients == null || ingredients.isEmpty()) {
            return false;
        }
        
        String ingredientsLower = ingredients.toLowerCase();
        
        // More specific alcohol detection to avoid false positives
        String[] badAlcohols = {
            "alcohol denat", "ethanol", "ethyl alcohol", "isopropyl alcohol", 
            "denatured alcohol", "sd alcohol", "alcohol denatured"
        };
        
        for (String alcohol : badAlcohols) {
            if (ingredientsLower.contains(alcohol)) {
                return true;
            }
        }
        
        // Check for standalone "alcohol" but not as part of other words
        if (ingredientsLower.contains(" alcohol") || ingredientsLower.contains(",alcohol")) {
            return true;
        }
        
        return false;
    }

    /**
     * Check if ingredients contain fragrances
     */
    private boolean containsFragrance(String ingredients) {
        if (ingredients == null || ingredients.isEmpty()) {
            return false;
        }
        
        String ingredientsLower = ingredients.toLowerCase();
        
        String[] fragrances = {
            "fragrance", "parfum", "perfume", "aroma", "essential oil"
        };
        
        for (String fragrance : fragrances) {
            if (ingredientsLower.contains(fragrance)) {
                return true;
            }
        }
        
        return false;
    }

    /**
     * Check if ingredients contain oils
     */
    private boolean containsOil(String ingredients) {
        if (ingredients == null || ingredients.isEmpty()) {
            return false;
        }
        
        String ingredientsLower = ingredients.toLowerCase();
        
        // Look for individual oil-related words
        String[] oilWords = {
            "argan", "marula", "rosehip", "borage", "chia", "sea-buckthorn", 
            "squalane", "jojoba", "coconut", "olive", "almond", "sunflower",
            "grapeseed", "castor", "mineral oil", "paraffin oil", "petroleum"
        };
        
        for (String oilWord : oilWords) {
            if (ingredientsLower.contains(oilWord)) {
                return true;
            }
        }
        
        // Also check for standalone "oil" but be more careful
        if (ingredientsLower.contains(" oil") || ingredientsLower.contains(",oil")) {
            return true;
        }
        
        return false;
    }
    
    private boolean productNameContainsOil(String productName) {
        if (productName == null || productName.isEmpty()) {
            logger.info("Product name is null or empty");
            return false;
        }
        
        String nameLower = productName.toLowerCase();
        logger.info("Checking product name for oil: '" + productName + "' -> '" + nameLower + "'");
        
        // Check for oil-related words in product name
        String[] oilWords = {
            "oil", "argan", "marula", "rosehip", "borage", "chia", "sea-buckthorn", 
            "squalane", "jojoba", "coconut", "olive", "almond", "sunflower",
            "grapeseed", "castor"
        };
        
        for (String oilWord : oilWords) {
            if (nameLower.contains(oilWord)) {
                logger.info("Found oil word '" + oilWord + "' in product name '" + productName + "'");
                return true;
            }
        }
        
        logger.info("No oil words found in product name '" + productName + "'");
        return false;
    }

    /**
     * Check if ingredients contain sensitive skin irritants
     */
    private boolean containsSensitiveSkinIrritants(String ingredients) {
        if (ingredients == null || ingredients.isEmpty()) {
            return false;
        }
        
        String ingredientsLower = ingredients.toLowerCase();
        
        String[] irritants = {
            "menthol", "peppermint", "eucalyptus", "camphor", "sodium lauryl sulfate",
            "sls", "sodium laureth sulfate", "sles", "alcohol", "witch hazel"
        };
        
        for (String irritant : irritants) {
            if (ingredientsLower.contains(irritant)) {
                return true;
            }
        }
        
        return false;
    }

    private List<String> getProductTags(String ingredients) {
        List<String> tags = new ArrayList<>();
        if (ingredients == null || ingredients.isEmpty()) {
            return tags;
        }

        String[] ingredientArray = ingredients.toLowerCase().split(",");
        for (String ingredient : ingredientArray) {
            String trimmedIngredient = ingredient.trim();
            if (!trimmedIngredient.isEmpty()) {
                tags.add(trimmedIngredient);
            }
        }
        return tags;
    }

    public List<String> getUniqueBrands() {
        List<Product> allProducts = productRepository.findAll();
        return allProducts.stream()
                .map(Product::getBrand)
                .distinct()
                .sorted()
                .collect(Collectors.toList());
    }
}
