import glob
import os
import cv2
import time
import face_detection


def draw_blur(image, bboxes):
    # get width and height of the image
    h, w = image.shape[:2]
    # gaussian blur kernel size depends on width and height of original image
    kernel_width = (w // 7) | 1
    kernel_height = (h // 7) | 1

    for bbox in bboxes:
        x0, y0, x1, y1 = [int(_) for _ in bbox]

        # get the face image
        face = image[y0: y1, x0: x1]
        # apply gaussian blur to this face
        face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
        # put the blurred face into the original image
        image[y0: y1, x0: x1] = face





def find_and_blur_faces(folder_path):
    impaths = folder_path
    impaths = glob.glob(os.path.join(impaths, "*.jpg"))
    detector = face_detection.build_detector(
        "DSFDDetector",
        max_resolution=1080
    )
    for impath in impaths:
        if impath.endswith("out.jpg"): continue
        im = cv2.imread(impath)
        print("Processing:", impath)
        t = time.time()
        dets = detector.detect(
            im[:, :, ::-1]
        )[:, :4]
        print(f"Detection time: {time.time() - t:.3f}")
        draw_blur(im, dets)
        imname = os.path.basename(impath).split(".")[0]
        output_path = os.path.join(
            os.path.dirname(impath),
            f"{imname}_out.jpg"
        )
        cv2.imwrite(output_path, im)
