<p align="center">
<img src="pictures/logo.png" height=400px width=400px>  
</p>

<p align="center">
<u><b>사장님용 QR체크인, 전자출입명부를 위한 파이썬 API Wrapper</b></u><br><b>QR체크인도 할수 있어요!</b> 
</p>
<hr>

<p align="center">
  <a href="https://github.com/alus20x/PyKIPass/blob/main/LICENSE"
    ><img
      src="https://img.shields.io/badge/license-CC--BY--NC--4.0-orange?style=flat-square"
      alt="repo license"
  /></a>
    <a href="https://pypi.org/project/PyKIPass"
    ><img
      src="https://img.shields.io/pypi/v/PyKIPass?style=flat-square"
      alt="pypi"
  /></a>
  
  
</p>


## Legal Disclaimer
**서비스에 무리가 갈정도로 요청하지 마세요.**
**Do not send request over a short span.**

비상업적 용도만 사용 가능. 오직 교육적 목적으로만 사용할수 있으며, 전자출입명부(KIPass)는 질병관리청의 자산입니다. 악의적 공격에 이용할시 처벌 받을수 있습니다. 사용에 따른 책임은 사용자가 집니다. 

Non Commercial Only. Only use for educational purposes, KIPass is asset of MOHW. User takes responsibility for usage.

## Install
```
pip install PyKIPass
```

## Using

### Import
```python
> from PyKIPass import *
```

### Login
```python
> kipass = KIPass("USERNAME", "PASSWORD")
```

#### Security Considerations
아이디, 비밀번호는 환경변수를 이용해 저장하는것이 보안상 좋습니다.

```python
> import os
> kipass = KIPass(username=os.environ.get("KI_PASS_ID"), password=os.environ.get("KI_PASS_PASSWORD"))
```


### 특정 날짜의 고객수 불러오기
```python
> 
```

### 특정 기간의 고객수 불러오기

### QR코드 인증하기
```python
```
