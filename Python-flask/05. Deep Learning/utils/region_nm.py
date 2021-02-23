def region_name(df):
    region = []
    for i in df.index:
        if df['도로명주소'][i].split()[2][-1] == '구':
            if df['도로명주소'][i].split()[0][-2] == '북':
                region.append(df['도로명주소'][i].split()[0][0] + '북' + ' ' + df['도로명주소'][i].split()[1] + ' ' + df['도로명주소'][i].split()[2])
            elif df['도로명주소'][i].split()[0][-2] == '남':
                region.append(df['도로명주소'][i].split()[0][0] + '남' + ' ' + df['도로명주소'][i].split()[1] + ' ' + df['도로명주소'][i].split()[2])
            else:
                region.append(df['도로명주소'][i].split()[0][:2] + ' ' + df['도로명주소'][i].split()[1] + ' ' + df['도로명주소'][i].split()[2])
        else:
            if df['도로명주소'][i].split()[0][-2] == '북':
                region.append(df['도로명주소'][i].split()[0][0] + '북' + ' ' + df['도로명주소'][i].split()[1])
            elif df['도로명주소'][i].split()[0][-2] == '남':
                region.append(df['도로명주소'][i].split()[0][0] + '남' + ' ' + df['도로명주소'][i].split()[1])
            elif df['도로명주소'][i].split()[0][:2] == '세종':
                region.append(df['도로명주소'][i].split()[0][:2] + ' ' + '세종시')
            else:
                region.append(df['도로명주소'][i].split()[0][:2] + ' ' + df['도로명주소'][i].split()[1])
    return region

def region_id(lst):
    ids = []
    for i in range(len(lst)):
        if len(lst[i].split()) == 3:
            if len(lst[i].split()[2]) == 2:
                ids.append(lst[i].split()[1][:-1] + ' ' + lst[i].split()[2])
            elif lst[i].split()[2] in ['마산합포구', '마산회원구']:
                ids.append(lst[i].split()[1][:-1] + ' ' + lst[i].split()[2][2:-1])  
            else:
                ids.append(lst[i].split()[1][:-1] + ' ' + lst[i].split()[2][:-1])
        else:
            if lst[i].split()[0] in ['서울', '인천', '대구', '대전', '부산', '울산', '광주']:
                if len(lst[i].split()[1]) == 2:
                    ids.append(lst[i].split()[0] + ' ' + lst[i].split()[1])
                else:
                    ids.append(lst[i].split()[0] + ' ' + lst[i].split()[1][:-1])
            else:
                if lst[i].split()[1] == '고성군' and lst[i].split()[0] == '강원':
                    ids.append('고성(강원)')
                elif lst[i].split()[1] == '고성군' and lst[i].split()[0] == '경남':
                    ids.append('고성(경남)')
                else:
                    ids.append(lst[i].split()[1][:-1])
    return ids