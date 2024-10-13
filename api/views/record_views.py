import pytz
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Record
from datetime import datetime

@api_view(['POST'])
def addrecord(request):
    # 確認使用者是否已登入
    if 'email' not in request.session:
        return Response({"error": "使用者未登入"}, status=status.HTTP_401_UNAUTHORIZED)

    # 從 session 取得使用者 email
    user_email = request.session['email']

    # 從請求中取得其他資料
    count = request.data.get('count')
    datetime_str = request.data.get('datetime')
    left_errors = request.data.get('left_errors', 0)
    right_errors = request.data.get('right_errors', 0)
    sport_time = request.data.get('sport_time')

    # 驗證欄位是否為空
    if not all([count, datetime_str, sport_time]):
        return Response({"error": "缺少必要的欄位"}, status=status.HTTP_400_BAD_REQUEST)

    # 調整時間格式並改為台灣台北時區
    try:
        # 將字串轉為 datetime
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        # 設置為台灣台北時間
        taipei_tz = pytz.timezone('Asia/Taipei')
        datetime_obj = taipei_tz.localize(datetime_obj)  # 將 datetime 設為台灣台北時間
    except ValueError:
        return Response({"error": "日期時間格式不正確，應為 'YYYY-MM-DD HH:MM:SS'"}, status=status.HTTP_400_BAD_REQUEST)

    # 建立運動紀錄
    try:
        record = Record(
            user_email=user_email,
            count=count,
            datetime=datetime_obj,
            left_errors=left_errors,
            right_errors=right_errors,
            sport_time=sport_time
        )
        record.save()
        return Response({"message": "運動紀錄新增成功"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
