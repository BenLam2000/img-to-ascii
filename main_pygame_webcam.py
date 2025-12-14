import cv2
import os
import numpy as np
import time
import pygame


def read_img(img_name, live_cam=False):
    if live_cam:
        image = img_name
        img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        img_ori = cv2.imread(img_name)
        # print(img_BGR)
        if img_ori.shape[2] == 3:  # color image
            img_gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
        else:
            img_gray = img_ori
    ori_height, ori_width = img_gray.shape

    return img_gray, ori_width, ori_height


# downscale
def downscale(img_gray, max_width, max_height):
    aspect_ratio = img_gray.shape[1]/img_gray.shape[0]
    # check for height
    new_width = int(aspect_ratio * max_height)
    new_height = max_height
    # check for width
    if new_width > max_width:
        new_height = int(max_width/aspect_ratio)
        new_width = max_width

    img_small = cv2.resize(img_gray, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
    # print(img_small.shape)
    return img_small


# takes in grayscale image and prints in ASCII image
def img2ascii(img_small):
    # os.system('cls')
    num_rows = len(img_small)
    num_columns = len(img_small[0])
    for row in range(num_rows):
        for col in range(num_columns):
            luminance_index = np.clip(int(img_small[row][col]/255 * len(chars)),0,len(chars)-1)
            # print(luminance_index)
            luminance = chars[luminance_index]
            x_shift = int(col - num_columns/2)
            y_shift = int(row - num_rows/2)
            x_pos = int(SCREEN_WIDTH/2 + x_shift*CHAR_SIZE + CHAR_SIZE/2)
            y_pos = int(SCREEN_HEIGHT/2 + y_shift*CHAR_SIZE + CHAR_SIZE/2)
            text_display(luminance, x_pos, y_pos)
            # print(luminance*2, end="")
        # print("\n", end="")


def text_display(char, x, y):
    text = font.render(str(char), True, (255, 255, 255))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


if __name__ == "__main__":
    # img = cv2.imread('pics/sequence1/000000.png')
    # print(img.shape)
    # print(os.listdir('pics/sequence1'))

    chars = '.,-~:;=!*#$@'

    # chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    # chars = chars[::-1]

    # chars = " .:-=+*#%@"
    # print(len(chars))

    # @@@@@@@@@@@@@@@@@@@ CHANGE THIS @@@@@@@@@@@@@@@@@@@@@@@@@@@
    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
    FPS = 60
    FONT_SIZE = 10
    CHAR_SIZE = 11
    # folder = 'pics/sequence1'
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    CHAR_WIDTH, CHAR_HEIGHT = int(SCREEN_WIDTH/CHAR_SIZE), int(SCREEN_HEIGHT/CHAR_SIZE)  # how many ASCII characters to fit in pygame screen

    # img_names = os.listdir(folder)
    # img_count = len(img_names)
    # img_id = 0

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Monospace', FONT_SIZE, bold=True)

    # # test live camera
    # # Create a VideoCapture object to access the camera
    # cap = cv2.VideoCapture(0)
    # # 0 represents the default camera (you may use 1, 2, etc., to switch between multiple cameras if available)
    # frame = 0
    #
    # while True:
    #     # Capture frame-by-frame
    #     ret, frame = cap.read()
    #
    #     # Display the frame
    #     cv2.imshow('Live Video', frame)
    #
    #     # Break the loop when 'q' is pressed
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #
    # # Release the VideoCapture object and close the window
    # cap.release()
    # cv2.destroyAllWindows()
    # print(frame.shape)


    # Create a VideoCapture object to access the camera
    cap = cv2.VideoCapture(0)

    paused = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    paused = not paused

        # Capture frame-by-frame
        ret, frame = cap.read()
        # Display the frame
        cv2.imshow('Live Video', frame)

        screen.fill((0,0,0))
        # text_display('@'*38, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

        # img_name = img_names[img_id]
        # img_filepath = os.path.join(folder, img_name)
        # img, width, height = read_img(img_filepath)
        img, width, height = read_img(frame, live_cam=True)
        img_downscaled = downscale(img, max_width=CHAR_WIDTH, max_height=CHAR_HEIGHT)
        img2ascii(img_downscaled)
        # img_id += 1
        # if img_id >= img_count:
        #     img_id = 0
        clock.tick(FPS)

        if not paused:
            pygame.display.update()

    cap.release()
    cv2.destroyAllWindows()
