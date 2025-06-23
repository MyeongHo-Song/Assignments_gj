# 은행 계좌 시스템 개발 학습 노트

## 📋 과제 개요
- **파일명**: assignment_1.py
- **작성자**: Kwanju Eun
- **작성일**: 2025-06-17
- **목표**: 다양한 유형의 은행 계좌(저축, 입출금, 마이너스 계좌)를 Python 클래스로 구현

## 🏗️ 클래스 구조

### BankAccount 클래스 속성
```python
class BankAccount:
    Unique_id = 1  # 클래스 변수 - 자동 ID 생성
    
    def __init__(self, username, password, account_type, interest_rate):
        self.__username = username      # 사용자명 (private)
        self.__password = password      # 비밀번호 (private)
        self.__account_type = account_type  # 계좌 유형 (private)
        self.__interest_rate = interest_rate # 이자율 (private)
        self.__balance = 0              # 잔액 (private)
        self.__created_date = datetime.now() # 생성일 (private)
        self.__id = BankAccount.Unique_id    # 고유 ID (private)
        BankAccount.Unique_id += 1      # 다음 ID 준비
```

## 🔧 주요 메소드 및 고민사항

### 1. 생성자 (`__init__`)
**고민**: 자동 ID 생성 방식
- **해결**: 클래스 변수 `Unique_id` 사용
- **장점**: 인스턴스 생성 시마다 자동으로 고유 ID 할당

### 2. 소멸자 (`__del__`)
**고민**: 과제 평가 항목에 "Initializer and Finalizer" 포함
- **해결**: `__del__` 메소드 추가
- **용도**: 객체 소멸 시 정리 작업 수행

### 3. 입금 메소드 (`deposit`)
**고민**: 반환값이 필요한가?
```python
def deposit(self, amount):
    if amount <= 0:
        print("Invalid amount")
    else:
        self.__balance += amount
        print(f"Deposit {amount} success. Current balance: {self.__balance}")
    # return 없음 - 자동으로 None 반환
```
**결론**: 작업 수행 + 결과 출력이 목적이므로 `return` 불필요

### 4. 출금 메소드 (`withdraw`)
**고민 1**: 비밀번호 검증 실패 시 처리
```python
if password != self.__password:
    print("Invalid password")
    return  # 함수 실행 중단
```
**해결**: `return`으로 함수 실행 중단

**고민 2**: `return` vs `break` 사용
- **결론**: `return` 사용 (함수 내에서 실행 중단)
- **이유**: `break`는 반복문에서만 사용 가능

**고민 3**: 계좌 유형별 출금 규칙
- **D/W_account**: 잔액 확인 후 출금
- **Saving_account**: 1년 경과 확인 후 출금
- **minus_account**: -500,000 한도 확인 후 출금

**구현된 로직**:
```python
elif self.__account_type=="Saving_account":
    current_date = datetime.now()
    time_diff = current_date - self.__created_date
    if time_diff.days >= 365:  # 1년 경과 확인
        if self.__balance >= amount:
            self.__balance -= amount
            print(f"Withdraw {amount} success. Current balance: {self.__balance}")
        else:
            print("Insufficient balance")
    else:
        print("Saving_account cannot withdraw before 1 year")
```

### 5. 잔액 조회 메소드 (`get_balance`)
**고민**: 출력 vs 반환
```python
# 잘못된 구현
def get_balance(self):
    print(f"Current balance: {self.__balance}")

# 올바른 구현
def get_balance(self):
    return self.__balance
```
**결론**: 값을 반환하는 것이 목적이므로 `return` 사용

### 6. 계좌 정보 출력 메소드 (`show_account_info`)
**고민**: 반환값이 필요한가?
**결론**: 정보 출력이 목적이므로 `return` 불필요

## 🐛 발견된 문제점들과 해결책

### 1. 로직 오류
**문제**: 비밀번호 오류 시 함수가 계속 실행됨
**해결**: `return` 추가로 함수 실행 중단

### 2. 마이너스 계좌 한도 검증 오류
**문제**: 출금 전 잔액만 확인
**해결**: 출금 후 잔액이 -500,000을 초과하는지 확인
```python
# 잘못된 구현
if self.__balance >= -500000:

# 올바른 구현
if self.__balance - amount >= -500000:
```

### 3. 저축계좌 출금 제한 미구현
**문제**: 1년 경과 여부 확인 로직 없음
**해결**: `datetime` 모듈 사용하여 경과일 계산

## 📚 Python 문법 학습

### 1. `return` 문 사용 기준
- **값을 반환해야 할 때**: `return 값`
- **함수 실행을 중단해야 할 때**: `return`
- **단순 작업만 수행할 때**: `return` 불필요 (자동으로 `None` 반환)

### 2. `return` vs `break`
- **`return`**: 함수 내에서 사용, 함수 실행 중단
- **`break`**: 반복문 내에서 사용, 반복문 실행 중단

### 3. Private 속성 (`__`)
- **용도**: 클래스 외부에서 직접 접근 방지
- **접근 방법**: getter/setter 메소드 사용

## 🎯 설계 원칙

### 1. 단일 책임 원칙
- 각 메소드는 하나의 명확한 목적을 가져야 함
- 출력과 반환을 분리하여 설계

### 2. 일관성
- 비슷한 기능의 메소드는 일관된 패턴 사용
- 에러 처리 방식 통일

### 3. 실용성
- 과제 요구사항에 충분히 부합하면서도 간결한 코드
- 불필요한 복잡성 제거

## 🔄 Git 작업 과정

### 1. 브랜치 관리
- `kwanju` 브랜치에서 개발
- `main` 브랜치로 병합

### 2. 커밋 메시지
- 명확하고 설명적인 커밋 메시지 작성
- 예: "feat:Update wrong logic code, test code and add finalizer"

### 3. 인증 문제 해결
- GitHub 권한 확인
- 터미널에서 직접 Git 명령 실행으로 인증 갱신

## 📝 향후 개선 방향

### 1. 기능 확장
- 이자 계산 및 적용 기능
- 거래 내역 기록 기능
- 계좌 이체 기능

### 2. 코드 개선
- 예외 처리 강화
- 입력값 검증 강화
- 로깅 기능 추가

### 3. 테스트 코드
- 단위 테스트 작성
- 다양한 시나리오 테스트

## 💡 학습한 교훈

1. **함수 설계 시 목적을 명확히 하기**
2. **Python 문법의 정확한 이해와 적용**
3. **문제 해결 과정에서의 체계적 접근**
4. **코드 리뷰와 개선의 중요성**
5. **Git을 활용한 버전 관리의 필요성**

---
*이 문서는 은행 계좌 시스템 개발 과정에서의 학습 내용을 정리한 것입니다.* 