import os
from PIL import Image
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np
import csv
import math

class histogram:
    def __init__(self, ROOT_DIR):
        super().__init__()

        print('2015253039 권진우 영상처리 HW2 \n')

        # image 불러오기
        self.image_name = 'lena_gray_8bit.bmp'

        if os.path.isfile(os.path.join(ROOT_DIR, self.image_name)):
            self.lena = Image.open(os.path.join(ROOT_DIR, self.image_name))

        # initialize
        self.initiate(ROOT_DIR) # self.intensity (영상 전체 픽셀의 명암 값을 받기 위해)

        self.control()

    def control(self):
        print('0. 프로그램 종료')
        print('1. lena.bmp의 히스토그램')
        print('2. lena.bmp의 평활화 히스토그램')
        print('3. lena.bmp의 스트레칭 히스토그램')
        print('4. lena.bmp의 엔드인 스트레칭 히스토그램')
        mode = int(input("수행 할 과제 번호 입력 1~4 :"))

        if mode is 1:
            self.histo_1() # 기존 histogram
        elif mode is 2:
            self.histo_2() # 평활화
        elif mode is 3:
            self.histo_3() # 스트레칭
        elif mode is 4:
            self.histo_4() # 엔드인 탐색 스트레칭
        elif mode is 0:
            print('프로그램을 종료합니다.')
            exit() # 프로그램 종료
        else:
            print('0~5사이의 정수를 입력하여주십시오.')

    def histo_4(self): # 엔드인 탐색 히스토그램
        print('End-In Stretching Histogram')
        new_pixel = []
        ei_pixel_num = []
        ei_intensity2 = np.array([[0]*512]*512)

        # 50~190 까지의 값을 기준으로 엔드인 탐색에 맞게 수식 대입 & 클램핑 작업
        for i, e in enumerate(self.intensity):
            if e <= 50:
                new_pixel.append(0)
            elif 50 < e and e < 190:
                new_pixel.append(int((255*(e-50)/140)))
            else:
                new_pixel.append(255)
            x = math.floor(i / 512)
            y = int(i % 512)
            ei_intensity2[x][y] = new_pixel[-1]

        for i in range(256):
            ei_pixel_num.append(new_pixel.count(i)) # 새 픽셀 명암 분포에 따라 빈도수를 세어서

        plt.plot(self.bright_hist, ei_pixel_num)
        plt.title('End-In Stretched Histogram')
        plt.xlabel('Bright')
        plt.ylabel('Frequency')
        plt.show()
        plt.title('End-In Stretched image')
        plt.imshow(ei_intensity2, cmap='gray')
        plt.show()

        self.control()

    def histo_3(self): # 스트레칭 히스토그램
        print('Stretched Histogram')

        st_intensity = []
        st_intensity2 = np.array([[0]*512]*512)
        st_pixel_num = []
        low = 0
        high = 0

        for i, e in enumerate(self.pixel_num): # low값 찾기
            if int(e) is not 0:
                low = int(i)
                break
        for i in range(low, len(self.pixel_num)): # high값 찾기
            if int(self.pixel_num[i]) is 0:
                high = int(i)
                break

        for i, e in enumerate(self.intensity): # 스트레칭 공식을 통해 픽셀 마다의 새로운 명암 값을 넣은 배열 만들기
            st_intensity.append(int(255*((e-low)/(high-low))))
            x = math.floor(i / 512)
            y = int(i % 512)
            st_intensity2[x][y] = st_intensity[-1]

        for i in range(256): # 히스토그램 분포를 만들기 위해 명암 값의 개수 세기
            st_pixel_num.append(st_intensity.count(i))

        plt.plot(self.bright_hist, st_pixel_num)
        plt.title('Stretched Histogram')
        plt.xlabel('Bright')
        plt.ylabel('Frequency')
        plt.show()
        plt.title('Stretched image')
        plt.imshow(st_intensity2, cmap='gray')
        plt.show()

        self.control()

    def histo_2(self): # 평활화 히스토그램

        accumulated_sum = [0]*256

        accumulate = 0
        for i, e in enumerate(self.pixel_num): # self.pixel_num = 누적 합에 대한 배열리스트 # accumulate : 누적 합 배열
            accumulate = accumulate + e
            accumulated_sum[i] = accumulated_sum[i] + accumulate
        print("누적 합 배열 넣기 끝")

        Normalized_sum = [0]*256 # 정규화된 누적 합

        for a in range(256):
            Normalized_sum[a] = 255*accumulated_sum[a]/(512*512) if 255 >= 255*accumulated_sum[a]/262144 else 255 # 밝기 최대 값*누적합/총 픽셀 수
        print("정규화 누적 합 배열 넣기 끝") # 255가 넘는 값에 대해서는 255로 클램핑

        print(int(0.8))
        eq_intensity = []
        eq_intensity2 = np.array([[0]*512]*512) # 이미지를 띄우기 위한 2차원 배열 선언
        for i, e in enumerate(self.intensity): # 262144개의 pixel에 대해서 평활화 과정 수행
            eq_intensity.append(int(Normalized_sum[e])) # 첫번째 픽셀 값부터 정규화 합 배열의 값으로 치환
            x = math.floor(i/512)
            y = int(i%512)
            eq_intensity2[x][y] = eq_intensity[-1]

        eq_pixel_num = []
        for i in range(256):
            eq_pixel_num.append(eq_intensity.count(i)) # 0~255 밝기 값에 대한 수를 list에 받아서 히스토그램에 적용

        plt.plot(self.bright_hist, eq_pixel_num) # 평활화 된 히스토그램
        plt.title('Equalized Histogram')
        plt.xlabel('Bright')
        plt.ylabel('Frequency')
        plt.show()
        plt.title('Equalized image')
        plt.imshow(eq_intensity2, cmap='gray')
        plt.show()

        self.control()

    def histo_1(self): # 기본 히스토그램 출력
        # X축(bright_hist : 0~255배열), Y축(pixel_num : 해당 명암 값을 가진 픽셀 개수)
        plt.plot(self.bright_hist, self.pixel_num)
        plt.title('lena Histogram')
        plt.xlabel('Bright')
        plt.ylabel('Frequency')
        plt.show()
        plt.imshow(self.array_lena, cmap='gray') # Gray Scale로 출력
        plt.show()

        self.control()

    # 프로그램 수행 초기화 과정 : 불러온 이미지 np.array에 넣기, 1차원 나열, 명암 값 분포 Compute
    def initiate(self, ROOT_DIR):
        intensity = []  # 영상 각 Pixel의 명도
        bright_hist = []  # histogram X축 밝기 값 list
        pixel_num = [0 for i in range(256)]  # 0~255에 대해 해당 밝기 값을 가진 픽셀의 개수 0~255범위의 배열을 넣을 예정

        list = []  # csv파일을 읽을 때 받는 list

        array_lena = np.array(self.lena)
        self.array_lena = array_lena

        for i in range(len(array_lena[0])):
            for j in array_lena[i]:
                intensity.append(j)  # 1차원 형태로 정렬

        # 히스토그램 X축(밝기 값)에 대한 list
        for i in range(256):
            bright_hist.append(i)

        # 이미지에 대한 명암 값 분포 값을 csv에 저장 시켜둠으로써 이후 수행부터는 csv에서 읽음으로써 더욱 빠른 프로그램 수행
        if os.path.exists(
                os.path.join(ROOT_DIR, self.image_name + '.csv')):  # 이전에 수행한 적 있으면 csv로 명암값에 대한 histogram 값이 저장 되어있다.
            with open(self.image_name + '.csv', 'r') as rfp:  # csv 명암 값 읽기
                csv_read = csv.reader(rfp, delimiter=',', quotechar='"')
                for row in csv_read:
                    list.append(row)
            str_pixel_num = list[0]
            pixel_num = [int(i) for i in str_pixel_num]  # list 전체 원소를 int type으로 변환
        else:  # 이전에 수행된 적 없는 이미지이면 histogram 각 픽셀의 명암 값에 대해서 Search 수행
            print('영상으로부터 Pixel 명암 값 Search 수행시작')
            for i in intensity:
                pixel_num[i] += 1

            # 명암 값의 개수를 세기 위한 또 다른 Method
            # for i in range(256):
            #     pixel_num.append(intensity.count(i))

            # for bright in range(256):
            #     for pixel in range(len(intensity)):
            #         if bright == intensity[pixel]:
            #             hist[bright] = hist[bright] + 1
            #     if i % 5 == 0:
            #         print('진행률% :', i * 100 / 255)

            # 이미지에 대한 명암값이 csv 파일로 존재한다면 불러와서 바로 프로그램 Initiate 과정 마무리
            with open(self.image_name + '.csv', 'w', encoding="utf-8") as fp:  # 명암 값 csv 형태로 저장
                for i in range(255):
                    fp.write(str(pixel_num[i]) + ',')
                fp.write(str(pixel_num[255]))

            fp.close()

        self.intensity = intensity
        self.bright_hist = bright_hist
        self.pixel_num = pixel_num

        return
