# --- المكتبات ---
import logging
import asyncio
import random
import time
import os
import json
import unicodedata
import re
import io
import difflib
import requests
import httpx  
import aiohttp
import arabic_reshaper
import math
import traceback
import numpy as np
import pandas as pd
from aiohttp import web
from scipy.stats import linregress
from scipy.signal import find_peaks
from typing import Dict, Union
from aiogram import types
from datetime import datetime, timedelta # 💡 تمت الإضافة هنا
from aiogram.dispatcher.filters import Text 
from pilmoji import Pilmoji 
from PIL import Image, ImageDraw, ImageFont, ImageOps
from bidi.algorithm import get_display
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from supabase import create_client, Client
from datetime import datetime, timezone
# استدعاء العميل غير المتزامن (من المسار الرئيسي للمكتبة)
from binance import AsyncClient
# استدعاء العميل العادي
from binance.client import Client
# استدعاء استثناءات الأخطاء
from binance.exceptions import BinanceAPIException
# --- المفاتيح ---
ADMIN_ID = 8695560834
# سحب التوكينات من Render (لن يعمل البوت بدونها في الإعدادات)
API_TOKEN = os.getenv('BOT_TOKEN')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
GROUP_ID = os.getenv('GROUP_ID')
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
tell_1 = os.getenv('tell_1')
tell_2 = os.getenv('tell_2')


# 2. التحقق ثانياً
if not API_TOKEN or not GROUP_ID:
    logging.error("❌ خطأ: المتغيرات المشفرة مفقودة في إعدادات Render!")
    

