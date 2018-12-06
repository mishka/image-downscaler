import subprocess, sys
from termcolor import colored
from imutils import paths
from PIL import Image

nupscaled = 0
bad = 0
count = 0

for img in paths.list_images(sys.argv[1]):
    result = subprocess.run(['resdet', img], stdout=subprocess.PIPE).stdout.decode('utf-8')
    lst = result.splitlines()
    res = lst[0][7:]
    org = lst[1][12:]
    orgs = org.split("x")
    x = int(orgs[0])
    y = int(orgs[1][:4])

    if "(not upsampled)" in org:
        print(colored(f"[-] Not upscaled.. {x}x{y}", "white"))
        nupscaled += 1
        pass
    elif x < 400 or y < 400:
        print(colored(f"[x] Bad detection, skipping. {res} - {x}x{y}", "red"))
        bad += 1
        pass
    else:
        print(colored(f"[+] Downscaling {res} to {org}", "green"))
        pic = Image.open(img)
        resize = pic.resize((x, y), Image.ANTIALIAS)
        resize.save(img, pic.format, quality=100)
        count += 1

print(f"\nStats\n Healty : {nupscaled}\n Downscaled : {count}\n Bad detection : {bad}")