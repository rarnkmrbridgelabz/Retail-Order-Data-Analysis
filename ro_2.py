import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns

# Set seaborn style for better visuals
sns.set_theme(style="whitegrid")

# Function to fetch data from MySQL
def get_data(query):
    conn = pymysql.connect(host="localhost", user="root", password="root", database="retail_orders")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Define all 20 queries
queries = {
    "1. Top 10 highest revenue-generating products": """SELECT p.product_id, SUM(p.total_revenue) AS total_revenue 
                                                        FROM products p 
                                                        JOIN orders o ON p.product_id = o.product_id 
                                                        GROUP BY p.product_id 
                                                        ORDER BY total_revenue DESC 
                                                        LIMIT 10;""",

    "2. Top 5 cities with highest profit margins": """SELECT o.city, (SUM(p.profit) / SUM(p.total_revenue)) * 100 AS profit_margin 
                                                       FROM orders o 
                                                       JOIN products p ON o.product_id = p.product_id 
                                                       GROUP BY o.city 
                                                       ORDER BY profit_margin DESC 
                                                       LIMIT 5;""",

    "3. Total discount given for each category": """SELECT p.category, SUM(p.discount_amount) AS total_discount 
                                                     FROM products p 
                                                     GROUP BY p.category;""",

    "4. Average sale price per product category": """SELECT p.category, AVG(p.sale_price) AS avg_sale_price 
                                                      FROM products p 
                                                      GROUP BY p.category;""",

    "5. Region with the highest average sale price": """SELECT o.region, AVG(p.sale_price) AS avg_sale_price 
                                                         FROM orders o 
                                                         JOIN products p ON o.product_id = p.product_id 
                                                         GROUP BY o.region 
                                                         ORDER BY avg_sale_price DESC 
                                                         LIMIT 1;""",

    "6. Total profit per category": """SELECT p.category, SUM(p.profit) AS total_profit 
                                       FROM products p 
                                       GROUP BY p.category;""",

    "7. Top 3 segments with highest quantity of orders": """SELECT o.segment, SUM(o.quantity) AS total_quantity 
                                                             FROM orders o 
                                                             GROUP BY o.segment 
                                                             ORDER BY total_quantity DESC 
                                                             LIMIT 3;""",

    "8. Average discount percentage given per region": """SELECT o.region, AVG(p.discount_percent) AS avg_discount 
                                                           FROM orders o 
                                                           JOIN products p ON o.product_id = p.product_id 
                                                           GROUP BY o.region;""",

    "9. Product category with highest total profit": """SELECT p.category, SUM(p.profit) AS total_profit 
                                                         FROM products p 
                                                         GROUP BY p.category 
                                                         ORDER BY total_profit DESC 
                                                         LIMIT 1;""",

    "10. Total revenue generated per year": """SELECT YEAR(o.order_date) AS year, SUM(p.total_revenue) AS total_revenue 
                                                FROM orders o 
                                                JOIN products p ON o.product_id = p.product_id 
                                                GROUP BY YEAR(o.order_date) 
                                                ORDER BY year;""",

    "11. Top 5 products with highest discount percentage": """SELECT p.product_id, p.category, p.sub_category, 
                                                                   (p.discount_amount / p.list_price) * 100 AS discount_ratio 
                                                              FROM products p 
                                                              ORDER BY discount_ratio DESC 
                                                              LIMIT 5;""",

    "12. Month with highest total revenue and top category": """SELECT MONTH(o.order_date) AS month, p.category, SUM(p.total_revenue) AS total_revenue 
                                                                 FROM orders o 
                                                                 JOIN products p ON o.product_id = p.product_id 
                                                                 GROUP BY month, p.category 
                                                                 ORDER BY total_revenue DESC 
                                                                 LIMIT 1;""",

    "13. City with highest average profit per order": """SELECT o.city, AVG(p.profit) AS avg_profit_per_order 
                                                          FROM orders o 
                                                          JOIN products p ON o.product_id = p.product_id 
                                                          GROUP BY o.city 
                                                          ORDER BY avg_profit_per_order DESC 
                                                          LIMIT 1;""",

    "14. Top 3 states with highest revenue growth": """SELECT o.state, YEAR(o.order_date) AS year, SUM(p.total_revenue) AS total_revenue, 
                                                             LAG(SUM(p.total_revenue)) OVER (PARTITION BY o.state ORDER BY YEAR(o.order_date)) AS prev_year_revenue, 
                                                             (SUM(p.total_revenue) - LAG(SUM(p.total_revenue)) OVER (PARTITION BY o.state ORDER BY YEAR(o.order_date))) AS revenue_growth 
                                                       FROM orders o 
                                                       JOIN products p ON o.product_id = p.product_id 
                                                       GROUP BY o.state, year 
                                                       ORDER BY revenue_growth DESC 
                                                       LIMIT 3;""",

    "15. Segment with most expensive average order": """SELECT o.segment, AVG(p.sale_price * o.quantity) AS avg_order_value 
                                                         FROM orders o 
                                                         JOIN products p ON o.product_id = p.product_id 
                                                         GROUP BY o.segment 
                                                         ORDER BY avg_order_value DESC 
                                                         LIMIT 1;""",

    "16. Top 5 most frequently ordered product categories": """SELECT p.category, COUNT(o.order_id) AS order_count 
                                                                FROM orders o 
                                                                JOIN products p ON o.product_id = p.product_id 
                                                                GROUP BY p.category 
                                                                ORDER BY order_count DESC 
                                                                LIMIT 5;""",

    "17. Top 3 states where profit margin is below 5%": """SELECT o.state, (SUM(p.profit) / SUM(p.total_revenue)) * 100 AS profit_margin 
                                                            FROM orders o 
                                                            JOIN products p ON o.product_id = p.product_id 
                                                            GROUP BY o.state 
                                                            HAVING profit_margin < 5 
                                                            ORDER BY profit_margin ASC 
                                                            LIMIT 3;""",

    "18. Top 5 cities with highest product variety": """SELECT o.city, COUNT(DISTINCT o.product_id) AS unique_products_ordered 
                                                        FROM orders o 
                                                        GROUP BY o.city 
                                                        ORDER BY unique_products_ordered DESC 
                                                        LIMIT 5;""",

    "19. Most discounted product category per region": """SELECT o.region, p.category, AVG(p.discount_percent) AS avg_discount 
                                                           FROM orders o 
                                                           JOIN products p ON o.product_id = p.product_id 
                                                           GROUP BY o.region, p.category 
                                                           ORDER BY avg_discount DESC 
                                                           LIMIT 1;""",

    "20. Top 3 cities with highest cost-to-revenue ratio": """SELECT o.city, (SUM(p.total_cost) / SUM(p.total_revenue)) * 100 AS cost_to_revenue_ratio 
                                                               FROM orders o 
                                                               JOIN products p ON o.product_id = p.product_id 
                                                               GROUP BY o.city 
                                                               ORDER BY cost_to_revenue_ratio DESC 
                                                               LIMIT 3;"""
}

# Streamlit App
st.title("📊 Business Data Insights Dashboard")

# Dropdown selection
selected_query = st.selectbox("🔍 Select a Query", list(queries.keys()))

if selected_query:
    query = queries[selected_query]
    df = get_data(query)

    st.subheader("📌 Query Result")
    st.dataframe(df.style.background_gradient(cmap="Blues"))

    # Visualization
    st.subheader("📊 Visualization")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df, x=df.columns[0], y=df.columns[1], palette="coolwarm", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_title(selected_query, fontsize=14, fontweight="bold")
    st.pyplot(fig)