# تعريف المحركات
bot = Bot(token=API_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
# 1. في بداية الملف (خارج كل الدوال) قم بتعريف هذا المتغير
bot_username = None 

# --- قسم الدوال ---
# ==========================================
# 🛠️ دوال مساعدة
# ==========================================
def format_num(num, decimals=8):
    if num is None: return "0"
    return f"{float(num):.{decimals}f}".rstrip('0').rstrip('.') if '.' in f"{float(num):.{decimals}f}" else f"{float(num):.{decimals}f}"

async def send_telegram_notification(text: str, chat_id: str):
    global BOT_TOKEN # تم التعديل هنا
    
    if not BOT_TOKEN or not chat_id:
        logging.warning("⚠️ لم يتم إرسال الإشعار: تأكد من إعداد BOT_TOKEN و chat_id")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" # وتم التعديل هنا
    # ... باقي الكود كما هو ...

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    logging.error(f"❌ فشل إرسال إشعار تليجرام: {await response.text()}")
    except Exception as e:
        logging.error(f"❌ خطأ أثناء الاتصال بتليجرام: {e}")
        


async def intelligence_scanner():
    print(f"🚀 {datetime.now().strftime('%H:%M:%S')} | الرادار v11.2 يمسح السوق بـ 50+ استراتيجية")
    
    try:
        res = supabase.table("crypto_market_simulation_u").select("*").execute()
        coins = res.data
    
        if not coins: 
            return []

        # 1. بداية حلقة التكرار للمرور على كل عملة
        for coin in coins:
            coin_name = coin.get('symbol')
            
            # ==========================================
            # ⛔ [ 0. فلتر إبادة الأشباح المطور ]
            # ==========================================
            price = float(coin.get('current_price') or 0.0)
            vol_15m = float(coin.get('volume_15m') or 0.0)
            vol_ma_15m = float(coin.get('volume_ma_15m') or 1.0)
            vol_24h = float(coin.get('volume_24h') or 0.0) 
            bbw_15m = float(coin.get('bbw_15m') or 0.0)
            adx_15m = float(coin.get('adx_15m') or 0.0)

            # تطبيق شروط الطرد
            if price <= 0: continue 
            if vol_15m < 50000: continue
            if vol_24h > 0 and vol_24h < 1000000: continue
            if vol_15m < (vol_ma_15m * 0.3): continue
            if bbw_15m <= 0.01: continue
            if adx_15m > 0 and adx_15m < 15: continue
            # ---------------------------------------------------------
            
            # ==========================================
            # 📊 [ استخراج المتغيرات والبيانات الإضافية ]
            # ==========================================
            # --- بيانات السوق الأساسية والحيتان (تمت الإضافة هنا) ---
            open_price_24h = float(coin.get('open_price_24h') or price)
            high_24h = float(coin.get('high_24h') or (price * 1.05)) 
            low_24h = float(coin.get('low_24h') or (price * 0.95)) 
            change_24h = float(coin.get('change_24h') or 0.0)
            last_tick_direction = coin.get('last_tick_direction') or ""
            taker_buy_ratio_1h = float(coin.get('taker_buy_ratio_1h') or 1.0)
            whale_net_flow_volume = float(coin.get('whale_net_flow_volume') or 0.0)
            whale_absorption_detected = bool(coin.get('whale_absorption_detected') or False)
            orderbook_imbalance_ratio = float(coin.get('orderbook_imbalance_ratio') or 0.0)
            
            # --- الماكد 15 دقيقة (مطلوب لاستراتيجيتك الخاصة) ---
            macd_15m = float(coin.get('macd_15m') or 0.0)
            macd_signal_15m = float(coin.get('macd_signal_15m') or 0.0)
            macd_hist_15m = float(coin.get('macd_hist_15m') or 0.0)
            
            # --- المتوسطات (EMAs) ---
            ema_20_15m = float(coin.get('ema_20_15m') or 0.0)
            ema_20_1h = float(coin.get('ema_20_1h') or 0.0)
            ema_20_4h = float(coin.get('ema_20_4h') or 0.0)
            ema_50_15m = float(coin.get('ema_50_15m') or 0.0)
            ema_100_15m = float(coin.get('ema_100_15m') or 0.0)
            ema_200_1h = float(coin.get('ema_200_1h') or 0.0)

            # --- RSI & ADX ---
            rsi_15m = float(coin.get('rsi_15m') or 50.0) 
            rsi_1h = float(coin.get('rsi_1h') or 50.0)
            adx_1h = float(coin.get('adx_1h') or 0.0)

            # --- البولينجر باند 15 دقيقة و 1 ساعة ---
            bb_upper_15m = float(coin.get('bb_upper_15m') or 0.0) 
            bb_lower_15m = float(coin.get('bb_lower_15m') or 0.0) 
            bb_upper_1h = float(coin.get('bb_upper_1h') or 0.0)
            bb_lower_1h = float(coin.get('bb_lower_1h') or 0.0)

            # --- الفوليوم و VWAP ---
            vwap_1h = float(coin.get('vwap_1h') or 0.0)
            vwap_4h = float(coin.get('vwap_4h') or 0.0)
            volume_delta_1h = float(coin.get('volume_delta_1h') or 0.0)
            mfi_15m = float(coin.get('mfi_15m') or 50.0) # السيولة

            # --- السوبر تريند ---
            supertrend_1h = float(coin.get('supertrend_1h') or 0.0)
            supertrend_15m = float(coin.get('supertrend_15m') or 0.0)
            # --- استكمال مؤشرات 15 دقيقة المطلوبة للسكالبينج الخاطف ---
            stochastic_k_15m = float(coin.get('stochastic_k_15m') or 50.0)
            stochastic_d_15m = float(coin.get('stochastic_d_15m') or 50.0)
            obv_15m = float(coin.get('obv_15m') or 0.0)
            obv_slope_15m = float(coin.get('obv_slope_15m') or 0.0)
            mfi_15m = float(coin.get('mfi_15m') or 50.0)
            cmf_15m = float(coin.get('cmf_15m') or 0.0)
            williams_r_15m = float(coin.get('williams_r_15m') or -50.0)
            choppiness_index_15m = float(coin.get('choppiness_index_15m') or 50.0)
            parabolic_sar_15m = float(coin.get('parabolic_sar_15m') or 0.0)
            volume_delta_15m = float(coin.get('volume_delta_15m') or 0.0)
            kc_upper_1h = float(coin.get('kc_upper_1h') or 0.0) 
            kc_lower_1h = float(coin.get('kc_lower_1h') or 0.0)

            # ==========================================
            # 🎯 2. بنك الاستراتيجيات السريعة (52 استراتيجية)
            # ========================================== 
            strategy_id = 0
            strategy_name = ""
            trade_type = ""

            # 🔻 1. [طلبك الخاص]: السعر قرب قاع 24 ساعة + ماكد 15د أحمر
            if price <= (low_24h * 1.015) and macd_hist_15m < 0:
                strategy_id, strategy_name, trade_type = 1, "كسر قاع 24 ساعة + ماكد سلبي", "SHORT"
                
            # 🔺 2. العكس: السعر قرب قمة 24 ساعة + ماكد 15د أخضر
            elif price >= (high_24h * 0.985) and macd_hist_15m > 0:
                strategy_id, strategy_name, trade_type = 2, "اختراق قمة 24 ساعة + ماكد إيجابي", "SHORT"

            # --- استراتيجيات الحيتان والأوردر بوك (سكالبينج خاطف) ---
            elif whale_absorption_detected and taker_buy_ratio_1h > 1.2 and price > vwap_1h:
                strategy_id, strategy_name, trade_type = 3, "امتصاص حيتان + سيولة شرائية (سكالب)", "LONG"
            elif orderbook_imbalance_ratio < -0.4 and volume_delta_1h < 0 and price < ema_20_15m:
                strategy_id, strategy_name, trade_type = 4, "خلل الأوردر بوك البيعي", "SHORT"
            elif whale_net_flow_volume > 500000 and rsi_15m < 65 and price > ema_20_1h:
                strategy_id, strategy_name, trade_type = 5, "تدفق حيتان مفاجئ (LONG)", "LONG"
            elif whale_net_flow_volume < -500000 and rsi_15m > 35 and price < ema_20_1h:
                strategy_id, strategy_name, trade_type = 6, "تخارج حيتان مفاجئ (SHORT)", "SHORT"

            # --- استراتيجيات VWAP وتوازن السوق ---
            elif price > vwap_1h and price > vwap_4h and macd_hist_15m > 0 and 50 < rsi_15m < 70:
                strategy_id, strategy_name, trade_type = 7, "تطابق VWAP الشرائي المتعدد", "LONG"
            elif price < vwap_1h and price < vwap_4h and macd_hist_15m < 0 and 30 < rsi_15m < 50:
                strategy_id, strategy_name, trade_type = 8, "تطابق VWAP البيعي المتعدد", "SHORT"
            elif (price <= vwap_1h * 1.002 and price >= vwap_1h * 0.998) and taker_buy_ratio_1h > 1.1:
                strategy_id, strategy_name, trade_type = 9, "ارتداد شرائي من خط VWAP", "LONG"

            # --- استراتيجيات البولينجر باند (سكويز وانفجار) ---
            elif price > bb_upper_15m and rsi_15m > 60 and volume_delta_1h > 0:
                strategy_id, strategy_name, trade_type = 10, "اختراق البولنجر 15د بزخم سيولة", "LONG"
            elif price < bb_lower_15m and rsi_15m < 40 and volume_delta_1h < 0:
                strategy_id, strategy_name, trade_type = 11, "كسر البولنجر 15د بزخم سيولة", "SHORT"
            elif price <= bb_lower_1h and rsi_15m < 30 and macd_hist_15m > 0: # دايفرجنس مخفي
                strategy_id, strategy_name, trade_type = 12, "ارتداد من قاع بولنجر 1س (عكس الاتجاه)", "LONG"
            elif price >= bb_upper_1h and rsi_15m > 70 and macd_hist_15m < 0:
                strategy_id, strategy_name, trade_type = 13, "ارتداد من قمة بولنجر 1س (عكس الاتجاه)", "SHORT"

            # --- استراتيجيات تقاطعات EMA السريعة (سكالبينج) ---
            elif ema_20_15m > ema_50_15m and price > ema_20_15m and adx_1h > 25:
                strategy_id, strategy_name, trade_type = 14, "متابعة ترند 15د قوي (ADX>25)", "LONG"
            elif ema_20_15m < ema_50_15m and price < ema_20_15m and adx_1h > 25:
                strategy_id, strategy_name, trade_type = 15, "متابعة هبوط 15د قوي (ADX>25)", "SHORT"
            elif price > ema_20_15m and price > ema_20_1h and price > ema_20_4h and rsi_15m < 65:
                strategy_id, strategy_name, trade_type = 16, "توافق الترندات الشرائي (15د, 1س, 4س)", "LONG"
            elif price < ema_20_15m and price < ema_20_1h and price < ema_20_4h and rsi_15m > 35:
                strategy_id, strategy_name, trade_type = 17, "توافق الترندات البيعي (15د, 1س, 4س)", "SHORT"
            elif price == ema_200_1h and rsi_15m < 40: # ملامسة متحرك 200
                strategy_id, strategy_name, trade_type = 18, "اصطياد الارتداد من EMA 200 الذهبي", "LONG"

            # --- استراتيجيات RSI والتشبع السريع ---
            elif rsi_15m < 25 and rsi_1h < 30 and macd_hist_15m > macd_signal_15m:
                strategy_id, strategy_name, trade_type = 19, "تشبع بيعي مزدوج + بداية انعكاس", "LONG"
            elif rsi_15m > 75 and rsi_1h > 70 and macd_hist_15m < macd_signal_15m:
                strategy_id, strategy_name, trade_type = 20, "تشبع شرائي مزدوج + بداية انعكاس", "SHORT"
            elif 45 < rsi_15m < 55 and rsi_1h > 60 and price > ema_20_15m:
                strategy_id, strategy_name, trade_type = 21, "استراحة محارب (استمرار صعود 1س)", "LONG"
            elif 45 < rsi_15m < 55 and rsi_1h < 40 and price < ema_20_15m:
                strategy_id, strategy_name, trade_type = 22, "استراحة محارب (استمرار هبوط 1س)", "SHORT"

            # --- استراتيجيات السوبر تريند ---
            elif price > supertrend_15m and price > supertrend_1h and macd_hist_15m > 0:
                strategy_id, strategy_name, trade_type = 23, "سوبر تريند أخضر مزدوج", "LONG"
            elif price < supertrend_15m and price < supertrend_1h and macd_hist_15m < 0:
                strategy_id, strategy_name, trade_type = 24, "سوبر تريند أحمر مزدوج", "SHORT"
            
            # --- دمج تغيرات 24 ساعة مع الماكد ---
            elif change_24h > 5 and macd_hist_15m > 0 and rsi_15m < 65:
                strategy_id, strategy_name, trade_type = 25, "زخم يومي شرائي عالٍ + ماكد إيجابي", "LONG"
            elif change_24h < -5 and macd_hist_15m < 0 and rsi_15m > 35:
                strategy_id, strategy_name, trade_type = 26, "زخم يومي بيعي عالٍ + ماكد سلبي", "SHORT"

            # -----------------------------------------------------
            # تكملة بنك الاستراتيجيات (27 إلى 52) لزيادة الدقة
            # -----------------------------------------------------
            elif taker_buy_ratio_1h > 1.5 and rsi_15m > 50 and price > ema_20_15m:
                strategy_id, strategy_name, trade_type = 27, "سيطرة المشترين اللحظية", "LONG"
            elif taker_buy_ratio_1h < 0.6 and rsi_15m < 50 and price < ema_20_15m:
                strategy_id, strategy_name, trade_type = 28, "سيطرة البائعين اللحظية", "SHORT"
            elif adx_1h > 35 and ema_20_15m > ema_100_15m and rsi_15m < 60:
                strategy_id, strategy_name, trade_type = 29, "ترند خارق للصعود (ADX > 35)", "LONG"
            elif adx_1h > 35 and ema_20_15m < ema_100_15m and rsi_15m > 40:
                strategy_id, strategy_name, trade_type = 30, "ترند خارق للهبوط (ADX > 35)", "SHORT"
            elif whale_absorption_detected and price < bb_lower_15m:
                strategy_id, strategy_name, trade_type = 31, "تجميع حيتان عند القاع (انفجار محتمل)", "LONG"
            elif orderbook_imbalance_ratio > 0.5 and price > vwap_1h and rsi_15m < 60:
                strategy_id, strategy_name, trade_type = 32, "خلل بوك شرائي مع دعم VWAP", "LONG"
            elif change_24h > 10 and rsi_15m > 75 and volume_delta_1h < 0:
                strategy_id, strategy_name, trade_type = 33, "شورت تصحيحي بعد بامب قوي", "SHORT"
            elif change_24h < -10 and rsi_15m < 25 and volume_delta_1h > 0:
                strategy_id, strategy_name, trade_type = 34, "لونج تصحيحي بعد دامب قوي", "LONG"
            elif macd_15m > 0 and macd_signal_15m > 0 and macd_hist_15m > 0 and price > ema_20_1h:
                strategy_id, strategy_name, trade_type = 35, "ثلاثية الماكد الذهبية", "LONG"
            elif macd_15m < 0 and macd_signal_15m < 0 and macd_hist_15m < 0 and price < ema_20_1h:
                strategy_id, strategy_name, trade_type = 36, "ثلاثية الماكد الحمراء", "SHORT"
            elif price > ema_20_4h and price < ema_20_15m and rsi_15m < 35:
                strategy_id, strategy_name, trade_type = 37, "بول باك للترند الصاعد 4س", "LONG"
            elif price < ema_20_4h and price > ema_20_15m and rsi_15m > 65:
                strategy_id, strategy_name, trade_type = 38, "تصحيح وهمي للترند الهابط 4س", "SHORT"
            elif volume_delta_1h > 0 and whale_net_flow_volume > 0 and last_tick_direction == "UpPlus":
                strategy_id, strategy_name, trade_type = 39, "زخم شرائي فوري (Tick & Vol)", "LONG"
            elif volume_delta_1h < 0 and whale_net_flow_volume < 0 and last_tick_direction == "DownMinus":
                strategy_id, strategy_name, trade_type = 40, "زخم بيعي فوري (Tick & Vol)", "SHORT"
            elif bb_upper_15m - bb_lower_15m < (price * 0.01) and rsi_15m > 55:
                strategy_id, strategy_name, trade_type = 41, "انفجار اختناق البولنجر (صعود)", "LONG"
            elif bb_upper_15m - bb_lower_15m < (price * 0.01) and rsi_15m < 45:
                strategy_id, strategy_name, trade_type = 42, "انفجار اختناق البولنجر (هبوط)", "SHORT"
            elif rsi_15m > 50 and rsi_1h > 50 and ema_20_15m > ema_50_15m and ema_20_1h > ema_50_1h:
                strategy_id, strategy_name, trade_type = 43, "تأكيد صعودي مزدوج الإطارات", "LONG"
            elif rsi_15m < 50 and rsi_1h < 50 and ema_20_15m < ema_50_15m and ema_20_1h < ema_50_1h:
                strategy_id, strategy_name, trade_type = 44, "تأكيد هبوطي مزدوج الإطارات", "SHORT"
            elif price >= (open_price_24h * 1.05) and taker_buy_ratio_1h > 1.1:
                strategy_id, strategy_name, trade_type = 45, "استمرار الصعود اليومي", "LONG"
            elif price <= (open_price_24h * 0.95) and taker_buy_ratio_1h < 0.9:
                strategy_id, strategy_name, trade_type = 46, "استمرار الهبوط اليومي", "SHORT"
            elif rsi_15m == 50 and macd_hist_15m > 0 and volume_delta_1h > 0:
                strategy_id, strategy_name, trade_type = 47, "اختراق خط الـ 50 المحايد للـ RSI (شراء)", "LONG"
            elif rsi_15m == 50 and macd_hist_15m < 0 and volume_delta_1h < 0:
                strategy_id, strategy_name, trade_type = 48, "كسر خط الـ 50 المحايد للـ RSI (بيع)", "SHORT"
            elif whale_absorption_detected and price > ema_20_4h and rsi_15m < 50:
                strategy_id, strategy_name, trade_type = 49, "شراء من مناطق امتصاص الحيتان الكبرى", "LONG"
            elif orderbook_imbalance_ratio > 0.8 and price > vwap_1h:
                strategy_id, strategy_name, trade_type = 50, "سيولة شرائية طاغية (Orderbook)", "LONG"
            elif orderbook_imbalance_ratio < -0.8 and price < vwap_1h:
                strategy_id, strategy_name, trade_type = 51, "سيولة بيعية طاغية (Orderbook)", "SHORT"
            elif price <= low_24h and rsi_15m > 30 and macd_hist_15m > 0:
                strategy_id, strategy_name, trade_type = 52, "دبل بوتوم (Double Bottom) يومي", "LONG"
            # ==========================================
            # 🚀 استراتيجيات Williams %R و MFI (تشبع السيولة السريع)
            # ==========================================
            elif williams_r_15m < -85 and mfi_15m < 20 and volume_delta_15m > 0:
                strategy_id, strategy_name, trade_type = 53, "تشبع بيعي Williams+MFI (قاع سريع)", "LONG"
            elif williams_r_15m > -15 and mfi_15m > 80 and volume_delta_15m < 0:
                strategy_id, strategy_name, trade_type = 54, "تشبع شرائي Williams+MFI (قمة سريعة)", "SHORT"
            elif williams_r_1h < -90 and price > kc_lower_15m and macd_hist_15m > 0:
                strategy_id, strategy_name, trade_type = 55, "ارتداد Williams من قاع القناة", "LONG"
            elif williams_r_1h > -10 and price < kc_upper_15m and macd_hist_15m < 0:
                strategy_id, strategy_name, trade_type = 56, "ارتداد Williams من قمة القناة", "SHORT"
            
            # ==========================================
            # 🌊 استراتيجيات Chaikin Money Flow (CMF) وتدفق الأموال
            # ==========================================
            elif cmf_15m > 0.15 and cmf_1h > 0.1 and price > vwap_15m:
                strategy_id, strategy_name, trade_type = 57, "تدفق أموال قوي (CMF إيجابي مزدوج)", "LONG"
            elif cmf_15m < -0.15 and cmf_1h < -0.1 and price < vwap_15m:
                strategy_id, strategy_name, trade_type = 58, "هروب أموال قوي (CMF سلبي مزدوج)", "SHORT"
            elif cmf_15m > 0.2 and rsi_15m < 45:
                strategy_id, strategy_name, trade_type = 59, "تجميع خفي (RSI هابط + CMF صاعد)", "LONG"
            elif cmf_15m < -0.2 and rsi_15m > 55:
                strategy_id, strategy_name, trade_type = 60, "تصريف خفي (RSI صاعد + CMF هابط)", "SHORT"

            # ==========================================
            # 🎯 استراتيجيات الاستوكاستيك (Stochastic) السريعة
            # ==========================================
            elif stochastic_k_15m < 20 and stochastic_k_15m > stochastic_d_15m and rsi_15m > 30:
                strategy_id, strategy_name, trade_type = 61, "تقاطع استوكاستيك إيجابي من القاع", "LONG"
            elif stochastic_k_15m > 80 and stochastic_k_15m < stochastic_d_15m and rsi_15m < 70:
                strategy_id, strategy_name, trade_type = 62, "تقاطع استوكاستيك سلبي من القمة", "SHORT"
            elif stochastic_k_1h < 20 and stochastic_k_15m > 50 and macd_hist_15m > 0:
                strategy_id, strategy_name, trade_type = 63, "دعم استوكاستيك 1س مع انطلاقة 15د", "LONG"
            elif stochastic_k_1h > 80 and stochastic_k_15m < 50 and macd_hist_15m < 0:
                strategy_id, strategy_name, trade_type = 64, "مقاومة استوكاستيك 1س مع هبوط 15د", "SHORT"

            # ==========================================
            # 📏 استراتيجيات قنوات كيلتنر (Keltner Channels)
            # ==========================================
            elif price > kc_upper_15m and adx_1h > 25 and volume_delta_15m > 0:
                strategy_id, strategy_name, trade_type = 65, "اختراق كيلتنر صاعد بزخم قوي", "LONG"
            elif price < kc_lower_15m and adx_1h > 25 and volume_delta_15m < 0:
                strategy_id, strategy_name, trade_type = 66, "كسر كيلتنر هابط بزخم قوي", "SHORT"
            elif price < kc_lower_15m and stochastic_k_15m < 15 and rsi_15m < 30:
                strategy_id, strategy_name, trade_type = 67, "ارتداد سكالبينج من قاع كيلتنر", "LONG"
            elif price > kc_upper_15m and stochastic_k_15m > 85 and rsi_15m > 70:
                strategy_id, strategy_name, trade_type = 68, "ارتداد سكالبينج من قمة كيلتنر", "SHORT"

            # ==========================================
            # 🌪️ استراتيجيات مؤشر التذبذب والترند (Choppiness & ADX)
            # ==========================================
            elif choppiness_index_1h < 38.2 and adx_1h > 30 and price > ema_20_15m:
                strategy_id, strategy_name, trade_type = 69, "بداية ترند صاعد قوي (انعدام التذبذب)", "LONG"
            elif choppiness_index_1h < 38.2 and adx_1h > 30 and price < ema_20_15m:
                strategy_id, strategy_name, trade_type = 70, "بداية ترند هابط قوي (انعدام التذبذب)", "SHORT"
            elif choppiness_index_15m > 61.8 and price <= bb_lower_15m and rsi_15m < 40:
                strategy_id, strategy_name, trade_type = 71, "شراء من دعم عرضي (سوق متذبذب)", "LONG"
            elif choppiness_index_15m > 61.8 and price >= bb_upper_15m and rsi_15m > 60:
                strategy_id, strategy_name, trade_type = 72, "بيع من مقاومة عرضية (سوق متذبذب)", "SHORT"

            # ==========================================
            # 📊 استراتيجيات الحجم التراكمي (OBV - On Balance Volume)
            # ==========================================
            elif obv_slope_15m > 0 and obv_slope_1h > 0 and price > vwap_15m:
                strategy_id, strategy_name, trade_type = 73, "زخم OBV تصاعدي مع VWAP", "LONG"
            elif obv_slope_15m < 0 and obv_slope_1h < 0 and price < vwap_15m:
                strategy_id, strategy_name, trade_type = 74, "زخم OBV تنازلي مع VWAP", "SHORT"
            elif price < ema_20_15m and obv_slope_15m > 0 and macd_hist_15m > 0:
                strategy_id, strategy_name, trade_type = 75, "دايفرجنس OBV إيجابي (السعر يهبط والحجم يصعد)", "LONG"
            elif price > ema_20_15m and obv_slope_15m < 0 and macd_hist_15m < 0:
                strategy_id, strategy_name, trade_type = 76, "دايفرجنس OBV سلبي (السعر يصعد والحجم يهبط)", "SHORT"

            # ==========================================
            # ☁️ استراتيجيات سحابة الإيشيموكو (Ichimoku) اللحظية
            # ==========================================
            elif price > ichimoku_cloud_top_1h and price > ema_20_15m and rsi_15m < 60:
                strategy_id, strategy_name, trade_type = 77, "استمرار فوق سحابة إيشيموكو 1س", "LONG"
            elif price < ichimoku_cloud_bottom_1h and price < ema_20_15m and rsi_15m > 40:
                strategy_id, strategy_name, trade_type = 78, "استمرار تحت سحابة إيشيموكو 1س", "SHORT"
            elif price > ichimoku_conversion_1h and ichimoku_conversion_1h > ichimoku_base_1h:
                strategy_id, strategy_name, trade_type = 79, "تقاطع إيشيموكو الذهبي 1س", "LONG"
            elif price < ichimoku_conversion_1h and ichimoku_conversion_1h < ichimoku_base_1h:
                strategy_id, strategy_name, trade_type = 80, "تقاطع إيشيموكو الميت 1س", "SHORT"

            # ==========================================
            # ⚡ استراتيجيات Parabolic SAR اللحظية
            # ==========================================
            elif price > parabolic_sar_15m and parabolic_sar_1h < price and macd_hist_15m > 0:
                strategy_id, strategy_name, trade_type = 81, "توافق Parabolic SAR شرائي 15د+1س", "LONG"
            elif price < parabolic_sar_15m and parabolic_sar_1h > price and macd_hist_15m < 0:
                strategy_id, strategy_name, trade_type = 82, "توافق Parabolic SAR بيعي 15د+1س", "SHORT"
            elif price > parabolic_sar_15m and volume_delta_15m > 0 and rsi_15m > 55:
                strategy_id, strategy_name, trade_type = 83, "انعكاس Parabolic SAR بزخم فوليوم", "LONG"
            elif price < parabolic_sar_15m and volume_delta_15m < 0 and rsi_15m < 45:
                strategy_id, strategy_name, trade_type = 84, "كسر Parabolic SAR بزخم فوليوم", "SHORT"

            # ==========================================
            # 🐋 دمج الحيتان والأوردر بوك مع المؤشرات السريعة (سكالبينج عنيف)
            # ==========================================
            elif whale_absorption_detected and mfi_15m < 30 and stochastic_k_15m < 20:
                strategy_id, strategy_name, trade_type = 85, "امتصاص حيتان في مناطق تشبع بيعي", "LONG"
            elif orderbook_imbalance_ratio > 0.6 and cmf_15m > 0.1 and adx_1h > 25:
                strategy_id, strategy_name, trade_type = 86, "ضغط بوك شرائي + سيولة CMF + ترند", "LONG"
            elif orderbook_imbalance_ratio < -0.6 and cmf_15m < -0.1 and adx_1h > 25:
                strategy_id, strategy_name, trade_type = 87, "ضغط بوك بيعي + هروب CMF + ترند", "SHORT"
            elif whale_net_flow_volume > 1000000 and price > vwap_15m and macd_hist_15m > 0:
                strategy_id, strategy_name, trade_type = 88, "دخول حوت مليوني فوق VWAP", "LONG"
            elif whale_net_flow_volume < -1000000 and price < vwap_15m and macd_hist_15m < 0:
                strategy_id, strategy_name, trade_type = 89, "تخارج حوت مليوني تحت VWAP", "SHORT"

            # ==========================================
            # 🎯 استراتيجيات Value Area و POC (مناطق القيمة)
            # ==========================================
            elif price > value_area_high_1h and volume_delta_15m > 0 and rsi_15m < 65:
                strategy_id, strategy_name, trade_type = 90, "اختراق منطقة القيمة العليا (Volume Profile)", "LONG"
            elif price < value_area_low_1h and volume_delta_15m < 0 and rsi_15m > 35:
                strategy_id, strategy_name, trade_type = 91, "كسر منطقة القيمة السفلى (Volume Profile)", "SHORT"
            elif (price >= poc_price_1h * 0.998 and price <= poc_price_1h * 1.002) and macd_hist_15m > 0:
                strategy_id, strategy_name, trade_type = 92, "ارتداد شرائي من خط الـ POC", "LONG"
            elif (price >= poc_price_1h * 0.998 and price <= poc_price_1h * 1.002) and macd_hist_15m < 0:
                strategy_id, strategy_name, trade_type = 93, "ارتداد بيعي من خط الـ POC", "SHORT"

            # ==========================================
            # 🔥 استراتيجيات 94 إلى 150 (كومبو سكالبينج وفوليوم وإشارات متقدمة)
            # ==========================================
            elif rsi_15m > rsi_1h and rsi_15m > 60 and adx_15m > 25:
                strategy_id, strategy_name, trade_type = 94, "تسارع RSI لحظي (سكالب صاعد)", "LONG"
            elif rsi_15m < rsi_1h and rsi_15m < 40 and adx_15m > 25:
                strategy_id, strategy_name, trade_type = 95, "تسارع RSI لحظي (سكالب هابط)", "SHORT"
            
            elif price > ema_50_15m and price < ema_20_15m and stochastic_k_15m < 20:
                strategy_id, strategy_name, trade_type = 96, "صيد الارتداد بين EMA20 و EMA50", "LONG"
            elif price < ema_50_15m and price > ema_20_15m and stochastic_k_15m > 80:
                strategy_id, strategy_name, trade_type = 97, "صيد الرفض بين EMA20 و EMA50", "SHORT"

            elif mfi_15m > 85 and rsi_15m > 75 and price > bb_upper_15m:
                strategy_id, strategy_name, trade_type = 98, "انفجار سعري متطرف (شورت قناص)", "SHORT"
            elif mfi_15m < 15 and rsi_15m < 25 and price < bb_lower_15m:
                strategy_id, strategy_name, trade_type = 99, "انهيار سعري متطرف (لونج قناص)", "LONG"

            elif volume_delta_1h > 0 and volume_delta_2h > 0 and macd_hist_15m > 0:
                strategy_id, strategy_name, trade_type = 100, "دلتا فوليوم خضراء متتالية (1س+2س)", "LONG"
            elif volume_delta_1h < 0 and volume_delta_2h < 0 and macd_hist_15m < 0:
                strategy_id, strategy_name, trade_type = 101, "دلتا فوليوم حمراء متتالية (1س+2س)", "SHORT"

            elif taker_buy_ratio_1h > 2.0 and rsi_15m < 50:
                strategy_id, strategy_name, trade_type = 102, "شراء ماركت مكثف مباغت (Taker Ratio>2)", "LONG"
            elif taker_buy_ratio_1h < 0.3 and rsi_15m > 50:
                strategy_id, strategy_name, trade_type = 103, "بيع ماركت مكثف مباغت (Taker Ratio<0.3)", "SHORT"

            elif cmf_1h > 0.2 and mfi_1h > 60 and price > ema_20_15m:
                strategy_id, strategy_name, trade_type = 104, "سيولة 1س تدعم السكالب الشرائي 15د", "LONG"
            elif cmf_1h < -0.2 and mfi_1h < 40 and price < ema_20_15m:
                strategy_id, strategy_name, trade_type = 105, "سيولة 1س تدعم السكالب البيعي 15د", "SHORT"

            elif price == high_24h and macd_hist_15m > 0 and volume_delta_1h > 0:
                strategy_id, strategy_name, trade_type = 106, "اختراق قمة يومية حقيقية (فوليوم أخضر)", "LONG"
            elif price == low_24h and macd_hist_15m < 0 and volume_delta_1h < 0:
                strategy_id, strategy_name, trade_type = 107, "كسر قاع يومي حقيقي (فوليوم أحمر)", "SHORT"

            elif williams_r_15m > -20 and stochastic_k_15m > 80 and macd_hist_15m < 0:
                strategy_id, strategy_name, trade_type = 108, "تضارب زخم القمة (Williams+Stoch ضد MACD)", "SHORT"
            elif williams_r_15m < -80 and stochastic_k_15m < 20 and macd_hist_15m > 0:
                strategy_id, strategy_name, trade_type = 109, "تضارب زخم القاع (Williams+Stoch ضد MACD)", "LONG"

            elif choppiness_index_15m < 30 and supertrend_15m < price and rsi_15m < 60:
                strategy_id, strategy_name, trade_type = 110, "ترند 15د صلب مع سوبر تريند", "LONG"
            elif choppiness_index_15m < 30 and supertrend_15m > price and rsi_15m > 40:
                strategy_id, strategy_name, trade_type = 111, "ترند 15د هابط مع سوبر تريند", "SHORT"

            elif bb_upper_1h - bb_lower_1h < (price * 0.015) and price > bb_upper_15m:
                strategy_id, strategy_name, trade_type = 112, "انفجار اختناق 1س للأعلى (Squeeze Break)", "LONG"
            elif bb_upper_1h - bb_lower_1h < (price * 0.015) and price < bb_lower_15m:
                strategy_id, strategy_name, trade_type = 113, "انفجار اختناق 1س للأسفل (Squeeze Break)", "SHORT"

            elif obv_slope_1h > 0 and cmf_1h > 0 and rsi_15m == 50:
                strategy_id, strategy_name, trade_type = 114, "اختراق خط الـ 50 RSI بدعم OBV+CMF", "LONG"
            elif obv_slope_1h < 0 and cmf_1h < 0 and rsi_15m == 50:
                strategy_id, strategy_name, trade_type = 115, "كسر خط الـ 50 RSI بضغط OBV+CMF", "SHORT"

            elif whale_absorption_detected and price < ema_200_1h and stochastic_k_15m < 20:
                strategy_id, strategy_name, trade_type = 116, "حيتان تشتري تحت الـ 200 EMA", "LONG"
            elif orderbook_imbalance_ratio > 0.9 and volume_1h > volume_ma_1h:
                strategy_id, strategy_name, trade_type = 117, "أوردر بوك شرائي متطرف + فوليوم سبايك", "LONG"
            elif orderbook_imbalance_ratio < -0.9 and volume_1h > volume_ma_1h:
                strategy_id, strategy_name, trade_type = 118, "أوردر بوك بيعي متطرف + فوليوم سبايك", "SHORT"

            elif price > ema_20_15m and price > ema_50_15m and price > ema_100_15m and rsi_15m < 60:
                strategy_id, strategy_name, trade_type = 119, "المروحة الشرائية (EMA 20,50,100)", "LONG"
            elif price < ema_20_15m and price < ema_50_15m and price < ema_100_15m and rsi_15m > 40:
                strategy_id, strategy_name, trade_type = 120, "المروحة البيعية (EMA 20,50,100)", "SHORT"

            elif kc_upper_15m > bb_upper_15m and price > kc_upper_15m:
                strategy_id, strategy_name, trade_type = 121, "اختراق بولنجر داخل كيلتنر صاعد", "LONG"
            elif kc_lower_15m < bb_lower_15m and price < kc_lower_15m:
                strategy_id, strategy_name, trade_type = 122, "كسر بولنجر داخل كيلتنر هابط", "SHORT"

            elif parabolic_sar_15m < price and parabolic_sar_1h < price and parabolic_sar_2h < price:
                strategy_id, strategy_name, trade_type = 123, "توافق Parabolic SAR ثلاثي الأبعاد (صعود)", "LONG"
            elif parabolic_sar_15m > price and parabolic_sar_1h > price and parabolic_sar_2h > price:
                strategy_id, strategy_name, trade_type = 124, "توافق Parabolic SAR ثلاثي الأبعاد (هبوط)", "SHORT"

            elif adx_1h < 15 and bbw_15m < 0.015 and macd_hist_15m > 0.001:
                strategy_id, strategy_name, trade_type = 125, "تجميع هادئ جداً قبل بامب محتمل", "LONG"
            elif adx_1h < 15 and bbw_15m < 0.015 and macd_hist_15m < -0.001:
                strategy_id, strategy_name, trade_type = 126, "تصريف هادئ جداً قبل دامب محتمل", "SHORT"

            elif rsi_15m > 65 and stochastic_k_15m > 85 and macd_hist_15m < macd_signal_15m:
                strategy_id, strategy_name, trade_type = 127, "تقاطع ماكد سلبي في مناطق الذروة", "SHORT"
            elif rsi_15m < 35 and stochastic_k_15m < 15 and macd_hist_15m > macd_signal_15m:
                strategy_id, strategy_name, trade_type = 128, "تقاطع ماكد إيجابي في مناطق القاع", "LONG"

            elif price > vwap_15m and price > poc_price_1h and obv_slope_15m > 0:
                strategy_id, strategy_name, trade_type = 129, "دعم مزدوج (VWAP + POC) مع OBV", "LONG"
            elif price < vwap_15m and price < poc_price_1h and obv_slope_15m < 0:
                strategy_id, strategy_name, trade_type = 130, "مقاومة مزدوجة (VWAP + POC) مع OBV", "SHORT"

            elif williams_r_1h < -80 and williams_r_15m > -50 and mfi_15m > 50:
                strategy_id, strategy_name, trade_type = 131, "تعافي سريع من قاع Williams", "LONG"
            elif williams_r_1h > -20 and williams_r_15m < -50 and mfi_15m < 50:
                strategy_id, strategy_name, trade_type = 132, "سقوط سريع من قمة Williams", "SHORT"

            elif cmf_1h > 0.15 and taker_buy_ratio_1h > 1.3 and price > ema_20_1h:
                strategy_id, strategy_name, trade_type = 133, "ضغط شراء ماركت مع CMF عالي", "LONG"
            elif cmf_1h < -0.15 and taker_buy_ratio_1h < 0.7 and price < ema_20_1h:
                strategy_id, strategy_name, trade_type = 134, "ضغط بيع ماركت مع CMF سلبي", "SHORT"

            elif change_24h > 15 and rsi_15m > 80 and volume_delta_15m < 0:
                strategy_id, strategy_name, trade_type = 135, "شورت عكسي سريع (بامب مفرط 24س)", "SHORT"
            elif change_24h < -15 and rsi_15m < 20 and volume_delta_15m > 0:
                strategy_id, strategy_name, trade_type = 136, "سكين ساقطة لونج (دامب مفرط 24س)", "LONG"

            elif price == ema_100_15m and macd_hist_15m > 0 and rsi_15m > 50:
                strategy_id, strategy_name, trade_type = 137, "ملامسة وارتداد من EMA 100 15د", "LONG"
            elif price == ema_100_15m and macd_hist_15m < 0 and rsi_15m < 50:
                strategy_id, strategy_name, trade_type = 138, "ملامسة وسقوط من EMA 100 15د", "SHORT"

            elif mfi_1h > 80 and cmf_1h < 0 and price < vwap_15m:
                strategy_id, strategy_name, trade_type = 139, "دايفرجنس السيولة (MFI عالي و CMF هابط)", "SHORT"
            elif mfi_1h < 20 and cmf_1h > 0 and price > vwap_15m:
                strategy_id, strategy_name, trade_type = 140, "دايفرجنس السيولة (MFI هابط و CMF صاعد)", "LONG"

            elif stochastic_k_15m > 80 and williams_r_15m > -20 and price >= bb_upper_15m:
                strategy_id, strategy_name, trade_type = 141, "ثلاثي التشبع الشرائي السريع (شورت)", "SHORT"
            elif stochastic_k_15m < 20 and williams_r_15m < -80 and price <= bb_lower_15m:
                strategy_id, strategy_name, trade_type = 142, "ثلاثي التشبع البيعي السريع (لونج)", "LONG"

            elif adx_15m > 40 and rsi_15m > 70 and macd_hist_15m > 0:
                strategy_id, strategy_name, trade_type = 143, "ترند سكالبينج متفجر للأعلى", "LONG"
            elif adx_15m > 40 and rsi_15m < 30 and macd_hist_15m < 0:
                strategy_id, strategy_name, trade_type = 144, "ترند سكالبينج متفجر للأسفل", "SHORT"

            elif orderbook_imbalance_ratio > 0.7 and whale_net_flow_volume > 0 and price > ema_20_15m:
                strategy_id, strategy_name, trade_type = 145, "هجوم الحيتان والأوردر بوك (لونج)", "LONG"
            elif orderbook_imbalance_ratio < -0.7 and whale_net_flow_volume < 0 and price < ema_20_15m:
                strategy_id, strategy_name, trade_type = 146, "هجوم الحيتان والأوردر بوك (شورت)", "SHORT"

            elif choppiness_index_1h > 61.8 and macd_hist_15m > 0 and rsi_15m == 50:
                strategy_id, strategy_name, trade_type = 147, "شراء تقاطع منتصف المسار العرضي", "LONG"
            elif choppiness_index_1h > 61.8 and macd_hist_15m < 0 and rsi_15m == 50:
                strategy_id, strategy_name, trade_type = 148, "بيع تقاطع منتصف المسار العرضي", "SHORT"

            elif price > supertrend_15m and price > parabolic_sar_15m and rsi_15m < 65:
                strategy_id, strategy_name, trade_type = 149, "سوبر تريند مع بارابوليك (صعود)", "LONG"
            elif price < supertrend_15m and price < parabolic_sar_15m and rsi_15m > 35:
                strategy_id, strategy_name, trade_type = 150, "سوبر تريند مع بارابوليك (هبوط)", "SHORT"


            # ==========================================
            # 🚀 3. تنفيذ الصفقة في حال تحقق أي استراتيجية
            # ==========================================
            if strategy_id > 0:
                await execute_trade(ADMIN_ID, coin_name, trade_type, price, strategy_id, strategy_name)
                # بمجرد العثور على فرصة للعملة وتفعيلها، ننتقل للعملة التي تليها فوراً
                continue 

    except Exception as e: 
        import logging 
        logging.error(f"❌ خطأ داخلي في دالة الاستراتجيات v11.2: {e}")

    print("✅ تم الانتهاء من مسح الاستراتيجيات (v11.2) بنجاح.")



async def execute_trade(user_id, coin_name, trade_type, entry_price, strategy_id, strategy_name, used_amount=0.5, leverage=50):
    """
    دالة فتح الصفقة بدقة بينانس:
    1. تمنع فتح صفقة لعملة موجودة مسبقاً في وضع "نشطة" (حتى لو من استراتيجية أخرى).
    2. تمنع فتح أكثر من 5 صفقات نشطة لنفس الاستراتيجية في نفس الوقت.
    3. تفتح الصفقة بـ 0.5 دولار (هامش).
    4. تخصم الرسوم والهامش من رصيد المحفظة الفعلي.
    5. تحسب الأهداف والوقف بناءً على الكمية (Coin Shares) لدقة 100%.
    """
    try:
        # ==========================================
        # 0. التحقق الصارم الأول: هل العملة نشطة في أي استراتيجية أخرى لنفس اللاعب؟
        # ==========================================
        active_check = supabase.table("active_trades").select("id").eq("user_id", str(user_id)).eq("coin_name", coin_name).eq("status", "نشطة").execute()
        
        if active_check.data:
            print(f"⚠️ تجاهل فتح الصفقة: توجد صفقة 'نشطة' بالفعل للعملة {coin_name} (سواء في هذه الاستراتيجية أو غيرها).")
            return False

        # ==========================================
        # 0.5 التحقق الصارم الثاني: هل الاستراتيجية وصلت للحد الأقصى (5 صفقات نشطة)؟
        # ==========================================
        strategy_trades_check = supabase.table("active_trades").select("id").eq("user_id", str(user_id)).eq("strategy_id", strategy_id).eq("status", "نشطة").execute()
        
        # إذا كان عدد الصفقات النشطة لهذه الاستراتيجية 5 فما فوق، نمنع فتح صفقة جديدة
        if strategy_trades_check.data and len(strategy_trades_check.data) >= 2:
            print(f"⏳ تجاهل فتح صفقة {coin_name}: الاستراتيجية رقم {strategy_id} ('{strategy_name}') وصلت للحد الأقصى (5 صفقات نشطة). ننتظر إغلاق إحداها.")
            return False

        # ==========================================
        # 1. التحقق من المحفظة وجلب الرصيد
        # ==========================================
        portfolio_res = supabase.table("portfolio").select("*").eq("player_name", str(user_id)).eq("strategy_id", strategy_id).execute()

        if not portfolio_res.data:
            print(f"⚠️ لا توجد محفظة للاستراتيجية '{strategy_name}'. جاري إنشاء واحدة...")
            
            new_portfolio_data = {
                "player_name": str(user_id),
                "strategy_id": strategy_id,
                "strategy_name": strategy_name,
                "previous_balance": 40.0,
                "current_balance": 40.0,
                "pnl_percentage": 0.0,
                "leverage": 45,
                "spot_balance": 0.0,
                "spot_leverage": 1
            }
            
            insert_port_res = supabase.table("portfolio").insert(new_portfolio_data).execute()
            
            if insert_port_res.data:
                portfolio_id = insert_port_res.data[0]['id']
                current_balance = 40.0
                leverage = 45
            else:
                logging.error("❌ فشل إنشاء المحفظة، سيتم إلغاء فتح الصفقة.")
                return False
        else:
            portfolio_id = portfolio_res.data[0]['id']
            current_balance = float(portfolio_res.data[0].get("current_balance", 0.0))
            leverage = int(portfolio_res.data[0].get("leverage", leverage))

        # ==========================================
        # 2. الحسابات الرياضية الدقيقة (Binance Math)
        # ==========================================
        notional_size = used_amount * leverage               # حجم العقد (مثال: 0.5 * 50 = 25$)
        coin_shares = notional_size / entry_price            # كمية العملات الفعلية (الأساس لكل الحسابات)
        borrowed_amount = notional_size - used_amount        
        
        # رسوم فتح الصفقة (Taker Fee 0.040%)
        open_fee = notional_size * 0.0004 
        
        # التكلفة الإجمالية لفتح الصفقة (الهامش المستخدم + الرسوم)
        total_cost = used_amount + open_fee

        # التحقق من أن الرصيد يكفي
        if current_balance < total_cost:
            print(f"❌ رصيد المحفظة ({current_balance}$) غير كافٍ لفتح الصفقة (المطلوب {total_cost}$).")
            return False

        # ==========================================
        # 3. حساب مستويات المخاطرة والأهداف بدقة (Target USD / Coin Shares)
        # ==========================================
        mmr = 0.004 # هامش الصيانة (0.4%)
        trade_type_upper = trade_type.upper()
        
        if trade_type_upper in ["LONG", "شراء"]:
            # في الشراء: السعر ينزل فنطرح الخسارة، ويرتفع فنجمع الربح
            support_zone = entry_price - (0.5 / coin_shares)  # خسارة 0.5$ بالضبط (منطقة التعزيز)
            stop_loss = entry_price - (2.0 / coin_shares)     # خسارة 1.0$ بالضبط
            
            target_1 = entry_price + (1.5 / coin_shares)      # ربح 1.5$
            target_2 = entry_price + (2.5 / coin_shares)      # ربح 2.5$
            target_3 = entry_price + (4.0 / coin_shares)      # ربح 4.0$
            
            liquidation_price = entry_price * (1 - (1/leverage) + mmr)
            
        else: # SHORT (بيع)
            # في البيع: السعر يرتفع فنجمع الخسارة، وينزل فنطرح الربح
            support_zone = entry_price + (0.5 / coin_shares)  # خسارة 0.5$ بالضبط (منطقة التعزيز)
            stop_loss = entry_price + (2.0 / coin_shares)     # خسارة 1.0$ بالضبط
            
            target_1 = entry_price - (1.5 / coin_shares)      # ربح 1.5$
            target_2 = entry_price - (2.5 / coin_shares)      # ربح 2.5$
            target_3 = entry_price - (4.0 / coin_shares)      # ربح 4.0$
            
            liquidation_price = entry_price * (1 + (1/leverage) - mmr)

        # ==========================================
        # 4. خصم الرصيد من المحفظة (Portfolio Update)
        # ==========================================
        new_balance = current_balance - total_cost
        update_port_res = supabase.table("portfolio").update({
            "current_balance": new_balance
        }).eq("id", portfolio_id).execute()

        if not update_port_res.data:
            logging.error("❌ فشل تحديث رصيد المحفظة.")
            return False

        print(f"💰 تم خصم {round(total_cost, 4)}$ من المحفظة. الرصيد المتبقي: {round(new_balance, 4)}$")

        # ==========================================
        # 5. إدراج الصفقة في جدول الصفقات النشطة وإرسال الإشعار
        # ==========================================
        trade_data = {
            "user_id": str(user_id),
            "strategy_id": strategy_id,
            "strategy_used_name": strategy_name,
            "coin_name": coin_name,
            "trade_type": trade_type_upper,
            "leverage": leverage,
            "used_amount": round(used_amount, 4),
            "borrowed_amount": round(borrowed_amount, 4),
            "coin_shares": round(coin_shares, 8),
            "entry_price": round(entry_price, 8),
            "current_price": round(entry_price, 8), 
            "highest_price_reached": round(entry_price, 8),
            "lowest_price_reached": round(entry_price, 8),
            "support_zone": round(support_zone, 8),
            "stop_loss": round(stop_loss, 8),
            "target_1": round(target_1, 8),
            "target_2": round(target_2, 8),
            "target_3": round(target_3, 8),
            "liquidation_price": round(liquidation_price, 8),
            "trading_fees": round(open_fee, 4), 
            "status": "نشطة"
        }

        insert_res = supabase.table("active_trades").insert(trade_data).execute()

        if insert_res.data:
            print(f"✅ تم فتح صفقة {trade_type} لـ {coin_name} بنجاح.")
            print(f"📉 منطقة الدعم (-0.5$): {round(support_zone, 6)} | 🛑 الوقف (-1.0$): {round(stop_loss, 6)}")
            
            # ------------------------------------------
            # تجهيز رسالة الإشعار وإرسالها للتليجرام
            # ------------------------------------------
            trade_icon = "🟢" if trade_type_upper in ["LONG", "شراء"] else "🔴"
            trade_label = "شراء" if trade_type_upper in ["LONG", "شراء"] else "بيع"
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            notification_msg = (
                "ــــــــــــــــــــــــــــــــــــ\n\n"
                f"{trade_icon} نوع الصفقة : {trade_label}\n"
                f"🎯 إسم الإستراتيجية : {strategy_name}\n"
                f"🔢 رقم الاستراتجية : {strategy_id}\n"
                f"💸 إسم العملة : #{coin_name}\n"
                f"🔄 الرافعة المالية : {leverage}\n"
                f"💳 الكمية : {round(coin_shares, 4)}\n"
                f"📊 المبلغ : {round(used_amount, 2)}\n"
                f"🧾 الإقتراض : {round(borrowed_amount, 2)}\n"
                f"📈 سعر الدخول : {round(entry_price, 6)}\n"
                f"⁦🔼 منطقة الدعم : {round(support_zone, 6)}\n"
                f"🚫 وقف الخسارة : {round(stop_loss, 6)}\n"
                f"🥇 الهدف الاول : {round(target_1, 6)}\n"
                f"🥈 الهدف الثاني : {round(target_2, 6)}\n"
                f"🥉 الهدف الثالث : {round(target_3, 6)}\n"
                f"🕛 وقت فتح الصفقة: {current_time}\n\n"
                "ــــــــــــــــــــــــــــــــــــ"
            )
            
            # بدلاً من استدعاء الدالة بدون معرف، مرر لها tell_2
            await send_telegram_notification(notification_msg, tell_1)
            
            return True
        else:
            # إعادة الرصيد في حال فشل إدراج الصفقة (Rollback)
            supabase.table("portfolio").update({"current_balance": current_balance}).eq("id", portfolio_id).execute()
            logging.error("❌ فشل إدراج الصفقة، تم إرجاع الرصيد للمحفظة.")
            return False

    except Exception as e:
        logging.error(f"❌ حدث خطأ غير متوقع: {e}")
        return False
# ==========================================
# 📊 دالة المراقبة الرئيسية (المصححة)
# ==========================================
import asyncio
import logging
from datetime import datetime, timezone
# يفترض استيراد المكتبات اللازمة مثل AsyncClient و send_telegram_notification وغيرها في بداية الملف

async def monitor_active_trades(supabase):
    try:
        # 1. جلب الصفقات النشطة
        res = supabase.table("active_trades").select("*").eq("status", "نشطة").execute()
        active_trades = res.data

        if not active_trades:
            return  

        # 2. إنشاء اتصال وتجهيز قاموس الأسعار
        client = await AsyncClient.create(API_KEY, SECRET_KEY)
        current_prices_dict = {}
        
        try:
            tickers = await client.futures_symbol_ticker()
            for item in tickers:
                current_prices_dict[item['symbol'].upper()] = float(item['price'])
        finally:
            await client.close_connection()

        if not current_prices_dict:
            logging.warning("⚠️ لم يتم العثور على أي أسعار من بينانس.")
            return

        # 3. معالجة الصفقات
        for trade in active_trades:
            try:  # <--- حماية كل صفقة بشكل منفصل حتى لا تتوقف المراقبة
                trade_id = trade['id']
                
                # معالجة اسم العملة لضمان تطابقه مع بينانس
                raw_coin_name = str(trade['coin_name']).replace('#', '').strip().upper()
                search_symbol = raw_coin_name if "USDT" in raw_coin_name else raw_coin_name + "USDT"
                
                if search_symbol not in current_prices_dict:
                    if raw_coin_name in current_prices_dict:
                        search_symbol = raw_coin_name
                    else:
                        logging.warning(f"⚠️ تخطي الصفقة {trade_id}: العملة {raw_coin_name} غير موجودة في بينانس.")
                        continue
                        
                current_price = current_prices_dict[search_symbol]
                
                trade_type = str(trade['trade_type']).upper()
                is_long = trade_type in ["LONG", "شراء"]
                
                user_id = str(trade['user_id'])
                strategy_id = int(trade.get('strategy_id') or 0)
                
                entry_price = float(trade['entry_price'])
                stop_loss = float(trade.get('stop_loss') or 0.0)
                support_zone = float(trade.get('support_zone') if trade.get('support_zone') is not None else 0.0)
                
                used_amount = float(trade['used_amount'])
                coin_shares = float(trade['coin_shares'])
                leverage = int(trade['leverage'])
                
                updates = {}
                close_trade = False
                close_reason = ""
                
                # تحديث أعلى وأدنى سعر
                highest = float(trade.get('highest_price_reached') or entry_price)
                lowest = float(trade.get('lowest_price_reached') or entry_price)
                if current_price > highest: 
                    highest = current_price
                    updates['highest_price_reached'] = highest
                if current_price < lowest: 
                    lowest = current_price
                    updates['lowest_price_reached'] = lowest

                # =======================================================
                # نظام المطاردة وتعديل وقف الخسارة (Trailing Stop-Loss)
                # =======================================================
                
                # حساب أقصى ربح وصل له السعر كنسبة مئوية من رأس المال المستخدم
                max_pnl = ((highest - entry_price) if is_long else (entry_price - lowest)) * coin_shares
                max_pnl_percentage = (max_pnl / used_amount) * 100

                new_stop_loss = stop_loss

                if max_pnl_percentage >= 1.0:
                    # إذا استمر الربح إلى 1.0 فما فوق، يطارد السعر ويبتعد عنه بنسبة 0.50
                    target_trailing_pnl_percent = max_pnl_percentage - 0.50
                    price_diff = (target_trailing_pnl_percent * used_amount) / (100 * coin_shares)
                    
                    calculated_sl = entry_price + price_diff if is_long else entry_price - price_diff
                    
                    if is_long and calculated_sl > stop_loss:
                        new_stop_loss = calculated_sl
                    elif not is_long and (stop_loss == 0 or calculated_sl < stop_loss):
                        new_stop_loss = calculated_sl

                elif max_pnl_percentage >= 0.50:
                    # تحريك الوقف إلى سعر الدخول + فوقه بقليل لضمان رسوم المنصة
                    # رسوم المنصة التقريبية للذهاب والعودة هي 0.08% من حجم العقد
                    price_diff_for_breakeven = (entry_price * 0.0008) 
                    breakeven_sl = entry_price + price_diff_for_breakeven if is_long else entry_price - price_diff_for_breakeven
                    
                    if is_long and breakeven_sl > stop_loss:
                        new_stop_loss = breakeven_sl
                    elif not is_long and (stop_loss == 0 or breakeven_sl < stop_loss):
                        new_stop_loss = breakeven_sl

                # تطبيق الوقف الجديد إذا تغير نحو الأرباح
                if new_stop_loss != stop_loss:
                    updates['stop_loss'] = new_stop_loss
                    stop_loss = new_stop_loss

                # =======================================================
                # التحقق من ضرب وقف الخسارة (الأساسي أو التتبعي)
                # =======================================================
                if stop_loss > 0:
                    if (is_long and current_price <= stop_loss) or (not is_long and current_price >= stop_loss):
                        close_trade = True
                        
                        # حساب صافي الأرباح اللحظية لمعرفة ما إذا كانت الصفقة أغلقت بربح أم بخسارة
                        final_pnl = ((current_price - entry_price) if is_long else (entry_price - current_price)) * coin_shares
                        final_fees = (used_amount * leverage) * 0.0004
                        net_final_pnl = final_pnl - final_fees
                        
                        # تغيير وصف الإغلاق بناءً على النتيجة الموجبة أو السالبة
                        if net_final_pnl > 0:
                            close_reason = "ناجحة - جني أرباح تتبعي (Trailing Stop) 🚀"
                        else:
                            close_reason = "ضرب وقف الخسارة (SL) ❌"

                # =======================================================
                # أنظمة التعزيز والتخفيف (إذا لم تُغلق الصفقة)
                # =======================================================
                if not close_trade:
                    # نظام التعزيز (DCA)
                    if support_zone > 0: 
                        hit_support = (is_long and current_price <= support_zone) or (not is_long and current_price >= support_zone)

                        if hit_support:
                            port_res = supabase.table("portfolio").select("id, current_balance").eq("player_name", user_id).eq("strategy_id", strategy_id).execute()
                            if port_res.data:
                                port_id = port_res.data[0]['id']
                                current_bal = float(port_res.data[0]['current_balance'])
                                dca_amount = used_amount 
                                total_dca_cost = dca_amount + (dca_amount * leverage * 0.0004)
                                
                                if current_bal >= total_dca_cost:
                                    supabase.table("portfolio").update({"current_balance": current_bal - total_dca_cost}).eq("id", port_id).execute()
                                    new_shares = (dca_amount * leverage) / current_price
                                    updates['used_amount'] = used_amount + dca_amount
                                    updates['coin_shares'] = coin_shares + new_shares
                                    updates['entry_price'] = ((used_amount + dca_amount) * leverage) / (coin_shares + new_shares)
                                    updates['support_zone'] = -1  
                                    
                                    entry_price, used_amount, coin_shares = updates['entry_price'], updates['used_amount'], updates['coin_shares']
                                    logging.info(f"🔄 تعزيز تم.")
                                else:
                                    updates['support_zone'] = -2 

                    # نظام تخفيف المخاطرة
                    elif support_zone == -1: 
                        in_profit = (is_long and current_price > entry_price) or (not is_long and current_price < entry_price)
                        if in_profit:
                            port_res = supabase.table("portfolio").select("id, current_balance").eq("player_name", user_id).eq("strategy_id", strategy_id).execute()
                            if port_res.data:
                                port_id = port_res.data[0]['id']
                                current_bal = float(port_res.data[0]['current_balance'])
                                
                                partial_pnl = ((current_price - entry_price) if is_long else (entry_price - current_price)) * (coin_shares / 2)
                                return_to_wallet = (used_amount / 2) + partial_pnl - ((used_amount / 2 * leverage) * 0.0004)
                                
                                supabase.table("portfolio").update({"current_balance": current_bal + return_to_wallet}).eq("id", port_id).execute()
                                updates['used_amount'] = used_amount / 2
                                updates['coin_shares'] = coin_shares / 2
                                updates['support_zone'] = current_price * 0.995 if is_long else current_price * 1.005
                                used_amount, coin_shares = updates['used_amount'], updates['coin_shares']


                # =======================================================
                # تحديث قاعدة البيانات وإغلاق الصفقة
                # =======================================================
                if close_trade:
                    pnl_value = ((current_price - entry_price) if is_long else (entry_price - current_price)) * coin_shares
                    closing_fee = (used_amount * leverage) * 0.0004
                    net_pnl = pnl_value - closing_fee
                    
                    # استرجاع مبلغ الصفقة + الربح الصافي (نفس بينانس بالضبط)
                    total_return_to_wallet = used_amount + net_pnl
                    pnl_percentage = (pnl_value / used_amount) * 100

                    # تحديث المحفظة
                    current_bal = 0.0
                    try:
                        port_res = supabase.table("portfolio").select("id, current_balance").eq("player_name", user_id).eq("strategy_id", strategy_id).execute()
                        if port_res.data:
                            port_id = port_res.data[0]['id']
                            current_bal = float(port_res.data[0]['current_balance'])
                            supabase.table("portfolio").update({"current_balance": current_bal + total_return_to_wallet}).eq("id", port_id).execute()
                    except Exception as e:
                        logging.error(f"خطأ تحديث المحفظة: {e}")

                    close_updates = {
                        "status": "مغلقة",
                        "close_price": current_price,
                        "close_reason": close_reason,
                        "realized_pnl": round(net_pnl, 4), 
                        "pnl_percentage": round(pnl_percentage, 2),
                        "closed_at": datetime.now(timezone.utc).isoformat()
                    }
                    close_updates.update(updates) 
                    
                    supabase.table("active_trades").update(close_updates).eq("id", trade_id).execute()
                    logging.info(f"🏁 إغلاق {raw_coin_name} | السبب: {close_reason}")
                    
                    # ----------------- تجهيز إشعار الإغلاق -----------------
                    trade_icon = "🟢" if is_long else "🔴"
                    trade_type_str = "شراء (LONG)" if is_long else "بيع (SHORT)"
                    
                    created_at_str = trade.get('created_at')
                    time_spent_str = "أقل من دقيقة"
                    if created_at_str:
                        try:
                            dt = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                            dt = dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt
                            time_spent = datetime.now(timezone.utc) - dt
                            days, seconds = time_spent.days, time_spent.seconds
                            h, m = seconds // 3600, (seconds % 3600) // 60
                            time_parts = [f"{x} {y}" for x, y in zip([days, h, m], ["يوم", "ساعة", "دقيقة"]) if x > 0]
                            if time_parts: time_spent_str = " و ".join(time_parts)
                        except: pass

                    strategy_name = trade.get('strategy_used_name', 'غير محدد')
                    
                    msg_lines = [
                        "ــــــــــــــــــــــــــــــــــــ", "",
                        f"{trade_icon} نوع الصفقة : {trade_type_str}",
                        f"🎯 إسم الإستراتيجية : {strategy_name}",
                        f"🔢 رقم الاستراتجية : {strategy_id}",
                        f"💸 إسم العملة : #{raw_coin_name}",
                        f"🔄 الرافعة المالية : {leverage}x",
                        f"💳 الكمية : {format_num(coin_shares, 4)}",
                        f"📊 المبلغ : {format_num(used_amount, 2)}$",
                        f"🧾 الإقتراض : {format_num(used_amount * leverage, 2)}$",
                        f"📈 سعر الدخول : {format_num(entry_price)}",
                        f"⁦📝 سعر الإغلاق : {format_num(current_price)}",
                        f"🔼 اقصى سعر : {format_num(highest)}",
                        f"🔽 أذنى سعر : {format_num(lowest)}",
                        f"💵 الربح او الخسارة : {format_num(net_pnl, 4)}$",
                        f"🧾 النسبة المؤية : {format_num(pnl_percentage, 2)}%",
                        f"🕛 الوقت المستغرق : {time_spent_str}",
                        f"🤔 سبب الإغلاق : {close_reason}",
                        f"💸 خصم رسوم الصفقة : {format_num(closing_fee, 4)}$",
                        f"💳 رصيد المحفظة الاستراتجية : {format_num(current_bal + total_return_to_wallet, 2)}$",
                        "", "ــــــــــــــــــــــــــــــــــــ"
                    ]
                    notification_msg = "\n".join(msg_lines)

                    # إرسال الإشعار في الخلفية
                    asyncio.create_task(send_telegram_notification(notification_msg, tell_2))       
                    
                    # إيقاظ الرادار للبحث عن فرصة جديدة
                    logging.info("♻️ تم إغلاق صفقة، جاري إيقاظ الرادار للبحث عن فرصة جديدة...")
                    asyncio.create_task(intelligence_scanner())
                    
                else: 
                    # التحديث المستمر للسعر والنسبة (مهم جداً للوحة التحكم)
                    updates['current_price'] = current_price
                    unrealized_pnl = ((current_price - entry_price) if is_long else (entry_price - current_price)) * coin_shares
                    updates['pnl_percentage'] = round((unrealized_pnl / used_amount) * 100, 2)
                    
                    supabase.table("active_trades").update(updates).eq("id", trade_id).execute()

            except Exception as e:
                logging.error(f"❌ خطأ داخلي في معالجة الصفقة {trade.get('id')}: {e}")
                continue # ننتقل للصفقة التالية إذا حدث خطأ في صفقة واحدة

    except Exception as e:
        logging.error(f"❌ حدث خطأ رئيسي في دالة المراقبة: {e}")

# 1. 🟢 ضع هذا الكلاس قبل "نظام الإنعاش الأبدي" (في منطقة عامة خارج الدوال)
class TelegramLoggerHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        if record.levelno >= logging.ERROR:
            try:
                loop = asyncio.get_event_loop()
                loop.create_task(self.send_log(log_entry))
            except RuntimeError:
                pass

    async def send_log(self, message):
        try:
            msg = f"⚠️ <b>تنبيـه خطأ في النظام:</b>\n<code>{message[:3500]}</code>"
            await self.bot.send_message(self.chat_id, msg, parse_mode="HTML")
        except Exception:
            pass

# ==========================================
# 5. نهاية الملف: نظام الإنعاش الأبدي 24/7 (النبض الذاتي) ⚡
# ==========================================
import os
import asyncio
import logging
import random
import aiohttp
from aiohttp import web

async def handle_ping(request):
    """استجابة سريعة لإخبار السيرفر أن النظام مستيقظ"""
    return web.Response(
        text="Alive & Vigilant ⚡", 
        headers={"Connection": "keep-alive"}
    )


async def handle_telegram_login(request):
    return web.Response(text="✅ Data Received")


async def self_resuscitation():
    """النبض الذاتي: البوت يوقظ نفسه لمنع النوم (Anti-Idle)"""
    render_url = os.getenv("RENDER_EXTERNAL_URL") 
    if not render_url: return

    while True:
        try:
            # كسر التخزين المؤقت لضمان وصول الطلب للمعالج مباشرة
            rand_ping = f"{render_url}?v={random.randint(1, 99999)}"
            async with aiohttp.ClientSession() as session:
                async with session.get(rand_ping, timeout=10) as response:
                    logging.info(f"💉 [نبضة حية]: {response.status}")
        except Exception as e:
            logging.error(f"⚠️ [فشل النبض]: {e}")
        
        await asyncio.sleep(240) # كل 4 دقائق


async def watch_dog(task_func, *args):
    """
    بروتوكول اليقظة: مراقب دائم للمحركات.
    إذا توقف أي محرك (سنة) أو انهار (نوم)، يعيده للحياة فوراً.
    """
    while True:
        try:
            logging.info(f"🛡️ تشغيل محرك: {task_func.__name__}")
            await task_func(*args)
        except Exception as e:
            logging.error(f"🚨 انهيار في {task_func.__name__}: {e}")
            logging.info("♻️ إعادة التشغيل التلقائي الآن...")
            await asyncio.sleep(10) # انتظار بسيط لتجنب التكرار السريع عند الخطأ


async def auto_evaluation_scheduler():
    """
    مجدول زمني شبحي يعمل في الخلفية لتقييم الصفقات كل 12 ساعة.
    """
    while True:
        try:
            print(f"🔄 [مجدول التقييم] بدء فحص الإشارات القديمة في: {datetime.now().strftime('%H:%M:%S')}")
            await evaluate_old_signals()
        except Exception as e:
            print(f"⚠️ خطأ في المجدول الزمني: {e}")
        
        # النوم لمدة 12 ساعة (بثواني) قبل الفحص التالي
        await asyncio.sleep(12 * 60 * 60)

# 🗑️ قم بحذف دالة scanner_loop نهائياً من الكود

async def monitor_loop():
    """حلقة تكرار لمراقبة الصفقات المفتوحة وإغلاقها عند الهدف/الوقف"""
    while True:
        try:
            await monitor_active_trades(supabase)
        except Exception as e:
            logging.error(f"❌ خطأ في حلقة المراقبة: {e}")
        # المراقبة كل 10 ثواني لضمان سرعة الاستجابة لضرب الأهداف
        await asyncio.sleep(10)


    # ... تشغيل polling التلجرام ...
# ---async def main_startup ---
async def main_startup():
    # 2. 🟢 ضع هذا الإعداد هنا في أول سطر داخل دالة main_startup
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(), # للطباعة في شاشة راندر كالعادة
            TelegramLoggerHandler(bot, GROUP_ID) # ليرسل الأخطاء للقروب فوراً
        ]
    )

    # أ) إعداد سيرفر الويب للبقاء Online (مهم للمنصات مثل Render/Heroku)
    app = web.Application()
    app.router.add_get('/', handle_ping)
    app.router.add_get('/login', handle_telegram_login)
    
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"🌐 Server Active on port {port}")

    asyncio.create_task(monitor_loop())
    
    # ج) تشغيل البوت الرئيسي (Aiogram) مع نظام إعادة المحاولة الصامد
    while True:
        try:
            logging.info("🚀 إقلاع محرك التليجرام... النظام تحت الحماية القصوى.")
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)
        except Exception as e:
            logging.error(f"❌ خطأ في البوت: {e}")
            logging.info("🔄 محاولة إعادة التشغيل تلقائياً خلال 10 ثوانٍ...")
            await asyncio.sleep(20)
    
# ---if __name__ == '__main__':---
if __name__ == '__main__':
    try:
        # تشغيل المحرك الرئيسي
        
        asyncio.run(main_startup())
    except KeyboardInterrupt:
        print("🛑 تم إيقاف النظام يدوياً من قبل أثير.")
    except Exception as e:
        # 🟢 طباعة إجبارية باللون الأحمر في راندر لكشف الخطأ القاتل
        print("\n" + "❌"*20)
        print(f"💥 انهيار قاتل منع البوت من الإقلاع:")
        print(f"{type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        print("❌"*20 + "\n")
        
        logging.critical(f"💥 انهيار غير متوقع في النظام: {e}")
