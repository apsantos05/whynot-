import subprocess
A="/mnt/user-data/uploads/Downloads/_claude_assets/snd/"
items=[ # file, start, volume, extra filter
 (A+"2023-01-14 Chasing Crop Circles - Spooky.wav",0.0,0.45,"afade=t=in:d=2.5,afade=t=out:st=19.6:d=1.4"),
 (A+"2022-04-23 Occult Blood - Spooky Times.wav",0.0,0.55,"afade=t=in:d=3"),
 (A+"spell_fire_01.ogg",0.35,0.45,"lowpass=f=3000"),
 (A+"2023-02-15 Dancing in the Shallows - Reverse Cymbals.wav",1.27,0.7,""),
]+[(A+"2022-08-17 Approaching the Crash Site - Boom.wav",t,0.95,"") for t in (2.2,3.0,3.8,4.6,5.3)]+[
 ("creak.wav",2.9,0.7,""),
 (A+"2022-10-26 Fire in the Mist - Vocal Mist.wav",6.0,0.7,"afade=t=in:d=0.6"),
 (A+"2022-10-26 Fire in the Mist - Breath Riser.wav",5.5,0.6,""),
]+[(A+"2022-08-17 Approaching the Crash Site - Boom.wav",t,0.85,"") for t in (9.0,10.0,11.0,12.0)]+[
 (A+"2022-04-16 Triple-C THICCC - Heavy Breathing.wav",10.4,0.6,""),
 ("laugh_deep.wav",12.35,1.0,""),
 (A+"2023-03-23 Lunar Descent - Reverse.wav",11.85,0.8,""),
 (A+"2022-08-17 Approaching the Crash Site - Boom.wav",13.0,1.0,""),
 (A+"breath.ogg",15.35,0.9,""),
 ("blow.wav",15.45,0.9,""),
 (A+"2022-08-17 Approaching the Crash Site - Boom.wav",16.3,1.0,""),
 ("laugh_tail.wav",17.0,0.55,""),
 (A+"2022-08-17 Approaching the Crash Site - Boom.wav",18.2,0.9,""),
]
cmd=["ffmpeg","-v","error","-y"]
for f,_,_,_ in items: cmd+=["-i",f]
fc=[]; labels=[]
for i,(f,st,v,ex) in enumerate(items):
    ch=f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo"
    if ex: ch+=","+ex
    # duck the beds around the blow-out
    if i in (0,1): ch+=",volume='if(between(t,15.5,16.25),0.15,1)':eval=frame"
    ch+=f",volume={v},adelay={int(st*1000)}|{int(st*1000)}[a{i}]"
    fc.append(ch); labels.append(f"[a{i}]")
fc.append("".join(labels)+f"amix=inputs={len(items)}:normalize=0:duration=longest,atrim=0:21,alimiter=limit=0.9,afade=t=out:st=20.2:d=0.8[out]")
cmd+=["-filter_complex",";".join(fc),"-map","[out]","-ar","44100","mix.wav"]
subprocess.run(cmd,check=True)
