rem 작업 스케줄러 등록
schtasks /create /tn "월간 정리 작업" /tr "C:\Users\Administrator\Desktop\MonthWork.bat" /sc MONTHLY /d 2
rem 작업 스케줄러 삭제
schtasks /delete /tn "월간 정리 작업"
