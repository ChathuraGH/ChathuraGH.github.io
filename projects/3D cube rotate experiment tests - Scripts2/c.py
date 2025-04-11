# works
# there is a paper written by me

import random



pool=[1,2,3,4,5,6]

s_2_near=[1,5,3,6]
s_4_near=[1,5,3,6]

s_1_near=[2,5,4,6]
s_3_near=[2,4,5,6]

s_5_near=[1,4,3,2]
s_6_near=[1,2,3,4]




def Random_Box_Sequence_Generator_V2(start=1):
	sq=[start]
	try:
		for i in range(0,5):
			item=random.choice(list(set(eval(f's_{sq[-1]}_near'))-set(sq)))
			# random.choice()
			print(item)
			sq.append(item)
		# if(len(sq)<6):
		# 	Random_Box_Sequence_Generator_V2()
		# else:
		print(random.choice(pool),'z1z',sq[-1],s_2_near[1],sq)
		return sq
	except:	
		if(len(sq)<6):
			return Random_Box_Sequence_Generator_V2()
		else:
			print(random.choice(pool),'z2z',sq[-1],s_2_near[1],sq)
			return sq



def Gen_Z():
	sq=Random_Box_Sequence_Generator_V2(1)
	if(sq[-1] in [2,4,5,6]):
		return sq

	else:
		return Gen_Z()



seq=Gen_Z()




a_s_2_near={
'3':{'direction':'up','rotate':'rotateX(90deg)'},
'1':{'direction':'down','rotate':'rotateX(-90deg)'},
'5':{'direction':'right','rotate':'rotateY(90deg)'},
'6':{'direction':'left','rotate':'rotateY(-90deg)'}
}
a_s_4_near={
'1' : {'direction':'up','rotate':'rotateX(90deg)'},
'3' : {'direction':'down','rotate':'rotateX(-90deg)'},
'5' : {'direction':'right','rotate':'rotateY(90deg)'},
'6' : {'direction':'left','rotate':'rotateY(-90deg)'}
}


# done
a_s_1_near={
'2' : {'direction':'up','rotate':'rotateX(90deg)'},
'4' : {'direction':'down','rotate':'rotateX(-90deg)'},
'5' : {'direction':'right','rotate':'rotateY(90deg)'},
'6' : {'direction':'left','rotate':'rotateY(-90deg)'}
}
a_s_3_near={
'2':{'direction':'down','rotate':'rotateX(-90deg)'},
'4':{'direction':'up','rotate':'rotateX(90deg)'},
'5':{'direction':'right','rotate':'rotateY(90deg)'},
'6':{'direction':'left','rotate':'rotateY(-90deg)'}
}

a_s_5_near={
'1':{'direction':'left','rotate':'rotateY(-90deg)'},
'4':{'direction':'down','rotate':'rotateX(-90deg)'},
'3':{'direction':'right','rotate':'rotateY(90deg)'},
'2':{'direction':'up','rotate':'rotateX(90deg)'}
}
a_s_6_near={
'1' : {'direction':'right','rotate':'rotateY(90deg)'},
'2' : {'direction':'up','rotate':'rotateX(90deg)'},
'3' : {'direction':'left','rotate':'rotateY(-90deg)'},
'4' : {'direction':'down','rotate':'rotateX(-90deg)'}
}



print('\n\n')


def css(seq=seq):
	css={}

	for i in seq[0:-1]:


		print(i,seq.index(i),'::',seq[seq.index(i)+1],seq.index(seq[seq.index(i)+1]),f'({i}-to-{seq[seq.index(i)+1]})')
		
		css[f"{i}"]=eval(f'a_s_{i}_near["{seq[seq.index(i)+1]}"]')
		# css[i]=eval(f'a_s_{i}_near["{seq[seq.index(i)+1]}"]')
		
		print(eval(f'a_s_{i}_near["{seq[seq.index(i)+1]}"]'))

	print('\n\n')
	print(css)
	return css




css_code=css()





def transform_animation_gen(css_code=css_code):
	transform=""
	for_i=1
	rotateX=0
	rotateY=0
	for i in css_code:
		print(i)
		
		if(css_code[i]["rotate"][0:7]=="rotateX"):
			# print('X',css_code[i]["rotate"][0:7],css_code[i]["rotate"][-6:-4])

			rotateX+=int(css_code[i]["rotate"][8:-4])
			transform+=f'{(100/5)*for_i}%'+'{-webkit-transform: '+f'rotateY({rotateY}deg) rotateX({rotateX}deg) rotateZ(0deg)'+';}\n'+f'/* ({i}-to-) */\n\n'

		
		elif(css_code[i]["rotate"][0:7]=="rotateY"):
			# print('Y',css_code[i]["rotate"][0:7],css_code[i]["rotate"][-6:-5])
			
			rotateY+=int(css_code[i]["rotate"][8:-4])
			transform+=f'{(100/5)*for_i}%'+'{-webkit-transform: '+f'rotateY({rotateY}deg) rotateX({rotateX}deg) rotateZ(0deg)'+';}\n'+f'/* ({i}-to-) */\n\n'

		
		for_i+=1
	return transform




print(transform_animation_gen())


print(seq)


