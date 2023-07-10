import paddle
import tqdm
import os
from glob import glob
from ppgan.apps import AnimeGANPredictor

def merge_video(frames_path, video_path):
    # https://stackoverflow.com/questions/24961127/how-to-create-a-video-from-images-with-ffmpeg
    # merge_cmd = "ffmpeg -y -framerate 30 -pattern_type glob -i '{}/*.png'  -c:v libx264 -pix_fmt yuv420p {}".format(frames_path, video_path)
    merge_cmd = f"ffmpeg -y -framerate 30 -i {frames_path}/out%d.png -c:v libx264 -r 30 {video_path}"
    os.system(merge_cmd)

def divide_video(video_path, frames_path):
    divide_cmd = "ffmpeg -i {} {}/out%d.png".format(video_path, frames_path)
    os.system(divide_cmd)

def cartonify(predictor, src_video_path, input_dir, output_dir, dst_video_path):
    divide_video(src_video_path, input_dir)
    files = glob(input_dir+"/*.png")
    for f in tqdm.tqdm(files):
        predictor.myrun(f)
    merge_video(output_dir, dst_video_path)



if __name__ == "__main__":
    num = 2
    input_dir = f"videos/videoframe{num}"
    output_dir = f"videos/videoframe{num}_anima"
    src_video_path = f"videos/{num}.mp4"
    dst_video_path = f"videos/{num}_anima.mp4"
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    predictor = AnimeGANPredictor(output_path=output_dir)
    cartonify(predictor, src_video_path, input_dir, output_dir, dst_video_path)