import sys
from datetime import datetime, timedelta
import pandas as pd

csv_name = input("CSV 파일 이름을 입력하세요: ")
json_name = input("JSON 파일 이름을 입력하세요: ")

def delta_to_datetime(delta_time):
    # 1970년 1월 1일부터의 초 단위로 된 시간을 구합니다.
    epoch = datetime(1970, 1, 1)
    # delta time을 timedelta 객체로 변환합니다.
    timedelta_obj = timedelta(seconds=delta_time)
    # epoch 시간에 timedelta를 더하여 새로운 datetime을 계산합니다.
    new_datetime = epoch + timedelta_obj
    return new_datetime

with open(json_name, 'r') as f:
    f.readline()
    data = f.readline()

# 시간 변환 코드
delta_time = float(data[6:23])
new_datetime = delta_to_datetime(delta_time)

# 분과 초만 문자열로 나타낸 코드
# 59: 0을 비교하는걸 막기 위해 10을 더하고 60
json_time = str(new_datetime)[14:16]+str(new_datetime)[17:19]+str(new_datetime)[20:]
print(json_time)

if json_time.startswith('58') or json_time.startswith('59'):
    print("json_data의 시간이 58분 또는 59분입니다. 오류가 발생할 가능성이 있으니 수동으로 처리하세요")
    sys.exit()

csv_data = pd.read_csv(csv_name, header=None)
csv_data.columns = ['time', 'artist', 'X', 'Y', 'Z']

# 'time' 열의 앞의 부분을 제거
csv_data['time'] = csv_data['time'].str[14:16]+csv_data['time'].str[17:19]+csv_data['time'].str[20:]

# CSV 데이터가 비어있지 않고, 첫 번째 행의 값이 json_time보다 큰지 확인
if not csv_data.empty and csv_data['time'].iloc[0] > json_time:
    print("CSV_data 가 JSON_data 보다 늦게 찍힘")
    sys.exit()

csv_data = csv_data[csv_data['time'] >= json_time]

# csv_data에서 'time'과 'artist' 열 제거
csv_data.drop(columns=['time', 'artist'], inplace=True)

# 수정된 데이터를 새로운 CSV 파일로 저장
csv_data.to_csv(csv_name, index=False)
print(csv_name + " 으로 정상적으로 저장됨")