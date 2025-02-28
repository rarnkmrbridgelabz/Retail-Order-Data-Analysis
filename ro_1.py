import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns

def get_data(query):
    # Connect to database (Replace with your actual database connection)
    conn = pymysql.connect(host="localhost", user="root", password="root", database="retail_orders")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Define query dictionary
queries = {
    "1. Top 10 highest revenue-generating products": "SELECT product_id, SUM(total_revenue) AS total_revenue FROM ro_table GROUP BY product_id ORDER BY total_revenue DESC LIMIT 10;",
    "2. Top 5 cities with highest profit margins": "SELECT city, (SUM(profit) / SUM(total_revenue)) * 100 AS profit_margin FROM ro_table GROUP BY city ORDER BY profit_margin DESC LIMIT 5;",
    "3. Total discount given for each category": "SELECT category, SUM(discount_amount) AS total_discount FROM ro_table GROUP BY category;",
    "4. Average sale price per product category": "SELECT category, AVG(sale_price) AS avg_sale_price FROM ro_table GROUP BY category;",
    "5. Region with the highest average sale price": "SELECT region, AVG(sale_price) AS avg_sale_price FROM ro_table GROUP BY region ORDER BY avg_sale_price DESC LIMIT 1;",
    "6. Total profit per category": "SELECT category, SUM(profit) AS total_profit FROM ro_table GROUP BY category;",
    "7. Top 3 segments with highest quantity of orders": "SELECT segment, SUM(quantity) AS total_quantity FROM ro_table GROUP BY segment ORDER BY total_quantity DESC LIMIT 3;",
    "8. Average discount percentage given per region": "SELECT region, AVG(discount_percent) AS avg_discount FROM ro_table GROUP BY region;",
    "9. Product category with highest total profit": "SELECT category, SUM(profit) AS total_profit FROM ro_table GROUP BY category ORDER BY total_profit DESC LIMIT 1;",
    "10. Total revenue generated per year": "SELECT YEAR(order_date) AS year, SUM(total_revenue) AS total_revenue FROM ro_table GROUP BY YEAR(order_date) ORDER BY year;"
}

# Streamlit App
st.title("🌟 Business Data Insights 🌟")
st.markdown("## 📊 Data Analysis Dashboard")
st.markdown("---")
st.markdown("<style>body {background-color: #f0f2f6;}</style>", unsafe_allow_html=True)

# Dropdown selection
selected_query = st.selectbox("🎯 Select a Query", list(queries.keys()))

if selected_query:
    query = queries[selected_query]
    df = get_data(query)
    
    st.subheader("📌 Query Result")
    st.dataframe(df.style.set_properties(**{'background-color': '#e8f4fc', 'color': 'black', 'border-color': 'white'}))
    
    # Visualization
    st.subheader("🎨 Visualization")
    sns.set_palette("pastel")  # Set color palette
    
    if "revenue" in selected_query.lower() or "profit" in selected_query.lower():
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df, x=df.columns[0], y=df.columns[1], ax=ax, palette="coolwarm")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_title(selected_query, fontsize=14, color="blue")
        ax.set_ylabel("Value", fontsize=12, color="darkred")
        st.pyplot(fig)
    
    elif "discount" in selected_query.lower():
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(df[df.columns[1]], labels=df[df.columns[0]], autopct='%1.1f%%', startangle=140, colors=sns.color_palette("coolwarm"))
        ax.set_title(selected_query, fontsize=14, color="purple")
        st.pyplot(fig)
    
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df, x=df.columns[0], y=df.columns[1], ax=ax, palette="viridis")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_title(selected_query, fontsize=14, color="green")
        ax.set_ylabel("Value", fontsize=12, color="darkblue")
        st.pyplot(fig)
