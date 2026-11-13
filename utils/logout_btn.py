import streamlit as st
import time
import logging
from utils.auth import logout_user

logger = logging.getLogger(__name__)

def logout_confirmation_modal():
    """
    Modal dialog for logout confirmation
    Handles sleep error and manages state properly
    """
    if st.session_state.get("show_logout_modal", False):
        st.divider()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.container(border=True):
                st.markdown("### 🚪 Confirm Logout")
                st.write("Are you sure you want to logout? Any unsaved interview data will be lost.")
                
                st.divider()
                
                col_yes, col_no = st.columns(2)
                
                with col_yes:
                    if st.button("✅ Logout", key="confirm_logout", use_container_width=True, type="primary"):
                        perform_logout()
                
                with col_no:
                    if st.button("❌ Cancel", key="cancel_logout", use_container_width=True):
                        st.session_state.show_logout_modal = False
                        st.rerun()
        
        st.divider()


def perform_logout():
    """
    Handle logout with proper error handling and state cleanup
    Prevents re-login without fresh session
    """
    try:
        # Log the logout action
        user_email = st.session_state.get("user", {}).get("email", "unknown")
        logger.info(f"User {user_email} initiated logout")
        
        # Set logout flag BEFORE clearing session
        st.session_state.is_logged_out = True
        
        # Perform logout (clears cookies and session)
        logout_user()
        
        # Show success message
        st.success("✅ Logged out successfully!")
        
        try:
            time.sleep(1.5)
        except Exception as e:
            logger.warning(f"Sleep interrupted: {e}")
        
        # Redirect to sign in page
        st.switch_page("pages/sign_in.py")
        
    except Exception as e:
        logger.error(f"Logout failed: {str(e)}")
        st.error(f"❌ Logout error: {str(e)}")
        st.session_state.show_logout_modal = False
        
        # Allow user to retry
        if st.button("Try Again", key="retry_logout"):
            st.rerun()


def logout_button():
    """
    Logout button that triggers confirmation modal
    """
    if st.button("🚪 Logout", key="logout_btn", type="secondary"):
        st.session_state.show_logout_modal = True