from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .serializers import SignupSerializer, LoginSerializer
from plans.models import BudgetPlan
from plans.views import DailyPlanView
from plans.serializers import MonthlyPlanSerializer
from payments.models import Payment
from payments.views import DailyPaymentView
from .models import User


class SignUpView(APIView):
    """
    POST : 회원가입
    """

    def get(self, request):
        return Response({"message": "username, password를 입력해주세요."})

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user_id": user.id,
                    "username": user.username,
                    "message": "회원가입이 완료되었습니다.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    POST : 로그인
    """

    def get(self, request):
        return Response({"message": "username, password를 입력해주세요."})

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None or password is None:
            return Response(
                {"message": "username, password를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            serializer = LoginSerializer(user)

            # simple jwt 토큰 발급
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            refresh_token = str(token)

            res = Response(
                {
                    "user_id": user.id,
                    "username": user.username,
                    "message": "로그인이 완료되었습니다.",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            request.session["refresh_token"] = refresh_token
            res.set_cookie("access_token", access_token, httponly=True)

            return res
        else:
            return Response(
                {"message": "아이디 또는 비밀번호가 일치하지 않습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    """
    POST : 로그아웃
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "로그아웃 하시겠습니까?"})

    def post(self, request):
        # 쿠키에서 access_token 삭제
        response = Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")

        # 세션에서 refresh_token 가져오기
        refresh_token = request.session.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                del request.session["refresh_token"]
            except Exception as e:
                print(e)

            return response

        logout(request)
        return response


class MyPageView(APIView):
    """
    GET : 마이페이지(한달 예산 계획 / 한달 지출 금액 / 일일 예산 / 일일 지출 금액)
    """

    pass
