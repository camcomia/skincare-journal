// Filter Options Constants
export const PRODUCT_TYPES = [
  'Cleanser',
  'Toner', 
  'Booster',
  'Emulsion',
  'Moisturizer',
  'Ampoule',
  'Treatment',
  'Mask',
  'Sunscreen',
  'Serum',
  'Essence',
  'Eye Cream',
  'Lip Care',
  'Body Care',
  'Other'
];

export const SORT_OPTIONS = [
  { value: 'name', label: 'Name A-Z' },
  { value: 'name-desc', label: 'Name Z-A' },
  { value: 'price', label: 'Price Low-High' },
  { value: 'price-desc', label: 'Price High-Low' },
  { value: 'brand', label: 'Brand' },
  { value: 'date', label: 'Date Added' }
];

export const AVAILABLE_TAGS = [
  'alcohol-free',
  'fragrance-free', 
  'oil-free',
  'sensitive skin friendly'
];

// Filter validation helpers
export const isValidProductType = (type) => PRODUCT_TYPES.includes(type);
export const isValidSortOption = (sort) => SORT_OPTIONS.some(option => option.value === sort);
export const isValidTag = (tag) => AVAILABLE_TAGS.includes(tag);

// Filter display helpers
export const getProductTypeLabel = (type) => type || 'All Types';
export const getSortOptionLabel = (sort) => {
  const option = SORT_OPTIONS.find(opt => opt.value === sort);
  return option ? option.label : 'Sort by';
};
export const getTagLabel = (tag) => tag.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
