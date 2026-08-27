-- E-COMMERCE DATA ANALYSIS
-- PostgreSQL

-- =====================================================
-- 1. Monthly Revenue Trend
-- =====================================================
SELECT
DATE_TRUNC('month', o.order_date) AS bulan,
SUM(oi.subtotal) AS total_pendapatan
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
WHERE o.order_status = 'Paid'
GROUP BY bulan
ORDER BY bulan;

-- =====================================================
-- 2. Top Selling Products
-- =====================================================
SELECT
p.product_name,
SUM(oi.quantity) AS total_terjual
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_terjual DESC
LIMIT 10;

-- =====================================================
-- 3. Revenue Analysis by Product Category
-- =====================================================
SELECT
    c.category_name,
    SUM(oi.subtotal) AS total_pendapatan
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN categories c
    ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_pendapatan DESC;

-- =====================================================
-- 4. Customer Purchase Frequency
-- =====================================================
SELECT
    c.customer_id,
    c.full_name,
    COUNT(o.order_id) AS total_transaksi,
    SUM(oi.subtotal) AS total_belanja
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.full_name
ORDER BY total_belanja DESC
LIMIT 10;

-- =====================================================
-- 5. Seller Performance
-- =====================================================
SELECT
    s.seller_name,
    COUNT(DISTINCT oi.order_id) AS total_order,
    SUM(oi.subtotal) AS total_pendapatan,
    ROUND(
        SUM(oi.subtotal)::numeric /
        COUNT(DISTINCT oi.order_id),
        2
    ) AS rata_rata_nilai_order
FROM sellers s
JOIN products p
    ON s.seller_id = p.seller_id
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY s.seller_name
ORDER BY total_pendapatan DESC
LIMIT 10;

-- =====================================================
-- 6. Payment Method Analysis
-- =====================================================
SELECT
payment_method,
COUNT(*) AS total_transaksi
FROM payments
WHERE payment_status = 'Paid'
GROUP BY payment_method
ORDER BY total_transaksi DESC;

-- =====================================================
-- 7. Delivery Status Analysis
-- =====================================================
SELECT
shipment_status,
COUNT(*) AS total_pengiriman
FROM shipments
GROUP BY shipment_status
ORDER BY total_pengiriman DESC;
