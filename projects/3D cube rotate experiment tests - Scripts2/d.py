# works
# there is a paper written by me

import random



pool=[

# 14,,,2
# 14,536,2
[
['down','rotateX(-90deg)',[1,4,5,3,6,2],4],
['right','rotateZ(90deg)',[1,4,5,3,6,2],5],
['down','rotateY(-90deg)',[1,4,5,3,6,2],3],
['up','rotateY(90deg)',[1,4,5,3,6,2],6],
['right','rotateZ(90deg)',[1,4,5,3,6,2],2],
],

# 14,635,2
# [

# ]




]



























# seq=random.choice(pool)






def transform_animation_gen(css_code=pool[0]):
	transform=""
	com_transform=""
	for_i=1
	rotateX=0
	rotateY=0
	rotateZ=0
	for i in css_code:
		print(i)
		
		if(i[1][0:7]=="rotateX"):
			# print('X',css_code[i]["rotate"][0:7],css_code[i]["rotate"][-6:-4])

			rotateX+=int(i[1][8:-4])
			transform+=f'{(100/5)*for_i}%'+'{-webkit-transform: '+f'rotateY({rotateY}deg) rotateX({rotateX}deg) rotateZ(0deg)'+';}\n'+f'/* ({i}-to-) */\n\n'
			com_transform+=f'{(100/5)*for_i}%'+'{-webkit-transform: '+f'rotateY({rotateY}deg) rotateX({rotateX}deg) rotateZ({rotateZ}deg)'+';}\n'
		
		elif(i[1][0:7]=="rotateY"):
			# print('Y',css_code[i]["rotate"][0:7],css_code[i]["rotate"][-6:-5])
			
			rotateY+=int(i[1][8:-4])
			transform+=f'{(100/5)*for_i}%'+'{-webkit-transform: '+f'rotateY({rotateY}deg) rotateX({rotateX}deg) rotateZ({rotateZ}deg)'+';}\n'+f'/* ({i}-to-) */\n\n'
			com_transform+=f'{(100/5)*for_i}%'+'{-webkit-transform: '+f'rotateY({rotateY}deg) rotateX({rotateX}deg) rotateZ({rotateZ}deg)'+';}\n'

		elif(i[1][0:7]=="rotateZ"):
			# print('Z',css_code[i]["rotate"][0:7],css_code[i]["rotate"][-6:-5])
			
			rotateZ+=int(i[1][8:-4])
			transform+=f'{(100/5)*for_i}%'+'{-webkit-transform: '+f'rotateY({rotateY}deg) rotateX({rotateX}deg) rotateZ({rotateZ}deg)'+';}\n'+f'/* ({i}-to-) */\n\n'
			com_transform+=f'{(100/5)*for_i}%'+'{-webkit-transform: '+f'rotateY({rotateY}deg) rotateX({rotateX}deg) rotateZ({rotateZ}deg)'+';}\n'

		for_i+=1
	return [transform,com_transform]




seq=transform_animation_gen()



print(seq[0])


print(seq[1])