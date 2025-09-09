import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Customer Purchase Behavior Dashboard", layout="wide")

st.title("🛒 Customer Purchase Behavior Dashboard")

# Inline sample data (no external CSV needed)
data = {
    "OrderID": [1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015],
    "CustomerID": ["C001","C002","C003","C001","C004","C005","C006","C007","C008","C002","C009","C010","C011","C012","C013"],
    "OrderDate": pd.to_datetime([
        "2024-01-05","2024-01-06","2024-01-10","2024-02-15","2024-02-20",
        "2024-03-01","2024-03-05","2024-03-12","2024-04-02","2024-04-08",
        "2024-05-05","2024-05-09","2024-06-01","2024-06-15","2024-06-20"
    ]),
    "Gender": ["Male","Female","Male","Male","Female","Male","Female","Female","Male","Female","Female","Male","Male","Female","Male"],
    "Region": ["North","South","West","North","East","South","North","West","East","South","West","North","South","East","West"],
    "Category": ["Electronics","Fashion","Groceries","Fashion","Electronics",
                 "Groceries","Fashion","Electronics","Groceries","Fashion",
                 "Fashion","Electronics","Groceries","Fashion","Electronics"],
    "Quantity": [1,2,10,1,1,20,3,2,5,1,4,1,15,2,1],
    "UnitPrice": [300,50,5,80,250,4,60,200,10,120,75,400,6,95,500],
}
df = pd.DataFrame(data)
df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]
df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)

# Sidebar filters
st.sidebar.header("🔍 Filters")
region_filter = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())
gender_filter = st.sidebar.multiselect("Select Gender", df["Gender"].unique(), default=df["Gender"].unique())

filtered_df = df[(df["Region"].isin(region_filter)) & (df["Gender"].isin(gender_filter))]

# KPIs
total_revenue = filtered_df["TotalAmount"].sum()
total_customers = filtered_df["CustomerID"].nunique()
avg_order_value = filtered_df["TotalAmount"].mean()
repeat_customers = filtered_df.groupby("CustomerID").size().gt(1).sum()
repeat_pct = (repeat_customers / total_customers * 100) if total_customers > 0 else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
kpi2.metric("👥 Customers", total_customers)
kpi3.metric("📦 Avg Order Value", f"${avg_order_value:,.2f}")
kpi4.metric("🔄 Repeat Customers", f"{repeat_pct:.1f}%")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Top Product Categories")
    top_products = filtered_df.groupby("Category")["TotalAmount"].sum().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(x=top_products.values, y=top_products.index, palette="viridis", ax=ax)
    ax.set_xlabel("Revenue ($)")
    ax.set_ylabel("Category")
    st.pyplot(fig)

with col2:
    st.subheader("📈 Monthly Sales Trend")
    monthly_sales = filtered_df.groupby("Month")["TotalAmount"].sum()
    fig, ax = plt.subplots(figsize=(6,4))
    monthly_sales.plot(kind="line", marker="o", ax=ax)
    ax.set_ylabel("Revenue ($)")
    ax.set_xlabel("Month")
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.subheader("🌍 Customer Segmentation by Region")
region_dist = filtered_df["Region"].value_counts()
fig, ax = plt.subplots(figsize=(6,6))
ax.pie(region_dist.values, labels=region_dist.index, autopct="%1.1f%%", startangle=90, colors=sns.color_palette("Set3"))
st.pyplot(fig)

st.success("✅ Dashboard loaded successfully!")
