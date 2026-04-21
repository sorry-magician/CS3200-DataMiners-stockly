import streamlit as st


def home_nav():
    st.sidebar.page_link("Home.py", label="Home")


# ---- Role: store_owner (Maya Chen)

def store_owner_home_nav():
    st.sidebar.page_link(
        "pages/10_Store_Owner_Home.py",
        label="Store Owner Home"
    )

def inventory_dashboard_nav():
    st.sidebar.page_link(
        "pages/11_Inventory_Dashboard.py",
        label="Inventory Dashboard"
    )

def product_management_nav():
    st.sidebar.page_link(
        "pages/12_Product_Management.py",
        label="Product Management"
    )

def overstock_analysis_nav():
    st.sidebar.page_link(
        "pages/13_Overstock_Analysis.py",
        label="Overstock Analysis"
    )


# ---- Role: inventory_manager (Jordan Patel)

def inventory_manager_home_nav():
    st.sidebar.page_link(
        "pages/20_Inventory_Manager_Home.py",
        label="Inventory Manager Home"
    )

def purchase_orders_nav():
    st.sidebar.page_link(
        "pages/20_Purchase_Orders.py",
        label="Purchase Orders"
    )

def inventory_search_nav():
    st.sidebar.page_link(
        "pages/21_Inventory_Search.py",
        label="Inventory Search"
    )

def stock_management_nav():
    st.sidebar.page_link(
        "pages/22_Stock_Management.py",
        label="Stock Management"
    )


# ---- Role: analyst (Priya Nair)

def analyst_home_nav():
    st.sidebar.page_link(
        "pages/30_Analyst_Home.py",
        label="Analyst Home"
    )

def revenue_dashboard_nav():
    st.sidebar.page_link(
        "pages/31_Revenue_Dashboard.py",
        label="Revenue Dashboard"
    )

def product_performance_nav():
    st.sidebar.page_link(
        "pages/32_Product_Performance.py",
        label="Product Performance"
    )

def supplier_analysis_nav():
    st.sidebar.page_link(
        "pages/33_Supplier_Analysis.py",
        label="Supplier Analysis"
    )


# ---- Role: administrator (Alex Torres)

def admin_home_nav():
    st.sidebar.page_link(
        "pages/40_Admin_Home.py",
        label="Admin Home"
    )

def user_management_nav():
    st.sidebar.page_link(
        "pages/41_User_Management.py",
        label="User Management"
    )

def audit_log_nav():
    st.sidebar.page_link(
        "pages/42_Audit_Log.py",
        label="Audit Log"
    )

def system_config_nav():
    st.sidebar.page_link(
        "pages/43_System_Config.py",
        label="System Config"
    )


# ---- Sidebar assembly

def SideBarLinks(show_home=False):
    st.sidebar.markdown("## Stockly")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        home_nav()

    if st.session_state["authenticated"]:

        if st.session_state["role"] == "store_owner":
            store_owner_home_nav()
            inventory_dashboard_nav()
            product_management_nav()
            overstock_analysis_nav()

        if st.session_state["role"] == "inventory_manager":
            inventory_manager_home_nav()
            purchase_orders_nav()
            inventory_search_nav()
            stock_management_nav()

        if st.session_state["role"] == "analyst":
            analyst_home_nav()
            revenue_dashboard_nav()
            product_performance_nav()
            supplier_analysis_nav()

        if st.session_state["role"] == "administrator":
            admin_home_nav()
            user_management_nav()
            audit_log_nav()
            system_config_nav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")