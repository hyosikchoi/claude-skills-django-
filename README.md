# shopping-mall-api

쇼핑몰 Django REST API 프로젝트

## 아키텍처

```
Request → ViewSet → Controller → Service → Model
            ↓
        Serializer (검증/직렬화)
            ↓
        Response
```

## 프로젝트 구조

```
shopping-mall-api/
├── configs/              # Django 설정
│   └── settings/
│       ├── base.py
│       ├── local.py
│       └── test.py
├── commons/              # 공통 유틸리티
│   ├── const/
│   │   └── choices.py    # UserRoleChoice, ProductStatusChoice, PaymentStatusChoice
│   └── urls.py           # 루트 URL 설정
├── apis/                 # API 계층
│   ├── commons/          # 공통 ViewSet, Permission, ErrorCode
│   ├── accounts/         # 로그인/로그아웃/회원가입
│   ├── products/         # 상품 CRUD
│   └── payments/         # 결제/영수증
└── domains/              # 비즈니스 로직
    ├── commons/          # BaseModel, BaseService
    ├── accounts/
    │   ├── models/       # User
    │   └── services/     # AuthService
    ├── products/
    │   ├── models/       # Product
    │   └── services/     # ProductService
    └── payments/
        ├── models/       # Receipt, ReceiptDetail
        └── services/     # PaymentService
```

## 도메인 모델

| 모델 | 설명 |
|------|------|
| `User` | 사용자 (role: ADMIN / USER) |
| `Product` | 상품 (status: ACTIVE / INACTIVE / SOLD_OUT) |
| `Receipt` | 결제 영수증 (status: PENDING / COMPLETED / CANCELLED / REFUNDED) |
| `ReceiptDetail` | 영수증 상세 (구매 상품 내역) |

## API 엔드포인트

### Auth (인증)
| Method | URL | 설명 | 권한 |
|--------|-----|------|------|
| POST | `/api/accounts/auth/register` | 회원가입 | 누구나 |
| POST | `/api/accounts/auth/login` | 로그인 | 누구나 |
| POST | `/api/accounts/auth/logout` | 로그아웃 | 로그인 필요 |
| GET | `/api/accounts/auth/me` | 내 정보 조회 | 로그인 필요 |

### Products (상품)
| Method | URL | 설명 | 권한 |
|--------|-----|------|------|
| GET | `/api/products` | 상품 목록 (페이징) | 누구나 |
| GET | `/api/products/{product_uuid}` | 상품 상세 | 누구나 |
| POST | `/api/products` | 상품 등록 | 관리자 |
| PATCH | `/api/products/{product_uuid}` | 상품 수정 | 관리자 |
| DELETE | `/api/products/{product_uuid}` | 상품 삭제 | 관리자 |

### Payments (결제)
| Method | URL | 설명 | 권한 |
|--------|-----|------|------|
| GET | `/api/payments` | 내 영수증 목록 (페이징) | 로그인 필요 |
| GET | `/api/payments/{receipt_uuid}` | 영수증 상세 | 로그인 필요 |
| POST | `/api/payments` | 결제 | 로그인 필요 |
| POST | `/api/payments/{receipt_uuid}/cancel` | 결제 취소 | 로그인 필요 |

## 환경 설정

1. Python 3.11+ 설치
2. 가상환경 생성 및 활성화
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. 의존성 설치
   ```bash
   pip install -e .[dev]
   ```
4. `.env` 파일 생성
   ```bash
   cp .env .env
   # .env 파일에서 DATABASE 설정 수정
   ```
5. 마이그레이션
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. 서버 실행
   ```bash
   python manage.py runserver
   ```

## API 문서

Swagger UI: http://localhost:8000/api/docs/
