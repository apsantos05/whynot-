"""Remove o "why not?" dourado de cima do neon no vídeo da cortina (inpaint quadro a quadro com máscara fixa).
Uso: python3 xmas_tira_whynot.py <entrada.mp4> <ultimo_quadro.png> <saida.mp4>"""
import sys, subprocess, numpy as np, cv2
IN, LAST, OUT = sys.argv[1:4]
Y0, Y1, X0, X1 = 495, 590, 400, 690
im = cv2.imread(LAST).astype(int); b, g, r = im[..., 0], im[..., 1], im[..., 2]
m = np.zeros(im.shape[:2], np.uint8)
box = (g > 45) & (r > 60) & (g > 0.5 * r)
m[Y0:Y1, X0:X1] = box[Y0:Y1, X0:X1].astype(np.uint8) * 255
m = cv2.dilate(m, np.ones((9, 9), np.uint8))
cv2.imwrite(OUT + '_mask.png', m)
W, H = 1080, 1920
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', IN, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '24', '-i', '-', '-i', IN,
                        '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '12', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'copy', OUT], stdin=subprocess.PIPE)
n = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
    sub = f[Y0 - 40:Y1 + 40, X0 - 40:X1 + 40]; ms = m[Y0 - 40:Y1 + 40, X0 - 40:X1 + 40]
    f[Y0 - 40:Y1 + 40, X0 - 40:X1 + 40] = cv2.inpaint(sub, ms, 9, cv2.INPAINT_TELEA)
    enc.stdin.write(f.tobytes()); n += 1
enc.stdin.close(); enc.wait(); print(n, 'quadros')
