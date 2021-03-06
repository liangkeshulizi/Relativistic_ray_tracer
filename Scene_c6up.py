from my_raytracer import *

(width, height) = (1920, 1080)      # 屏幕尺寸
resolution= height/width
light_pos = vec3(0, 2, -2)          # 点光源位置
center = vec4(0, 0, 2.5, 0)         # 摄像机位置
focal_length= 200
shape1 = Sphere(.5, get_checkerboard_color_func(rgb(0,0.5,0), rgb(1,1,1)))
shape2 = Sphere(999999999, lambda p: rgb(0.5,0.5,0.5))#util.get_checkerboard_color_func(rgb(0,.05,.05),rgb(.5,.5,.5), 9999999999))
offset1 = vec4(0, 0.4, 0, 0)
offset2 = vec4(0, 0, -999999999.5, 0)
beta = (0.6, 0, 0)

movingobjects= [MovingObject(shape1, beta, offset1, Material(500)), MovingObject(shape2, (0,0,0), offset2, None)]#, MovingObject(light_ball, (0,0,0), offset_light, None)]

# Screen coordinates: x0, y0, x1, y1
camera_height= 200
camera_width= camera_height/resolution
S = (-camera_width, camera_height, camera_width, -camera_height)
x= np.tile(np.linspace(S[0], S[2], width), height)     # [1,2,3,4,1,2,3,4,1,2,3,4]
z= np.repeat(np.linspace(S[1], S[3], height), width)   # [1,1,1,1,2,2,2,2,3,3,3,3]
y= -focal_length
origin_to_image_times= abs(vec4(0,x,y,z))

t_start= time.time()
frames= 250
for shot_time, frame_count in np.linspace([-2.5,1],[8,frames], frames):
    start= center + vec4(shot_time, 0, 0, 0)
    directions= vec4(-origin_to_image_times, x, y, z)
    print('开始渲染第%s帧' % int(frame_count))
    t0 = time.time()
    color = raytrace(start, directions, movingobjects, light_pos)
    print("  耗时%f，预计剩余%i分钟"%(time.time()-t0, (time.time()-t_start)/frame_count*(frames-frame_count)/60))
    filename= "C:\\render\\c0.6up\\%i.png" % frame_count
    file_color = [Image.fromarray((255 * np.clip(c, 0, 1).reshape((height, width))).astype(np.uint8), "L") for c in color.components()]
    Image.merge("RGB", file_color).save(filename)