import os
from typing import Optional, Dict, Any
from supabase import create_client, Client
from .config import SUPABASE_URL, SUPABASE_KEY


def get_supabase_client() -> Client:
    """
    Get Supabase client instance
    """
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def test_supabase_connection():
    """
    Test connection to Supabase
    """
    client = get_supabase_client()
    try:
        # Simple query to test connection
        response = client.table('user_profiles').select('count').limit(1).execute()
        print("✅ Supabase connection successful!")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False


def create_user_profile(user_data):
    """
    Create or update user profile in Supabase
    """
    client = get_supabase_client()
    try:
        # Check if user already exists
        existing_user = client.table('user_profiles').select('*').eq('user_id', user_data['user_id']).execute()
        
        if existing_user.data:
            # Update existing user
            response = client.table('user_profiles').update(user_data).eq('user_id', user_data['user_id']).execute()
        else:
            # Create new user
            response = client.table('user_profiles').insert(user_data).execute()
        
        return response.data
    except Exception as e:
        print(f"Error creating/updating user profile: {e}")
        return None


def get_user_profile(user_id):
    """
    Get user profile from Supabase
    """
    client = get_supabase_client()
    try:
        response = client.table('user_profiles').select('*').eq('user_id', user_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting user profile: {e}")
        return None


# Supabase Auth functions
def sign_up_user(email: str, password: str, user_data: Dict[str, Any]) -> Optional[Dict]:
    """
    Sign up a new user in Supabase Auth
    """
    client = get_supabase_client()
    try:
        response = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": user_data
            }
        })
        return response.user
    except Exception as e:
        print(f"Error signing up user in Supabase: {e}")
        return None


def sign_in_user(email: str, password: str) -> Optional[Dict]:
    """
    Sign in user with Supabase Auth
    """
    client = get_supabase_client()
    try:
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response.user
    except Exception as e:
        print(f"Error signing in user with Supabase: {e}")
        return None


def reset_password(email: str) -> bool:
    """
    Send password reset email via Supabase
    """
    client = get_supabase_client()
    try:
        response = client.auth.reset_password_email(email)
        return True
    except Exception as e:
        print(f"Error sending password reset email: {e}")
        return False


def update_password(access_token: str, new_password: str) -> bool:
    """
    Update user password in Supabase
    """
    client = get_supabase_client()
    try:
        response = client.auth.update_user({
            "password": new_password
        })
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False


def get_user_by_email(email: str) -> Optional[Dict]:
    """
    Get user from Supabase Auth by email
    """
    client = get_supabase_client()
    try:
        # Note: This requires admin privileges in Supabase
        # For now, we'll use the profiles table
        response = client.table('user_profiles').select('*').eq('email', email).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting user by email: {e}")
        return None 