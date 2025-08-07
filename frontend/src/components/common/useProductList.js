import { useState, useEffect, useCallback, useRef } from 'react';

const API_BASE_URL = 'http://localhost:8080/api/products';
const PAGE_SIZE = 20;

export const useProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedIngredients, setExpandedIngredients] = useState({});
  const [showScrollUp, setShowScrollUp] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [totalProducts, setTotalProducts] = useState(0);
  const [totalProductsInSystem, setTotalProductsInSystem] = useState(0);
  const [isFirstLoad, setIsFirstLoad] = useState(true);
  const [isApplyingFilters, setIsApplyingFilters] = useState(false);
  const [activeFilters, setActiveFilters] = useState({ 
    productType: '', 
    tags: [],
    brand: '',
    search: '',
    sortBy: 'name'
  });
  const [brands, setBrands] = useState([]);
  const [brandsLoaded, setBrandsLoaded] = useState(false);
  const [searchInputValue, setSearchInputValue] = useState('');
  
  // Add refs to prevent duplicate calls and race conditions
  const isLoadingRef = useRef(false);
  const hasMoreRef = useRef(true);
  const scrollTimeoutRef = useRef(null);
  const lastRequestedPageRef = useRef(0);
  const productsCountRef = useRef(0);
  
  // Fetch brands for dropdown (only once)
  const fetchBrands = useCallback(async () => {
    if (brandsLoaded) return; // Prevent multiple calls
    
    try {
      const response = await fetch(`${API_BASE_URL}/brands`);
      if (response.ok) {
        const brandsData = await response.json();
        setBrands(brandsData);
        setBrandsLoaded(true);
      }
    } catch (error) {
      console.error('Error fetching brands:', error);
    }
  }, [brandsLoaded]);

  // Update refs when state changes
  useEffect(() => {
    isLoadingRef.current = loadingMore;
    hasMoreRef.current = hasMore;
  }, [loadingMore, hasMore]);

  // Sync search input value with active filters
  useEffect(() => {
    setSearchInputValue(activeFilters.search);
  }, [activeFilters.search]);

  // Fetch products with better error handling and robust hasMore logic
  const fetchProducts = useCallback(async (page = 1, isInitial = false, filters = null) => {
    if (page === lastRequestedPageRef.current && !isInitial) {
      return;
    }
    try {
      if (isInitial && isFirstLoad) {
        setLoading(true);
        setError(null);
        lastRequestedPageRef.current = 0;
      } else if (!isInitial) {
        setLoadingMore(true);
        isLoadingRef.current = true;
      }
      lastRequestedPageRef.current = page;
      const currentFilters = filters || activeFilters;
      const params = new URLSearchParams({
        page: page.toString(),
        limit: PAGE_SIZE.toString(),
        ...(currentFilters.productType && { productType: currentFilters.productType }),
        ...(currentFilters.tags.length > 0 && { tags: currentFilters.tags.join(',') }),
        ...(currentFilters.brand && { brand: currentFilters.brand }),
        ...(currentFilters.search && { search: currentFilters.search }),
        ...(currentFilters.sortBy && { sortBy: currentFilters.sortBy })
      });
      const response = await fetch(`${API_BASE_URL}?${params}`);
      if (response.ok) {
        const data = await response.json();
        const productsData = data.products || data;
        if (isInitial) {
          setProducts(productsData);
          productsCountRef.current = productsData.length;
          setTotalProducts(data.total || productsData.length);
          // Store the total products in system when no filters are applied
          if (!currentFilters.productType && currentFilters.tags.length === 0 && !currentFilters.brand && !currentFilters.search) {
            setTotalProductsInSystem(data.total || productsData.length);
          }
          setCurrentPage(1);
          setIsFirstLoad(false); // Mark first load as complete
        } else {
          setProducts(prev => {
            const updated = [...prev, ...productsData];
            productsCountRef.current = updated.length;
            return updated;
          });
          setCurrentPage(page);
        }
        // Debugging logs
        console.log('Fetched page:', page, 'Products this page:', productsData.length, 'Total from API:', data.total, 'TotalPages:', data.totalPages, 'CurrentPage:', data.page, 'productsCountRef:', productsCountRef.current);
        // Use API's totalPages and page to determine hasMore
        const newHasMore = data.totalPages ? page < data.totalPages : (productsCountRef.current < (data.total || totalProducts));
        setHasMore(newHasMore);
        hasMoreRef.current = newHasMore;
      } else {
        throw new Error('Failed to fetch products');
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Failed to fetch products');
    } finally {
      setLoading(false);
      setLoadingMore(false);
      isLoadingRef.current = false;
    }
  }, [activeFilters, totalProducts, isFirstLoad]);

  // Load more products with strict guards
  const loadMoreProducts = useCallback(async () => {
    // Multiple guards to prevent duplicate calls
    if (isLoadingRef.current || !hasMoreRef.current) {
      return;
    }
    
    const nextPage = currentPage + 1;
    if (nextPage === lastRequestedPageRef.current) {
      return; // Already requested this page
    }
    
    isLoadingRef.current = true;
    setLoadingMore(true);
    await fetchProducts(nextPage, false);
  }, [currentPage, fetchProducts]);

  // Debounced scroll handler with longer timeout
  const handleScroll = useCallback(() => {
    // Clear existing timeout
    if (scrollTimeoutRef.current) {
      clearTimeout(scrollTimeoutRef.current);
    }

    // Show/hide scroll to top button
    if (window.scrollY > 300) setShowScrollUp(true);
    else setShowScrollUp(false);
    
    // Debounced scroll detection with longer timeout
    scrollTimeoutRef.current = setTimeout(() => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;
      
      if (scrollTop + windowHeight >= documentHeight - 200) {
        loadMoreProducts();
      }
    }, 200);
  }, [loadMoreProducts]);

  // Apply filters with reset
  const applyFilters = useCallback(async (newFilters) => {
    try {
      setError(null);
      setCurrentPage(1);
      setHasMore(true);
      hasMoreRef.current = true;
      lastRequestedPageRef.current = 0; // Reset page tracking
      setActiveFilters(newFilters);
      setIsApplyingFilters(true);
      // Don't set loading to true immediately - keep existing products visible
      await fetchProducts(1, true, newFilters);
    } catch (error) {
      console.error('Error applying filters:', error);
      setError('Failed to apply filters');
    } finally {
      setIsApplyingFilters(false);
    }
  }, []);

  // Search handler that only updates the input value without triggering search
  const handleSearchChange = useCallback((searchTerm) => {
    // Only update the input value, don't trigger search
    setSearchInputValue(searchTerm);
  }, []);

  // Handle search submission (when user presses Enter or leaves the field)
  const handleSearchSubmit = useCallback((searchTerm) => {
    const newFilters = {
      ...activeFilters,
      search: searchTerm.trim()
    };
    applyFilters(newFilters);
    setSearchInputValue(searchTerm.trim()); // Sync the input value
  }, [activeFilters]);

  // Clear search with immediate feedback
  const clearSearch = useCallback(() => {
    const newFilters = {
      ...activeFilters,
      search: ''
    };
    applyFilters(newFilters);
    setSearchInputValue(''); // Clear the input value
  }, [activeFilters]);

  // Event handlers
  const handleProductTypeChange = useCallback((e) => {
    const newFilters = {
      ...activeFilters,
      productType: e.target.value
    };
    applyFilters(newFilters);
  }, [activeFilters]);

  const handleBrandChange = useCallback((e) => {
    const newFilters = {
      ...activeFilters,
      brand: e.target.value
    };
    applyFilters(newFilters);
  }, [activeFilters]);

  const handleSortChange = useCallback((e) => {
    const newFilters = {
      ...activeFilters,
      sortBy: e.target.value
    };
    applyFilters(newFilters);
  }, [activeFilters]);

  const handleTagToggle = useCallback((tag) => {
    const newTags = activeFilters.tags.includes(tag)
      ? activeFilters.tags.filter(t => t !== tag)
      : [...activeFilters.tags, tag];
    
    const newFilters = {
      ...activeFilters,
      tags: newTags
    };
    applyFilters(newFilters);
  }, [activeFilters]);

  const clearFilters = useCallback(() => {
    applyFilters({ 
      productType: '', 
      tags: [], 
      brand: '', 
      search: '', 
      sortBy: 'name' 
    });
  }, []);

  const toggleIngredients = useCallback((id) => {
    setExpandedIngredients(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  }, []);

  const deleteProduct = useCallback(async (id) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        const response = await fetch(`${API_BASE_URL}/${id}`, { method: 'DELETE' });
        
        if (response.ok) {
          alert('Product deleted successfully!');
          fetchProducts(1, true);
        } else {
          alert('Error deleting product');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Error deleting product');
      }
    }
  }, [fetchProducts]);

  const scrollToTop = useCallback(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  // Set up scroll listener
  useEffect(() => {
    window.addEventListener('scroll', handleScroll, { passive: true });
    
    return () => {
      if (scrollTimeoutRef.current) {
        clearTimeout(scrollTimeoutRef.current);
      }
    };
  }, [handleScroll]);

  // Initial data fetch
  useEffect(() => {
    fetchBrands();
    fetchProducts(1, true);
  }, [fetchBrands, fetchProducts]);

  return {
    // State
    products,
    loading,
    error,
    expandedIngredients,
    showScrollUp,
    currentPage,
    hasMore,
    loadingMore,
    totalProducts,
    totalProductsInSystem,
    isFirstLoad,
    isApplyingFilters,
    activeFilters,
    brands,
    brandsLoaded,
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
    scrollToTop,
    fetchProducts
  };
};
