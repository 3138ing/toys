# 1. 나눔폰트 설치
!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf

# 2. 런타임 다시 시작

# 3. 확인
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family']='NanumBarunGothic'

# 4. 확인2
import matplotlib.font_manager as fm
sorted([font.name for font in fm.fontManager.ttflist])
