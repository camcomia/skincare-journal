package org.example.product;

import java.util.List;

public class PaginatedResponse<T> {
    private List<T> products;
    private long total;
    private int page;
    private int limit;
    private int totalPages;

    public PaginatedResponse(List<T> products, long total, int page, int limit, int totalPages) {
        this.products = products;
        this.total = total;
        this.page = page;
        this.limit = limit;
        this.totalPages = totalPages;
    }

    // Getters
    public List<T> getProducts() {
        return products;
    }

    public long getTotal() {
        return total;
    }

    public int getPage() {
        return page;
    }

    public int getLimit() {
        return limit;
    }

    public int getTotalPages() {
        return totalPages;
    }

    // Setters
    public void setProducts(List<T> products) {
        this.products = products;
    }

    public void setTotal(long total) {
        this.total = total;
    }

    public void setPage(int page) {
        this.page = page;
    }

    public void setLimit(int limit) {
        this.limit = limit;
    }

    public void setTotalPages(int totalPages) {
        this.totalPages = totalPages;
    }
}
