from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from app.database import get_db
from app.models import UserConfig, UserSecrets
from app.schemas.config_schemas import ConfigResponse, ConfigUpdate, SecretsResponse, SecretsUpdate
from app.utils.encryption import encrypt_key, decrypt_key, mask_key
import os

router = APIRouter()

@router.get("/config", response_model=ConfigResponse)
async def get_config(db: Session = Depends(get_db)):
    """Get current configuration"""
    config = db.query(UserConfig).first()
    if not config:
        # Create default config
        config = UserConfig()
        db.add(config)
        db.commit()
        db.refresh(config)
    
    return config

@router.post("/config", response_model=ConfigResponse)
async def update_config(
    config_update: ConfigUpdate,
    db: Session = Depends(get_db)
):
    """Update configuration"""
    config = db.query(UserConfig).first()
    if not config:
        config = UserConfig()
        db.add(config)
    
    # Update fields
    if config_update.top_n is not None:
        config.top_n = config_update.top_n
    if config_update.universe is not None:
        config.universe = config_update.universe
    if config_update.custom_tickers is not None:
        config.custom_tickers = config_update.custom_tickers
    if config_update.daily_run_time_local is not None:
        config.daily_run_time_local = config_update.daily_run_time_local
    if config_update.time_zone is not None:
        config.time_zone = config_update.time_zone
    
    db.commit()
    db.refresh(config)
    return config

@router.get("/secrets", response_model=SecretsResponse)
async def get_secrets_status(db: Session = Depends(get_db)):
    """Get status of API keys (masked)"""
    secrets = db.query(UserSecrets).first()
    
    response = {
        "openai_key_set": False,
        "market_data_key_set": False,
        "news_key_set": False,
        "options_key_set": False
    }
    
    if secrets:
        response["openai_key_set"] = secrets.openai_api_key_encrypted is not None
        response["market_data_key_set"] = secrets.market_data_api_key_encrypted is not None
        response["news_key_set"] = secrets.news_api_key_encrypted is not None
        response["options_key_set"] = secrets.options_api_key_encrypted is not None
    
    return response

@router.post("/secrets")
async def update_secrets(
    secrets_update: SecretsUpdate,
    db: Session = Depends(get_db)
):
    """Update API keys"""
    secrets = db.query(UserSecrets).first()
    if not secrets:
        secrets = UserSecrets()
        db.add(secrets)
    
    # Update encrypted keys
    if secrets_update.openai_api_key:
        secrets.openai_api_key_encrypted = encrypt_key(secrets_update.openai_api_key)
    
    if secrets_update.market_data_api_key:
        secrets.market_data_api_key_encrypted = encrypt_key(secrets_update.market_data_api_key)
    
    if secrets_update.news_api_key:
        secrets.news_api_key_encrypted = encrypt_key(secrets_update.news_api_key)
    
    if secrets_update.options_api_key:
        secrets.options_api_key_encrypted = encrypt_key(secrets_update.options_api_key)
    
    db.commit()
    
    return {"message": "API keys updated successfully"}

@router.post("/test_openai")
async def test_openai_connection(db: Session = Depends(get_db)):
    """Test OpenAI API connection"""
    from app.services.openai_service import OpenAIService
    
    try:
        openai_service = OpenAIService(db)
        result = await openai_service.test_connection()
        return {"success": result["success"], "message": result["message"]}
    except Exception as e:
        return {"success": False, "message": str(e)}